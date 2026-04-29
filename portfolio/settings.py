from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-31-@qtd^4dfhj*wk%%sqk-56zuoxk42u^+tw&34n#*k$x%g(dw'

DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',
    'core',
    'boutique',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Porto-Novo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule', 'SpecialChar'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['CodeSnippet', 'Source'],
        ],
        'extraPlugins': 'codesnippet',
        'height': 400,
        'width': '100%',
    },
}

JAZZMIN_SETTINGS = {
    "site_title": "Portfolio Admin",
    "site_header": "IDOHOU Augustin",
    "site_brand": "Portfolio",
    "site_logo": None,
    "welcome_sign": "Bienvenue dans votre espace admin",
    "copyright": "IDOHOU Sande Augustin",
    "search_model": ["core.Article", "core.Message"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": [
        "core",
        "core.Article",
        "core.Message",
        "core.Service",
        "core.Experience",
        "core.Formation",
        "core.Competence",
        "core.ReseauSocial",
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "core.Article": "fas fa-file-alt",
        "core.Message": "fas fa-envelope",
        "core.Service": "fas fa-cogs",
        "core.Experience": "fas fa-briefcase",
        "core.Formation": "fas fa-graduation-cap",
        "core.Competence": "fas fa-chart-bar",
        "core.ReseauSocial": "fas fa-share-alt",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": "css/admin_custom.css",
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "language_chooser": False,
    "topmenu_links": [
        {"name": "Voir le site", "url": "/", "new_window": True, "icon": "fas fa-external-link-alt"},
        {"name": "Blog", "url": "/blog/", "new_window": True, "icon": "fas fa-rss"},
        {"name": "Boutique", "url": "/boutique/", "new_window": True, "icon": "fas fa-store"},
    ],
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

WHATSAPP_NUMBER   = '22901907768888'
WHATSAPP_NUMBER_2 = '22901687212144'
PHONE_1 = '+229 01 90 77 68 88'
PHONE_2 = '+229 01 68 72 12 14'

# FedaPay
import os
FEDAPAY_PUBLIC_KEY  = os.environ.get('FEDAPAY_PUBLIC_KEY',  'pk_live_9j19NkT-hUoX6CCVmqy_cifQ')
FEDAPAY_SECRET_KEY  = os.environ.get('FEDAPAY_SECRET_KEY',  'sk_live_BxxhszGS-nMOxnkFotI_lInC')
FEDAPAY_ENVIRONMENT = os.environ.get('FEDAPAY_ENVIRONMENT', 'live')
