from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home, blog_list, article_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', home, name='home'),
    path('blog/', blog_list, name='blog_list'),
    path('blog/<slug:slug>/', article_detail, name='article_detail'),
]

# Servir media ET static en développement
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
