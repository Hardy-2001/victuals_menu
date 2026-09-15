from django.urls import path
from . import views

app_name = 'modern8'

urlpatterns = [
    # 🏠 1. Core Base Landing Endpoints
    path('', views.modern8_furniture_storefront_view, name='storefront'),
    path('<slug:slug>/', views.modern8_furniture_storefront_view, name='storefront_with_slug'),

    # 📁 2. Sub-Page Grid Layout Endpoints
    path('<slug:slug>/shop/', views.modern8_shop_view, name='shop'),
    path('<slug:slug>/about/', views.modern8_about_view, name='about'),
    path('<slug:slug>/services/', views.modern8_services_view, name='services'),
    path('<slug:slug>/blog/', views.modern8_blog_view, name='blog'),
    path('<slug:slug>/contact/', views.modern8_contact_view, name='contact'),
    path('<slug:slug>/cart/', views.modern8_cart_view, name='cart'),

    # 📥 3. Actions & Base Details Endpoints
    path('subscribe/', views.modern8_submit_newsletter, name='subscribe'),
    path('product/<int:pk>/', views.modern8_furniture_detail_view, name='product_detail'),

    # 🟢 4. THE ULTIMATE SHIELD: Matches your middleware's exact path structure!
    path('<slug:slug>/modern8/product/<int:pk>/', views.modern8_furniture_detail_view, name='product_detail_middleware_fallback'),
]
