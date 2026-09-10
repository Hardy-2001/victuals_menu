from django.urls import path
from . import views

urlpatterns = [
    # 🏥 Master Hospital Web Showcase Route (e.g., /modern4/)
    path('<slug:slug>/', views.modern4_hospital_storefront_view, name='modern4_hospital_storefront'),

    # 📥 Active Patient Appointment Submission Transaction Receiver Link
    path('<slug:slug>/book-appointment/', views.modern4_submit_appointment, name='modern4_submit_appointment'),

    # 📥 Active Footer Contact Message Mailbox Submission Receiver Link
    path('<slug:slug>/submit-message/', views.modern4_submit_contact_message, name='modern4_submit_contact_message'),
]
