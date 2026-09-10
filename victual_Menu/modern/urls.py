from django.urls import path
from . import views

app_name = 'modern'

urlpatterns = [
    path('<slug:store_slug>/', views.modern_store_front_view, name='store_front_hub'),

    # 🎯 NEW: ABOUT US STANDALONE INFORMATION CORRIDOR LINK
    # Maps directly to: http://127.0.0[store-slug]/about/
    path('<slug:store_slug>/about/', views.modern_store_about_view, name='store_about_hub'),

    path('<slug:store_slug>/product/<int:product_id>/', views.modern_product_detail_view, name='product_detail_hub'),
]

