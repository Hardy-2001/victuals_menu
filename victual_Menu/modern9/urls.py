from django.urls import path
from . import views

app_name = 'modern9'

urlpatterns = [
    path('<slug:slug>/', views.index_view, name='storefront_with_slug'),
    path('<slug:slug>/shop/', views.shop_view, name='shop'),
    path('<slug:slug>/product/<int:pk>/', views.single_product_view, name='single_product_page'),
    path('<slug:slug>/cart/', views.cart_view, name='cart'),
    path('<slug:slug>/subscribe/', views.subscribe_newsletter_view, name='subscribe'),
]
