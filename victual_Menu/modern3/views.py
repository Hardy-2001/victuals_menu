
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    Modern3StoreFront, HospitalService, HospitalDepartment, MedicalDoctor,
    HospitalFAQ, HospitalTestimonial, HospitalGalleryImage, MedicalAppointment,
    HospitalContactMessage
)


def hospital_landing_profile(request, slug):
    """
    🏥 DYNAMIC HEALTHCARE TENANT LANDING MATRIX
    Fetches the profile metadata and all dynamic child sections
    matching this clinic's sub-slug layout cleanly.
    """
    # 🔍 Fetch the specific storefront; error out safely if it doesn't exist
    profile = get_object_or_404(Modern3StoreFront, tenant_identity__hospital_slug=slug)

    # 📂 Query individual sub-sections restricted strictly to this hospital tenant
    services = HospitalService.objects.filter(store=profile)
    departments = HospitalDepartment.objects.filter(store=profile)
    doctors = MedicalDoctor.objects.filter(store=profile)
    faqs = HospitalFAQ.objects.filter(store=profile)
    testimonials = HospitalTestimonial.objects.filter(store=profile)
    gallery = HospitalGalleryImage.objects.filter(store=profile)

    context = {
        'hospital_profile': profile,
        'hospital_services': services,
        'hospital_departments': departments,
        'hospital_doctors': doctors,
        'hospital_faqs': faqs,
        'hospital_testimonials': testimonials,
        'hospital_gallery': gallery,
    }
    return render(request, 'modern3/index.html', context)


def process_patient_appointment(request, slug):
    """
    📥 TRANSACTION ENGINE: LIVE APPOINTMENT BOOKING REGISTRY
    Saves incoming bookings directly inside the database grid layout
    and automatically dispatches alert notifications straight to the site owner!
    """
    if request.method == 'POST':
        profile = get_object_or_404(Modern3StoreFront, tenant_identity__hospital_slug=slug)

        # 📥 Capture text criteria inputs submitted from front-end form fields
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        department = request.POST.get('department')
        doctor = request.POST.get('doctor')
        message_text = request.POST.get('message', '')

        # 🚀 1. Database Entry Registry Log
        appointment = MedicalAppointment.objects.create(
            store=profile,
            patient_name=name,
            patient_email=email,
            patient_phone=phone,
            appointment_date=date,
            selected_department=department,
            selected_doctor=doctor,
            patient_message=message_text
        )

        # 📧 2. Automated Alert Dispatch Engine
        # Fetches the linked tenant owner user account profile email address dynamically
        owner_email = profile.tenant_identity.user.email
        if owner_email:
            try:
                subject = f"🚨 New Patient Booking Notification — {profile.tenant_identity.hospital_name}"
                body = (
                    f"Hello Administrator,\n\n"
                    f"A new patient has scheduled an appointment on your storefront platform loop.\n\n"
                    f"📋 PATIENT INTAKE SUMMARY DETAILS:\n"
                    f"▪️ Name: {name}\n"
                    f"▪️ Email: {email}\n"
                    f"▪️ Phone Line: {phone}\n"
                    f"▪️ Targeted Date: {date}\n"
                    f"▪️ Division Department: {department}\n"
                    f"▪️ Selected Specialist Practitioner: {doctor}\n"
                    f"▪️ Additional symptoms notes: {message_text}\n\n"
                    f"Please log into your operational portal control board dashboard to review or approve this slot."
                )
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [owner_email], fail_silently=True)
            except Exception:
                pass

        # 🏁 Add a specific alert tag identifier to pop confirmation cards right onto the screen glass
        messages.success(request, "Your medical appointment reservation request has been processed successfully!",
                         extra_tags='appointment')
        return redirect(f"/modern3/{slug}/#appointment")

    return redirect(f"/modern3/{slug}/")


def submit_quick_message(request, slug):
    """
    📥 MAILBOX BACKEND INTERFACE FEEDBACK VAULT
    Processes footers contact inquiries straight into target tenant message dashboards.
    """
    if request.method == 'POST':
        profile = get_object_or_404(Modern3StoreFront, tenant_identity__hospital_slug=slug)

        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        body = request.POST.get('message')

        # Save submission record natively inside the tenant's isolated repository box
        HospitalContactMessage.objects.create(
            store=profile,
            sender_name=name,
            sender_email=email,
            message_subject=subject,
            message_body=body
        )

        messages.success(request, "Your message has been filed and delivered to the medical desk safely!",
                         extra_tags='contact')
        return redirect(f"/modern3/{slug}/#contact")

    return redirect(f"/modern3/{slug}/")
