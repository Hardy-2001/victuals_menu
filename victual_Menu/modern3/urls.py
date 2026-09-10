from django.urls import path
from . import views

urlpatterns = [
    # 🏥 Master Hospital Web Showcase Route (e.g., http://127.0.0)
    path('<slug:slug>/', views.hospital_landing_profile, name='hospital_profile'),

    # 📥 Active Patient Appointment Submission Transaction Receiver Link
    path('<slug:slug>/book-appointment/', views.process_patient_appointment, name='book_appointment'),

    # 📥 Active Footer Contact Message Mailbox Submission Receiver Link
    path('<slug:slug>/submit-message/', views.submit_quick_message, name='submit_message'),
]
