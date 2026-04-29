import json
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Produit, Commande


def _fedapay_headers():
    return {
        'Authorization': f'Bearer {settings.FEDAPAY_SECRET_KEY}',
        'Content-Type': 'application/json',
    }

FEDAPAY_BASE = 'https://api.fedapay.com/v1'


def boutique_liste(request):
    livres   = Produit.objects.filter(disponible=True, type_produit='livre')
    coaching = Produit.objects.filter(disponible=True, type_produit='coaching')
    services = Produit.objects.filter(disponible=True, type_produit='service')
    vedettes = Produit.objects.filter(disponible=True, en_vedette=True)
    return render(request, 'boutique/liste.html', {
        'livres': livres, 'coaching': coaching,
        'services': services, 'vedettes': vedettes,
    })


def boutique_detail(request, slug):
    produit = get_object_or_404(Produit, slug=slug, disponible=True)
    similaires = Produit.objects.filter(
        disponible=True, type_produit=produit.type_produit
    ).exclude(pk=produit.pk)[:3]
    return render(request, 'boutique/detail.html', {
        'produit': produit, 'similaires': similaires,
    })


def boutique_checkout(request, slug):
    produit = get_object_or_404(Produit, slug=slug, disponible=True)
    erreur = None

    if request.method == 'POST':
        nom       = request.POST.get('nom', '').strip()
        email     = request.POST.get('email', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        note      = request.POST.get('note', '').strip()

        if not (nom and email and telephone):
            erreur = 'Veuillez remplir tous les champs obligatoires.'
        else:
            # Create order first
            commande = Commande.objects.create(
                produit=produit, nom=nom, email=email,
                telephone=telephone, montant=produit.prix, note=note,
            )

            # Create FedaPay transaction
            parts = nom.split(' ', 1)
            firstname = parts[0]
            lastname  = parts[1] if len(parts) > 1 else '.'

            callback = request.build_absolute_uri(
                f'/boutique/succes/{commande.pk}/'
            )

            payload = {
                'description': f'Achat: {produit.nom}',
                'amount': int(produit.prix),
                'currency': {'iso': 'XOF'},
                'callback_url': callback,
                'customer': {
                    'firstname': firstname,
                    'lastname': lastname,
                    'email': email,
                    'phone_number': {'number': telephone, 'country': 'BJ'},
                },
            }

            try:
                resp = requests.post(
                    f'{FEDAPAY_BASE}/transactions',
                    headers=_fedapay_headers(),
                    json=payload,
                    timeout=15,
                )
                data = resp.json()
                transaction = data.get('v1/transaction', {})
                transaction_id = transaction.get('id')

                if transaction_id:
                    # Get payment token
                    tok_resp = requests.post(
                        f'{FEDAPAY_BASE}/transactions/{transaction_id}/token',
                        headers=_fedapay_headers(),
                        timeout=15,
                    )
                    tok_data = tok_resp.json()
                    token = tok_data.get('token')

                    commande.fedapay_id    = str(transaction_id)
                    commande.fedapay_token = token or ''
                    commande.save(update_fields=['fedapay_id', 'fedapay_token'])

                    if token:
                        redirect_url = f'https://pay.fedapay.com/{token}'
                        return redirect(redirect_url)

                erreur = 'Erreur lors de la création du paiement. Veuillez réessayer.'
            except Exception:
                erreur = 'Impossible de joindre le service de paiement. Réessayez plus tard.'

    return render(request, 'boutique/checkout.html', {
        'produit': produit, 'erreur': erreur,
    })


def boutique_succes(request, commande_id):
    commande = get_object_or_404(Commande, pk=commande_id)
    # FedaPay will confirm via webhook; here we show optimistic success
    if commande.statut == 'en_attente':
        commande.statut = 'approuve'
        commande.save(update_fields=['statut'])
    return render(request, 'boutique/succes.html', {'commande': commande})


@csrf_exempt
@require_POST
def boutique_webhook(request):
    try:
        payload = json.loads(request.body)
        event = payload.get('name', '')
        if 'transaction.approved' in event:
            transaction = payload.get('object', {})
            fedapay_id = str(transaction.get('id', ''))
            if fedapay_id:
                Commande.objects.filter(fedapay_id=fedapay_id).update(statut='approuve')
        elif 'transaction.canceled' in event or 'transaction.declined' in event:
            transaction = payload.get('object', {})
            fedapay_id = str(transaction.get('id', ''))
            if fedapay_id:
                Commande.objects.filter(fedapay_id=fedapay_id).update(statut='annule')
    except Exception:
        pass
    return HttpResponse('OK', status=200)
