from django.urls import path
from . import views

urlpatterns = [
    # 🏠 1. Core Base Landing Endpoints (Combined to accept slug under the identical base name!)
    path('', views.modern10_index_view, name='modern10_index_view'),
    path('<slug:slug>/', views.modern10_index_view, name='modern10_index_view'),

    # 📁 2. Sub-Page Grid Layout Endpoints (Slug-Scoped Multi-Tenant Channels)
    path('<slug:slug>/cars/', views.modern10_car_view, name='modern10_car_view'),
    path('<slug:slug>/about/', views.modern10_about_view, name='modern10_about_view'),
    path('<slug:slug>/blog/', views.modern10_blog_view, name='modern10_blog_view'),
    path('<slug:slug>/contact/', views.modern10_contact_view, name='modern10_contact_view'),

    # 📥 3. Actions & Base Details Product Endpoints
    path('subscribe/', views.modern10_submit_newsletter, name='modern10_subscribe'),
    path('<slug:slug>/cars/<int:pk>/', views.modern10_car_details_view, name='modern10_car_details_view'),
    path('<slug:slug>/blog/<int:pk>/', views.modern10_blog_details_view, name='modern10_blog_details_view'),

    # 🟢 4. THE ULTIMATE SHIELD: Matches your subdomains router middleware's exact fallback structure!
    path('<slug:slug>/modern10/cars/<int:pk>/', views.modern10_car_details_view, name='modern10_car_details_middleware_fallback'),
    path('<slug:slug>/modern10/blog/<int:pk>/', views.modern10_blog_details_view, name='modern10_blog_details_middleware_fallback'),
]
