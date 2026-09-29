from django.urls import path
from . import views

urlpatterns = [
    # 🏠 1. Core Base Salon Landing Endpoints (Accepts slugs under identical base name hooks!)
    path('', views.modern11_index_view, name='modern11_index_view'),
    path('<slug:slug>/', views.modern11_index_view, name='modern11_index_view'),

    # 📁 2. Sub-Page Grid Layout Endpoints (100% Dynamic Slug-Scoped Multi-Tenant Channels)
    path('<slug:slug>/about/', views.modern11_about_view, name='modern11_about_view'),
    path('<slug:slug>/services/', views.modern11_services_view, name='modern11_services_view'),
    path('<slug:slug>/work/', views.modern11_work_view, name='modern11_work_view'),
    path('<slug:slug>/blog/', views.modern11_blog_view, name='modern11_blog_view'),
    path('<slug:slug>/contact/', views.modern11_contact_view, name='modern11_contact_view'),

    # 🛍️ 3. Dynamic Cosmetics Retail Shop Catalogue Endpoint
    path('<slug:slug>/shop/', views.modern11_shop_view, name='modern11_shop_view'),

    # =========================================================================
    # 👑 THE ULTIMATE SHIELD: Matches your subdomains router middleware's exact fallback structure!
    # =========================================================================
    path('<slug:slug>/modern11/services/', views.modern11_services_view, name='modern11_services_middleware_fallback'),
    path('<slug:slug>/modern11/work/', views.modern11_work_view, name='modern11_work_middleware_fallback'),
    path('<slug:slug>/modern11/blog/', views.modern11_blog_view, name='modern11_blog_middleware_fallback'),
    path('<slug:slug>/modern11/contact/', views.modern11_contact_view, name='modern11_contact_middleware_fallback'),
    path('<slug:slug>/modern11/shop/', views.modern11_shop_view, name='modern11_shop_middleware_fallback'),
]
