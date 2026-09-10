from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

 # 🎯 Inherits your platform master subdomain identity tracker loop

from .models import (
    Modern4SlugTenant,
    Modern4StoreFront,
    Modern4HospitalService,
    Modern4MedicalDoctor,
    Modern4HospitalTestimonial,
    Modern4MedicalAppointment,
    Modern4HospitalContactMessage
)


def modern4_hospital_storefront_view(request, slug=None):
    tenant_slug = getattr(request, 'tenant_slug_token', slug)

    # 🧬 2. Look up the matching multi-tenant identity string inside your modern4 app registry
    active_slug_record = get_object_or_404(Modern4SlugTenant, hospital_slug__iexact=tenant_slug)

    # 🧬 3. Query all clinical profile configurations matching this specific visual store block
    platform_config = Modern4StoreFront.objects.filter(tenant_identity=active_slug_record).first()

    # Safety Check: If profile is completely blank, fetch a clean fallback baseline record framework
    if not platform_config:
        platform_config = Modern4StoreFront.objects.create(tenant_identity=active_slug_record)

    hospital_services = Modern4HospitalService.objects.filter(store=platform_config)
    hospital_doctors = Modern4MedicalDoctor.objects.filter(store=platform_config)
    hospital_testimonials = Modern4HospitalTestimonial.objects.filter(store=platform_config)

    # Pack the database entries neatly into your context dictionary engine
    context = {
        'active_tenant': active_slug_record,
        'platform_config': platform_config,
        'hospital_services': hospital_services,
        'hospital_doctors': hospital_doctors,
        'hospital_testimonials': hospital_testimonials,
    }

    return render(request, 'modern4/index.html', context)



def modern4_submit_appointment(request, slug=None):
    if request.method == "POST":
        tenant_slug = getattr(request, 'tenant_slug_token', slug)
        active_slug_record = get_object_or_404(Modern4SlugTenant, hospital_slug__iexact=tenant_slug)
        platform_config = get_object_or_404(Modern4StoreFront, tenant_identity=active_slug_record)

        # 📥 Extract data tokens from your localized form inputs
        patient_name = request.POST.get('patient_name')
        patient_email = request.POST.get('patient_email')
        patient_phone = request.POST.get('patient_phone')
        selected_doctor_id = request.POST.get('target_doctor')
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        patient_message = request.POST.get('patient_notes')

        # Fetch the selected doctor's name string token cleanly for historical archives
        try:
            doctor_record = Modern4MedicalDoctor.objects.get(id=selected_doctor_id, store=platform_config)
            target_doctor_name = f"{doctor_record.doctor_name} ({doctor_record.medical_title})"
        except (Modern4MedicalDoctor.DoesNotExist, ValueError):
            target_doctor_name = "On-Duty Medical Practitioner Desk"

        # 🚀 TRANSACTION MATRIX ASSEMBLY: Write a fresh appointment row to your database table safely
        Modern4MedicalAppointment.objects.create(
            store=platform_config,
            patient_name=patient_name,
            patient_email=patient_email,
            patient_phone=patient_phone,
            appointment_date=booking_date,
            appointment_time=booking_time,
            selected_doctor=target_doctor_name,
            patient_message=patient_message
        )

        # Display a premium success banner message on the glass viewport
        messages.success(request, f"Success! Appointment request for {patient_name} submitted safely.")

        # Bounce the browser path cleanly right back onto your active merchant subdomain landing
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect('/')


def modern4_submit_contact_message(request, slug=None):
    if request.method == "POST":
        tenant_slug = getattr(request, 'tenant_slug_token', slug)
        active_slug_record = get_object_or_404(Modern4SlugTenant, hospital_slug__iexact=tenant_slug)
        platform_config = get_object_or_404(Modern4StoreFront, tenant_identity=active_slug_record)

        sender_name = request.POST.get('name')
        sender_email = request.POST.get('email')
        message_subject = request.POST.get('subject', 'General Health Care Inquiry')
        message_body = request.POST.get('message')

        # 🚀 Write input metrics into your custom contact mailbox row layout track
        Modern4HospitalContactMessage.objects.create(
            store=platform_config,
            sender_name=sender_name,
            sender_email=sender_email,
            message_subject=message_subject,
            message_body=message_body
        )

        messages.success(request,
                         f"Thank you {sender_name}, your message has been transmitted safely to the clinical desk.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect('/')
