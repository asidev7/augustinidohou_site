from django.contrib import admin
from django.utils.html import format_html
from .models import Produit, Commande


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display  = ('apercu', 'nom', 'type_produit', 'prix_affiche', 'en_vedette', 'disponible', 'ordre')
    list_display_links = ('apercu', 'nom')
    list_filter   = ('type_produit', 'en_vedette', 'disponible')
    list_editable = ('disponible', 'en_vedette', 'ordre')
    search_fields = ('nom', 'description')
    fieldsets = (
        ('Contenu FR', {'fields': ('nom', 'slug', 'description', 'type_produit', 'prix')}),
        ('Contenu EN', {'fields': ('nom_en', 'description_en'), 'classes': ('collapse',)}),
        ('Média & Options', {'fields': ('image', 'en_vedette', 'disponible', 'ordre')}),
    )

    def apercu(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:40px;height:40px;object-fit:cover;border-radius:6px"/>', obj.image.url)
        icons = {'livre': '📚', 'coaching': '🎯', 'service': '⚙️'}
        return icons.get(obj.type_produit, '📦')
    apercu.short_description = ''

    def prix_affiche(self, obj):
        return format_html('<strong>{}</strong>', obj.prix_formatte)
    prix_affiche.short_description = 'Prix'


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display  = ('date', 'nom', 'produit', 'montant_affiche', 'statut_badge', 'email', 'telephone')
    list_filter   = ('statut', 'produit__type_produit')
    search_fields = ('nom', 'email', 'telephone', 'fedapay_id')
    readonly_fields = ('date', 'fedapay_id', 'fedapay_token', 'montant')
    list_display_links = ('date', 'nom')

    def montant_affiche(self, obj):
        return f"{int(obj.montant):,} FCFA".replace(',', ' ')
    montant_affiche.short_description = 'Montant'

    def statut_badge(self, obj):
        colors = {
            'en_attente': '#f59e0b',
            'approuve':   '#22c55e',
            'annule':     '#ef4444',
            'rembourse':  '#6366f1',
        }
        c = colors.get(obj.statut, '#94a3b8')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 10px;border-radius:99px;font-size:.75rem;font-weight:700">{}</span>',
            c, obj.get_statut_display()
        )
    statut_badge.short_description = 'Statut'
