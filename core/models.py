from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class ReseauSocial(models.Model):
    nom = models.CharField(max_length=50)
    url = models.URLField()
    icone = models.CharField(max_length=60, help_text='Classe FontAwesome ex: fab fa-github')
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['ordre']
        verbose_name = 'Réseau Social'
        verbose_name_plural = 'Réseaux Sociaux'

    def __str__(self):
        return self.nom


class Competence(models.Model):
    CATEGORIES = [
        ('linux',  'Linux & Sysadmin'),
        ('devops', 'DevOps & Cloud'),
        ('dev',    'Développement'),
        ('reseau', 'Réseau & Sécu'),
        ('autre',  'Autre'),
    ]
    nom = models.CharField(max_length=100)
    niveau = models.PositiveSmallIntegerField(default=80, help_text='0-100')
    categorie = models.CharField(max_length=20, choices=CATEGORIES, default='linux')
    icone = models.CharField(max_length=60, blank=True)
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['categorie', 'ordre']
        verbose_name = 'Compétence'
        verbose_name_plural = 'Compétences'

    def __str__(self):
        return self.nom


class Experience(models.Model):
    poste = models.CharField(max_length=150)
    entreprise = models.CharField(max_length=150)
    lieu = models.CharField(max_length=100, blank=True)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    en_cours = models.BooleanField(default=False)
    description = models.TextField()
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['ordre', '-date_debut']
        verbose_name = 'Expérience'
        verbose_name_plural = 'Expériences'

    def __str__(self):
        return f"{self.poste} @ {self.entreprise}"

    def periode(self):
        debut = self.date_debut.strftime('%b %Y')
        fin = "Présent" if self.en_cours else self.date_fin.strftime('%b %Y')
        return f"{debut} — {fin}"


class Formation(models.Model):
    diplome = models.CharField(max_length=200)
    etablissement = models.CharField(max_length=200)
    lieu = models.CharField(max_length=100, blank=True)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    en_cours = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['ordre', '-date_debut']
        verbose_name_plural = 'Formations'

    def __str__(self):
        return f"{self.diplome} — {self.etablissement}"

    def periode(self):
        debut = self.date_debut.strftime('%Y')
        fin = "Présent" if self.en_cours else self.date_fin.strftime('%Y')
        return f"{debut} — {fin}"


class Service(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    icone = models.CharField(max_length=60, default='fas fa-server')
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return self.titre


class Categorie(models.Model):
    nom = models.CharField(max_length=80)
    slug = models.SlugField(max_length=90, unique=True, blank=True)
    description = models.CharField(max_length=200, blank=True)
    icone = models.CharField(max_length=60, default='fas fa-tag', help_text='Classe FontAwesome')

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories Blog'
        ordering = ['nom']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    def nb_articles(self):
        return self.articles.filter(publie=True).count()


class Article(models.Model):
    titre = models.CharField(max_length=200, verbose_name='Titre')
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    resume = models.TextField(verbose_name='Résumé (affiché en liste)')
    contenu = RichTextUploadingField(verbose_name='Contenu complet', blank=True)
    categorie = models.ForeignKey(
        Categorie, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='articles', verbose_name='Catégorie'
    )
    image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name='Image principale')
    date = models.DateField(auto_now_add=True)
    date_modif = models.DateTimeField(auto_now=True)
    temps_lecture = models.PositiveSmallIntegerField(default=5, help_text='Minutes', verbose_name='Temps de lecture (min)')
    publie = models.BooleanField(default=True, verbose_name='Publié')
    vues = models.PositiveIntegerField(default=0, editable=False, verbose_name='Nombre de vues')

    # SEO
    meta_description = models.CharField(max_length=160, blank=True, verbose_name='Meta description (SEO, max 160 car.)')
    meta_keywords = models.CharField(max_length=255, blank=True, verbose_name='Mots-clés SEO (séparés par des virgules)')

    class Meta:
        ordering = ['-date']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titre)
            slug = base
            n = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        if not self.meta_description:
            self.meta_description = self.resume[:157] + '...' if len(self.resume) > 157 else self.resume
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        if not self.slug:
            return '/blog/'
        return reverse('article_detail', kwargs={'slug': self.slug})

    def incrementer_vues(self):
        Article.objects.filter(pk=self.pk).update(vues=models.F('vues') + 1)


class Message(models.Model):
    prenom = models.CharField(max_length=80)
    nom = models.CharField(max_length=80)
    email = models.EmailField()
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Messages'

    def __str__(self):
        return f"{self.prenom} {self.nom} — {self.sujet}"
