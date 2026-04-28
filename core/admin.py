from django.contrib import admin
from django.utils.html import format_html
from .models import ReseauSocial, Competence, Experience, Formation, Service, Categorie, Article, Message


@admin.register(ReseauSocial)
class ReseauSocialAdmin(admin.ModelAdmin):
    list_display = ('nom', 'icone_preview', 'url', 'ordre')
    list_editable = ('ordre',)

    def icone_preview(self, obj):
        return format_html('<i class="{}" style="font-size:1.2rem"></i> {}', obj.icone, obj.nom)
    icone_preview.short_description = 'Icône'


@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'niveau_bar', 'ordre')
    list_filter = ('categorie',)
    list_editable = ('ordre',)

    def niveau_bar(self, obj):
        return format_html(
            '<div style="width:120px;background:#eee;border-radius:4px;">'
            '<div style="width:{}%;background:#3b82f6;height:8px;border-radius:4px;"></div></div> {}%',
            obj.niveau, obj.niveau
        )
    niveau_bar.short_description = 'Niveau'


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('poste', 'entreprise', 'date_debut', 'en_cours', 'ordre')
    list_filter = ('en_cours',)
    list_editable = ('ordre',)


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('diplome', 'etablissement', 'date_debut', 'en_cours', 'ordre')
    list_editable = ('ordre',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'icone', 'ordre')
    list_editable = ('ordre',)


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug', 'icone', 'nb_articles')
    prepopulated_fields = {'slug': ('nom',)}

    def nb_articles(self, obj):
        return obj.articles.filter(publie=True).count()
    nb_articles.short_description = 'Articles publiés'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('apercu_image', 'titre', 'categorie', 'date', 'temps_lecture', 'vues_badge', 'publie')
    list_display_links = ('apercu_image', 'titre')
    list_filter = ('categorie', 'publie', 'date')
    search_fields = ('titre', 'resume', 'meta_keywords')
    prepopulated_fields = {'slug': ('titre',)}
    list_editable = ('publie',)
    readonly_fields = ('vues', 'date_modif', 'preview_image')

    fieldsets = (
        ('✏️ Contenu', {
            'fields': ('titre', 'slug', 'categorie', 'temps_lecture', 'publie')
        }),
        ('🖼️ Image principale', {
            'fields': ('image', 'preview_image'),
        }),
        ('📝 Texte', {
            'fields': ('resume', 'contenu'),
        }),
        ('🔍 SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',),
        }),
        ('📊 Statistiques', {
            'fields': ('vues', 'date_modif'),
            'classes': ('collapse',),
        }),
    )

    def apercu_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:54px;height:40px;object-fit:cover;border-radius:6px;"/>',
                obj.image.url
            )
        return format_html(
            '<div style="width:54px;height:40px;background:#1e293b;border-radius:6px;'
            'display:flex;align-items:center;justify-content:center;color:#475569;font-size:.7rem;">N/A</div>'
        )
    apercu_image.short_description = 'Image'

    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<div style="margin-top:8px;">'
                '<img src="{}" style="max-width:400px;max-height:220px;object-fit:cover;'
                'border-radius:10px;border:2px solid #3b82f6;"/>'
                '<p style="margin-top:6px;color:#94a3b8;font-size:.82rem;">Aperçu de l\'image actuelle</p>'
                '</div>',
                obj.image.url
            )
        return format_html('<p style="color:#94a3b8;font-size:.82rem;">Aucune image uploadée</p>')
    preview_image.short_description = 'Aperçu'

    def vues_badge(self, obj):
        return format_html(
            '<span style="background:#3b82f6;color:white;padding:2px 8px;border-radius:99px;font-size:.75rem;">'
            '👁 {}</span>', obj.vues
        )
    vues_badge.short_description = 'Vues'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'email', 'sujet', 'date', 'statut_lu')
    list_filter = ('lu',)
    readonly_fields = ('prenom', 'nom', 'email', 'sujet', 'message', 'date')
    actions = ['marquer_lu', 'marquer_non_lu']

    def statut_lu(self, obj):
        if obj.lu:
            return format_html('<span style="color:#22c55e;font-weight:700;">✔ Lu</span>')
        return format_html('<span style="color:#f59e0b;font-weight:700;">● Non lu</span>')
    statut_lu.short_description = 'Statut'

    def marquer_lu(self, request, queryset):
        queryset.update(lu=True)
    marquer_lu.short_description = 'Marquer comme lu'

    def marquer_non_lu(self, request, queryset):
        queryset.update(lu=False)
    marquer_non_lu.short_description = 'Marquer comme non lu'
