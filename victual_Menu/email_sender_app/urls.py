from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Public Frontend Email Capture Landing Page (e.g., clientbrand.corex.ng/)
    path('', views.email_sender_index_view, name='email_sender_index_view'),
    path('<slug:slug>/', views.email_sender_index_view, name='email_sender_index_view'),

    # ✉️ Admin-Triggered Dynamic Broadcast Dispatch Engine Link Hook
    path('broadcast/dispatch/<int:campaign_id>/', views.dispatch_broadcast_campaign, name='dispatch_broadcast_campaign'),
]
