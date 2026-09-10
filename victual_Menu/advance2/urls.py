from django.urls import path
from . import views

app_name = 'advance2'

urlpatterns = [
    # 🎯 PROFESSIONAL RESTAURANT LINK ENDPOINT CORRIDOR
    # Maps directly to: http://127.0.0[restaurant-slug]/
    path('<slug:store_slug>/', views.professional_restaurant_view, name='restaurant_hub'),
]
