from django.db import models
from django.contrib.auth.models import User


# ==============================================================================
# 🔒 APP LEVEL SAAS TENANT CORE REGISTRY
# ==============================================================================

class Modern4SlugTenant(models.Model):
    """
    🔒 ISOLATED MODERN4 HOSPITAL IDENTITY VAULT
    Anchors the core tenant credentials, unique slugs, and assigned agents.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User Account")
    hospital_name = models.CharField(max_length=120, unique=True, verbose_name="Hospital Name")
    hospital_slug = models.SlugField(max_length=120, unique=True, help_text="e.g., hospital")

    # 👑 THE ANCHOR COLUMN: Permanently links this hospital registry to the onboarding field agent profile!
    assigned_agent = models.ForeignKey(
        'super_admin.AgentProfile',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='modern4_onboarded_hospitals',
        help_text="The field agent tracking this premium hospital profile registry"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        # 🟢 PERMISSION branding explicitly matches your app requirements:
        verbose_name = "modern4 SaaS Tenant"
        verbose_name_plural = "modern4 SaaS Tenants"

    def __str__(self):
        return f"{self.hospital_name} ({self.hospital_slug})"


# ==============================================================================
# 💎 VISUAL CONTROL DECK PARAMETERS CONFIGURATIONS
# ==============================================================================

class Modern4StoreFront(models.Model):
    """
    💎 PREMIUM HOSPITAL APP VISUAL CONTROL DECK FOR MODERN4
    Houses the top alert contacts, hero banners, statistical matrices, and layout titles.
    """
    tenant_identity = models.OneToOneField(
        Modern4SlugTenant,
        on_delete=models.CASCADE,
        related_name='hospital_profile',
        verbose_name="SaaS Identity Link",
        null=True,
        blank=True
    )

    # 📞 Top Alert Bar & Contact Nodes (Nigeria Style Default Fallbacks Built-in)
    hospital_email = models.EmailField(default="desk@corex.ng")
    emergency_phone_line = models.CharField(max_length=30, default="+234 (0) 800 227 3964")
    hospital_physical_address = models.CharField(max_length=255,
                                                 default="Plot 14, Broad Street, Lagos Island, Lagos, Nigeria")
    operating_hours = models.CharField(max_length=255, default="Mon - Sat : 08:00 AM - 08:00 PM")

    hospital_logo = models.ImageField(
        upload_to='modern4_hospital_logos/',
        blank=True,
        null=True,
        help_text="Upload a square aspect ratio branding logo icon to display next to the site name header text row"
    )

    # 🔗 Social Network Media Platform Handle Tracking Paths
    fb_url = models.URLField(blank=True, null=True, default="https://facebook.com")
    x_url = models.URLField(blank=True, null=True, default="https://x.com")
    linkedin_url = models.URLField(blank=True, null=True, default="https://linkedin.com")
    ig_url = models.URLField(blank=True, null=True, default="https://instagram.com")

    # 🎨 Main Hero Section Elements (Updated fields extracted from your HTML parts)
    hero_title = models.CharField(max_length=500, default="Good Health Is The Root Of All Happiness")
    carousel_img_1 = models.ImageField(upload_to='modern4_carousel/', blank=True, null=True)
    carousel_txt_1 = models.CharField(max_length=100, default="Cardiology")
    carousel_img_2 = models.ImageField(upload_to='modern4_carousel/', blank=True, null=True)
    carousel_txt_2 = models.CharField(max_length=100, default="Neurology")
    carousel_img_3 = models.ImageField(upload_to='modern4_carousel/', blank=True, null=True)
    carousel_txt_3 = models.CharField(max_length=100, default="Pulmonary")

    # 📋 About Section Framework Fields
    about_main_title = models.CharField(max_length=255, default="Why You Should Trust Us? Get to Know About Us!")
    about_description_primary = models.TextField(blank=True, null=True)
    about_description_secondary = models.TextField(blank=True, null=True)
    about_showcase_image_1 = models.ImageField(upload_to='modern4_hospital_about/', blank=True, null=True)
    about_showcase_image_2 = models.ImageField(upload_to='modern4_hospital_about/', blank=True, null=True)
    about_check_1 = models.CharField(max_length=255, default="Quality health care services")
    about_check_2 = models.CharField(max_length=255, default="Only Certified & Qualified Doctors")
    about_check_3 = models.CharField(max_length=255, default="Medical Research Professionals")
    about_button_text = models.CharField(max_length=100, default="Explore Services")
    about_button_url = models.CharField(max_length=255, default="#services")

    # 📘 Features Section Value Card Blocks
    feature_main_headline = models.CharField(max_length=200, default="Why Choose Our Care Center")
    feature_summary_text = models.TextField(blank=True, null=True)
    feat_card_1_title = models.CharField(max_length=100, default="Certified Doctors")
    feat_card_1_sub = models.CharField(max_length=100, default="Highly Experienced")
    feat_card_2_title = models.CharField(max_length=100, default="Quality Services")
    feat_card_2_sub = models.CharField(max_length=100, default="Premium High-End")
    feat_card_3_title = models.CharField(max_length=100, default="Consultation Links")
    feat_card_3_sub = models.CharField(max_length=100, default="Trusted & Secure")
    feat_card_4_title = models.CharField(max_length=100, default="Dedicated Support")
    feat_card_4_sub = models.CharField(max_length=100, default="24 Hours Emergency")
    feature_banner_img = models.ImageField(upload_to='modern4_features_panel/', blank=True, null=True)

    # 📊 Statistical Trust Social Counters
    count_doctors = models.IntegerField(default=45)
    count_staff = models.IntegerField(default=120)
    count_patients = models.IntegerField(default=15400)

    # 🗺️ Master Section Headline Control Text Labels
    services_section_title = models.CharField(max_length=255, default="Health Care Solutions & Specialties")
    team_section_title = models.CharField(max_length=255, default="Our Experienced Doctors")
    appointment_title = models.CharField(max_length=255, default="Make An Appointment To Visit Our Doctors")
    appointment_description = models.TextField(blank=True, null=True)
    testimonial_section_title = models.CharField(max_length=255, default="What Our Patients Say!")
    newsletter_subtext = models.CharField(max_length=255, default="Stay updated with medical infrastructure news.")

    initialized_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-initialized_at']
        # 🟢 PERMISSION branding explicitly matches your app requirements:
        verbose_name = "modern4 Hospital Store Profile"
        verbose_name_plural = "modern4 Hospital Store Profiles"

    # Backward compatibility template properties mapping rails
    @property
    def user(self): return self.tenant_identity.user

    @property
    def hospital_name(self): return self.tenant_identity.hospital_name

    @property
    def hospital_slug(self): return self.tenant_identity.hospital_slug

    def __str__(self):
        return f"{self.tenant_identity.hospital_name} — Modern4 Visual Deck"

# ==============================================================================
# 📁 REPEATING CHILD CONTENT GRIDS RELATIONSHIPS (MODERN4 APP SCOPE)
# ==============================================================================

class Modern4HospitalService(models.Model):
    """
    📁 HOSPITAL CARD SECTIONS ROWS LOOP FOR MODERN4
    Organizes medical care treatment nodes with custom font icon badges.
    """
    store = models.ForeignKey(Modern4StoreFront, on_delete=models.CASCADE, related_name='hospital_services')
    service_name = models.CharField(max_length=120, verbose_name="Service Title")
    service_description = models.TextField(verbose_name="Service Summary Paragraph")
    icon_choice = models.CharField(
        max_length=50,
        default="fa fa-heartbeat",
        help_text="Bootstrap/FontAwesome icon class name string (e.g., fa fa-heartbeat, fa fa-tooth, fa fa-brain)"
    )

    class Meta:
        verbose_name = "modern4 Hospital Service Offer"
        verbose_name_plural = "modern4 Hospital Service Offers"

    def __str__(self):
        return f"{self.service_name} — {self.store.tenant_identity.hospital_name}"


class Modern4MedicalDoctor(models.Model):
    """
    👨‍⚕️ HOSPITAL PRACTITIONERS & MEDICAL SPECIALISTS REGISTRY FOR MODERN4
    Pops clinician profiles right onto your front scroller framework cleanly.
    """
    store = models.ForeignKey(Modern4StoreFront, on_delete=models.CASCADE, related_name='hospital_doctors')
    doctor_name = models.CharField(max_length=120)
    medical_title = models.CharField(max_length=100, help_text="e.g., Chief Medical Officer, Consultant Cardiologist")
    profile_photo = models.ImageField(upload_to='modern4_hospital_doctors/', blank=True, null=True)

    # Social Network Profile Data Fields
    twitter_link = models.URLField(blank=True, null=True, default="https://twitter.com")
    facebook_link = models.URLField(blank=True, null=True, default="https://facebook.com")
    instagram_link = models.URLField(blank=True, null=True, default="https://instagram.com")

    class Meta:
        verbose_name = "modern4 Medical Team Doctor"
        verbose_name_plural = "modern4 Medical Team Doctors"

    def __str__(self):
        return f"{self.doctor_name} ({self.medical_title})"


class Modern4HospitalTestimonial(models.Model):
    """
    ⭐ PATIENT SUCCESS STORIES SLIDER VAULT FOR MODERN4
    Renders patient reviews, star metrics, and thumbnail profile photos.
    """
    store = models.ForeignKey(Modern4StoreFront, on_delete=models.CASCADE, related_name='hospital_testimonials')
    patient_name = models.CharField(max_length=120)
    patient_title_or_role = models.CharField(max_length=100, default="Patient", help_text="e.g., Recovered Patient, Local Client")
    review_text = models.TextField()
    patient_avatar = models.ImageField(upload_to='modern4_hospital_reviews/', blank=True, null=True)

    class Meta:
        verbose_name = "modern4 Patient Testimonial Story"
        verbose_name_plural = "modern4 Patient Testimonial Stories"

    def __str__(self):
        return f"Review by {self.patient_name}"


class Modern4MedicalAppointment(models.Model):
    """
    📥 PATIENT APPOINTMENT TRANSACTION TRACKER FOR MODERN4
    Captures patient booking metrics securely inside your database core.
    """
    store = models.ForeignKey(Modern4StoreFront, on_delete=models.CASCADE, related_name='hospital_appointments')
    patient_name = models.CharField(max_length=120)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=30)
    appointment_date = models.CharField(max_length=100, help_text="Date string text picked from form")
    appointment_time = models.CharField(max_length=100, help_text="Time block text segment slot")
    selected_doctor = models.CharField(max_length=120)
    patient_message = models.TextField(blank=True)

    is_reviewed = models.BooleanField(default=False, verbose_name="Processed / Approved")
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-logged_at']
        verbose_name = "modern4 Incoming Patient Appointment"
        verbose_name_plural = "modern4 Incoming Patient Appointments"

    def __str__(self):
        return f"Booking link for {self.patient_name} -> {self.selected_doctor}"


class Modern4HospitalContactMessage(models.Model):
    """
    📥 QUICK MESSAGE FEEDBACK LOOP MAILBOX FOR MODERN4
    Stores website footer submission forms directly into the database grid.
    """
    store = models.ForeignKey(Modern4StoreFront, on_delete=models.CASCADE, related_name='hospital_mailbox')
    sender_name = models.CharField(max_length=120)
    sender_email = models.EmailField()
    message_subject = models.CharField(max_length=200)
    message_body = models.TextField()

    is_read = models.BooleanField(default=False)
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-received_at']
        verbose_name = "modern4 Mailbox Feedback Message"
        verbose_name_plural = "modern4 Mailbox Feedback Messages"

    def __str__(self):
        return f"Msg: {self.sender_name} — Subj: {self.message_subject[:30]}"
