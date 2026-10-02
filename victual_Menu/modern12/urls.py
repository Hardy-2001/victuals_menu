from django.urls import path
from . import views

urlpatterns = [
    # 🏠 1. Core Base Salon Landing Endpoints (Accepts slugs under identical base name hooks!)
    path('', views.modern12_index_view, name='modern12_index_view'),
    path('<slug:slug>/', views.modern12_index_view, name='modern12_index_view'),

    # 📁 2. Sub-Page Grid Layout Endpoints (100% Dynamic Slug-Scoped Multi-Tenant Channels)
    path('<slug:slug>/about/', views.modern12_about_view, name='modern12_about_view'),
    path('<slug:slug>/services/', views.modern12_services_view, name='modern12_services_view'),
    path('<slug:slug>/work/', views.modern12_work_view, name='modern12_work_view'),
    path('<slug:slug>/blog/', views.modern12_blog_view, name='modern12_blog_view'),
    path('<slug:slug>/contact/', views.modern12_contact_view, name='modern12_contact_view'),

    # 🛍️ 3. Dynamic Cosmetics Retail Shop Catalogue Endpoint
    path('<slug:slug>/shop/', views.modern12_shop_view, name='modern12_shop_view'),

    # =========================================================================
    # 👑 THE ULTIMATE SHIELD: Matches your subdomains router middleware's exact fallback structure!
    # =========================================================================
    path('<slug:slug>/modern12/services/', views.modern12_services_view, name='modern12_services_middleware_fallback'),
    path('<slug:slug>/modern12/work/', views.modern12_work_view, name='modern12_work_middleware_fallback'),
    path('<slug:slug>/modern12/blog/', views.modern12_blog_view, name='modern12_blog_middleware_fallback'),
    path('<slug:slug>/modern12/contact/', views.modern12_contact_view, name='modern12_contact_middleware_fallback'),
    path('<slug:slug>/modern12/shop/', views.modern12_shop_view, name='modern12_shop_middleware_fallback'),
]
