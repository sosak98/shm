from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('pagne/<int:pk>/', views.product_detail, name='product_detail'),
    path('panier/', views.panier, name='panier'),
    path('contact/', views.contact, name='contact'),
    # 📲 PWA : servis à la racine pour une portée '/'
    path('manifest.json', views.manifest_json, name='manifest'),
    path('sw.js', views.service_worker, name='sw'),
    # ⚡ Keep-Alive / Anti-sommeil
    path('health/', views.health_check, name='health'),
    path('ping/', views.health_check, name='ping'),
]
