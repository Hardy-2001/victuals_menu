from django.urls import path
from . import views

urlpatterns = [

    # Dynamic SaaS Home Menu
    path('<slug:restaurant_slug>/', views.online_menu, name='online_menu'),

    # Dynamic Isolated Tenant Feedback Channel Endpoint
    path('<slug:restaurant_slug>/submit-feedback/', views.submit_feedback, name='submit_feedback'),

    # Dynamic Isolated Tenant Checkout Sub-Page Endpoint
    path('<slug:restaurant_slug>/checkout/', views.checkout_summary, name='checkout_summary'),

    # Dynamic Product Detail Lookbook Sub-Page Endpoint
    path('<slug:restaurant_slug>/product/<int:product_id>/', views.product_detail, name='product_detail'),
]
