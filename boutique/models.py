from django.db import models
from django.utils.text import slugify


class Produit(models.Model):
    TYPE = [
        ('livre',    'Livre / E-book'),
        ('coaching', 'Coaching & Accompagnement'),
        ('service',  'Service Digital'),
    ]
    nom            = models.CharField(max_length=200)
    nom_en         = models.CharField(max_length=200, blank=True, verbose_name='Name (EN)')
    slug           = models.SlugField(max_length=220, unique=True, blank=True)
    description    = models.TextField()
    description_en = models.TextField(blank=True, verbose_name='Description (EN)')
    prix           = models.DecimalField(max_digits=10, decimal_places=0, help_text='Prix en XOF (FCFA)')
    image          = models.ImageField(upload_to='boutique/', blank=True, null=True)
    type_produit   = models.CharField(max_length=20, choices=TYPE, default='service', verbose_name='Type')
    en_vedette     = models.BooleanField(default=False, verbose_name='Mis en avant')
    disponible     = models.BooleanField(default=True)
    ordre          = models.PositiveSmallIntegerField(default=0)
    date_ajout     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordre', '-date_ajout']
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits / Services'

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.nom)
            slug, n = base, 1
            while Produit.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'; n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def prix_formatte(self):
        return f"{int(self.prix):,} FCFA".replace(',', ' ')


class Commande(models.Model):
    STATUT = [
        ('en_attente', 'En attente'),
        ('approuve',   'Approuvé ✓'),
        ('annule',     'Annulé'),
        ('rembourse',  'Remboursé'),
    ]
    produit       = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='commandes')
    nom           = models.CharField(max_length=200)
    email         = models.EmailField()
    telephone     = models.CharField(max_length=25)
    montant       = models.DecimalField(max_digits=10, decimal_places=0)
    fedapay_id    = models.CharField(max_length=100, blank=True, verbose_name='FedaPay ID')
    fedapay_token = models.CharField(max_length=300, blank=True, verbose_name='Token paiement')
    statut        = models.CharField(max_length=20, choices=STATUT, default='en_attente')
    note          = models.TextField(blank=True, verbose_name='Note client')
    date          = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'

    def __str__(self):
        return f"{self.nom} — {self.produit.nom} ({self.get_statut_display()})"
