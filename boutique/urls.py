from django.urls import path
from . import views

urlpatterns = [
    path('',                         views.boutique_liste,    name='boutique_liste'),
    path('webhook/',                 views.boutique_webhook,  name='boutique_webhook'),
    path('succes/<int:commande_id>/', views.boutique_succes,  name='boutique_succes'),
    path('<slug:slug>/',             views.boutique_detail,   name='boutique_detail'),
    path('<slug:slug>/payer/',       views.boutique_checkout, name='boutique_checkout'),
]
