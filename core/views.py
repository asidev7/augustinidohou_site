from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .models import ReseauSocial, Competence, Experience, Formation, Service, Categorie, Article, Message


def _ctx_base():
    return {
        'reseaux':  ReseauSocial.objects.all(),
        'whatsapp': getattr(settings, 'WHATSAPP_NUMBER', ''),
        'whatsapp_secondary': getattr(settings, 'WHATSAPP_NUMBER_2', ''),
        'phone1':   getattr(settings, 'PHONE_1', ''),
        'phone2':   getattr(settings, 'PHONE_2', ''),
        'contact_email': getattr(settings, 'CONTACT_EMAIL', ''),
    }


def home(request):
    if request.method == 'POST':
        Message.objects.create(
            prenom=request.POST.get('prenom', ''),
            nom=request.POST.get('nom', ''),
            email=request.POST.get('email', ''),
            sujet=request.POST.get('sujet', ''),
            message=request.POST.get('message', ''),
        )
        messages.success(request, 'Message envoyé ! Je vous réponds sous 24h.')
        return redirect('home')

    cat_slug = request.GET.get('cat', '')
    articles_qs = Article.objects.filter(publie=True).select_related('categorie')
    if cat_slug:
        articles_qs = articles_qs.filter(categorie__slug=cat_slug)

    default_skills = [
        ('Linux RHEL / CentOS', 90, 'linux'),
        ('Ubuntu / Debian',     88, 'linux'),
        ('Bash Scripting',      85, 'linux'),
        ('Docker & Compose',    92, 'devops'),
        ('Kubernetes / K3s',    80, 'devops'),
        ('Ansible',             85, 'devops'),
        ('Jenkins / CI-CD',     78, 'devops'),
        ('Terraform',           72, 'devops'),
        ('Nginx / Apache',      82, 'reseau'),
        ('Réseau TCP/IP',       80, 'reseau'),
        ('Python',              75, 'dev'),
        ('Git & GitOps',        88, 'dev'),
    ]

    competences = list(Competence.objects.all())
    stack_icons = [
        {'icon': c.icone, 'title': c.nom}
        for c in competences if c.icone
    ][:8]

    if not stack_icons:
        stack_icons = [
            {'icon': 'fab fa-linux', 'title': 'Linux'},
            {'icon': 'fab fa-docker', 'title': 'Docker'},
            {'icon': 'fab fa-python', 'title': 'Python'},
            {'icon': 'fab fa-git-alt', 'title': 'Git'},
            {'icon': 'fab fa-aws', 'title': 'AWS'},
            {'icon': 'fas fa-cogs', 'title': 'Automation'},
        ]

    ctx = _ctx_base()
    ctx.update({
        'competences':    competences,
        'experiences':    Experience.objects.all(),
        'formations':     Formation.objects.all(),
        'services':       Service.objects.all(),
        'articles':       articles_qs[:6],
        'categories':     Categorie.objects.all(),
        'cat_slug':       cat_slug,
        'default_skills': default_skills,
        'stack_icons':    stack_icons,
    })
    return render(request, 'index.html', ctx)


def blog_list(request):
    cat_slug = request.GET.get('cat', '')
    articles_qs = Article.objects.filter(publie=True).select_related('categorie')
    categorie_active = None
    if cat_slug:
        articles_qs = articles_qs.filter(categorie__slug=cat_slug)
        categorie_active = Categorie.objects.filter(slug=cat_slug).first()

    ctx = _ctx_base()
    ctx.update({
        'articles':          articles_qs,
        'categories':        Categorie.objects.all(),
        'cat_slug':          cat_slug,
        'categorie_active':  categorie_active,
    })
    return render(request, 'blog_list.html', ctx)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, publie=True)
    article.incrementer_vues()
    article.refresh_from_db(fields=['vues'])

    articles_recents = Article.objects.filter(
        publie=True
    ).exclude(pk=article.pk).order_by('-date')[:4]

    keywords = [
        kw.strip() for kw in article.meta_keywords.split(',') if kw.strip()
    ]

    ctx = _ctx_base()
    ctx.update({
        'article':         article,
        'articles_recents': articles_recents,
        'keywords':        keywords,
    })
    return render(request, 'blog_detail.html', ctx)
