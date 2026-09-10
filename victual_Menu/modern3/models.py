from django.db import models
from django.contrib.auth.models import User


class Modern3SlugTenant(models.Model):
    """
    🔒 ISOLATED MODERN3 HOSPITAL IDENTITY VAULT
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
        related_name='modern3_onboarded_hospitals',
        help_text="The field agent tracking this premium hospital profile registry"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Modern3 SaaS Tenant"
        verbose_name_plural = "Modern3 SaaS Tenants"

    def __str__(self):
        return f"{self.hospital_name} ({self.hospital_slug})"


class Modern3StoreFront(models.Model):
    """
    💎 PREMIUM HOSPITAL APP VISUAL CONTROL DECK
    Houses the top alert contacts, hero banners, statistical matrices, and map details.
    """
    tenant_identity = models.OneToOneField(
        Modern3SlugTenant,
        on_delete=models.CASCADE,
        related_name='hospital_profile',
        verbose_name="SaaS Identity Link",
        null=True,
        blank=True
    )

    # 📞 Top Alert Bar & Contact Nodes
    hospital_email = models.EmailField(default="contact@example.com")
    emergency_phone_line = models.CharField(max_length=30, default="+1 5589 55488 55")
    # 🎯 ADD THIS FIELD INSIDE YOUR Modern3StoreFront CLASS IN modern3/models.py:

    hospital_logo = models.ImageField(
        upload_to='hospital_logos/',
        blank=True,
        null=True,
        help_text="Upload a square aspect ratio branding logo icon to display next to the site name header text row"
    )

    # 🎨 Main Hero Section Elements
    hero_title = models.CharField(max_length=150, default="WELCOME TO MEDILAB")
    hero_sub_headline = models.TextField(default="Providing world-class comprehensive medical care configurations.")

    # 🎯 ADD THIS FIELD INSIDE YOUR Modern3StoreFront CLASS IN modern3/models.py:

    hero_background_image = models.ImageField(
        upload_to='hospital_hero_bg/',
        blank=True,
        null=True,
        help_text="Upload a high-resolution ambient background graphic picture for your main landing section"
    )

    # 📘 Blue "Why Choose Us" Featured Card Blocks
    why_choose_us_headline = models.CharField(max_length=200, default="Why Choose Medilab?")
    why_choose_us_body_text = models.TextField(default="Brief summary detailing medical care excellence parameters.")
    value_card_one_title = models.CharField(max_length=100, default="Corporis voluptates")
    value_card_one_body = models.TextField(default="Ullamco laboris nisi ut aliquip ex ea commodo consequat.")
    value_card_two_title = models.CharField(max_length=100, default="Ullamco laboris")
    value_card_two_body = models.TextField(default="Ullamco laboris nisi ut aliquip ex ea commodo consequat.")
    value_card_three_title = models.CharField(max_length=100, default="Labore consequatur")
    value_card_three_body = models.TextField(default="Ullamco laboris nisi ut aliquip ex ea commodo consequat.")

    # 🎬 About Section & YouTube Media Handles
    about_main_description = models.TextField(default="Detailed healthcare facility history or manifesto block.")
    about_video_url = models.URLField(default="https://youtube.com", help_text="Hospital video tour clip link")
    about_showcase_image = models.ImageField(upload_to='hospital_about/', blank=True, null=True)

    # 📊 Statistical Trust Social Counters
    count_doctors = models.IntegerField(default=85)
    count_departments = models.IntegerField(default=18)
    count_research_labs = models.IntegerField(default=12)
    count_awards = models.IntegerField(default=150)

    # 🗺️ Contact Map Section Parameters
    contact_headline = models.CharField(max_length=150, default="Contact")
    contact_description = models.TextField(default="Necessitatibus eius consequatur ex aliquid fuga eum quidem sint.")
    google_maps_embed_url = models.TextField(
        default="https://google.com...",
        help_text="Paste raw Google Maps iframe source URL link string"
    )
    hospital_physical_address = models.CharField(max_length=255, default="A108 Adam Street, New York, NY 535022")

    initialized_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-initialized_at']
        verbose_name = "Hospital Store Profile"
        verbose_name_plural = "Hospital Store Profiles"

    # Backward compatibility mappings
    @property
    def user(self): return self.tenant_identity.user

    @property
    def hospital_name(self): return self.tenant_identity.hospital_name

    @property
    def hospital_slug(self): return self.tenant_identity.hospital_slug

    def __str__(self):
        return f"{self.tenant_identity.hospital_name} — Visual Deck"


class HospitalService(models.Model):
    """
    📁 HOSPITAL CARD SECTIONS ROWS LOOP
    Organizes medical care treatment nodes with custom font icon badges.
    """
    store = models.ForeignKey(Modern3StoreFront, on_delete=models.CASCADE, related_name='hospital_services')
    service_name = models.CharField(max_length=120, verbose_name="Service Title")
    service_description = models.TextField(verbose_name="Service Summary Paragraph")
    icon_choice = models.CharField(
        max_length=50,
        default="bi-heart-pulse",
        help_text="Bootstrap icon class name string (e.g., bi-heart-pulse, bi-pills, bi-stethoscope)"
    )

    class Meta:
        verbose_name = "Hospital Service Offer"
        verbose_name_plural = "Hospital Service Offers"

    def __str__(self):
        return f"{self.service_name} — {self.store.hospital_name}"


class HospitalDepartment(models.Model):
    """
    📁 INTERACTIVE LEFT-MENU TAB SELECTORS MULTI-BAR
    Handles specific internal medical tabs (e.g., Cardiology, Neurology, Pediatrics).
    """
    store = models.ForeignKey(Modern3StoreFront, on_delete=models.CASCADE, related_name='hospital_departments')
    name = models.CharField(max_length=100, verbose_name="Tab Menu Title")
    headline = models.CharField(max_length=180, verbose_name="Content Primary Header Row")
    description = models.TextField(verbose_name="Detailed Summary Context Text")
    showcase_photo = models.ImageField(upload_to='hospital_departments/', blank=True, null=True)

    class Meta:
        verbose_name = "Hospital Department Tab"
        verbose_name_plural = "Hospital Department Tabs"

    def __str__(self):
        return f"{self.name} — {self.store.hospital_name}"


class MedicalDoctor(models.Model):
    """
    👨‍⚕️ HOSPITAL PRACTITIONERS & MEDICAL SPECIALISTS REGISTRY
    Pops clinician profiles right onto your front scroller framework cleanly.
    """
    store = models.ForeignKey(Modern3StoreFront, on_delete=models.CASCADE, related_name='hospital_doctors')
    doctor_name = models.CharField(max_length=120)
    medical_title = models.CharField(max_length=100, help_text="e.g., Chief Medical Officer, Anesthesiologist")
    doctor_biography = models.TextField(blank=True, help_text="Brief summary paragraph statement")
    profile_photo = models.ImageField(upload_to='hospital_doctors/', blank=True, null=True)

    # Social Network Profile Data Fields
    twitter_link = models.URLField(blank=True, null=True, default="https://twitter.com")
    facebook_link = models.URLField(blank=True, null=True, default="https://facebook.com")
    instagram_link = models.URLField(blank=True, null=True, default="https://instagram.com")
    linkedin_link = models.URLField(blank=True, null=True, default="https://linkedin.com")

    class Meta:
        verbose_name = "Medical Team Doctor"
        verbose_name_plural = "Medical Team Doctors"

    def __str__(self):
        return f"{self.doctor_name} ({self.medical_title})"


class HospitalFAQ(models.Model):
    """
    💬 INTERACTIVE ACCORDION DROP-DOWN QUESTION SLIDER BLOCK
    Handles frequently asked question cards natively without hardcoded layouts.
    """
    store = models.ForeignKey(Modern3StoreFront, on_delete=models.CASCADE, related_name='hospital_faqs')
    question_text = models.CharField(max_length=255)
    answer_text = models.TextField()

    class Meta:
        verbose_name = "Hospital FAQ Drawer"
        verbose_name_plural = "Hospital FAQ Drawers"

    def __str__(self):
        return f"FAQ: {self.question_text[:40]}..."


class HospitalTestimonial(models.Model):
    """
    ⭐ PATIENT SUCCESS STORIES SLIDER VAULT
    Renders patient reviews, star metrics, and thumbnail profile photos.
    """
    store = models.ForeignKey(Modern3StoreFront, on_delete=models.CASCADE, related_name='hospital_testimonials')
    patient_name = models.CharField(max_length=120)
    patient_title_or_role = models.CharField(max_length=100, default="Patient",
                                             help_text="e.g., Recovered Patient, Local Client")
    rating_stars = models.IntegerField(default=5, help_text="Enter number score from 1 to 5")
    review_text = models.TextField()
    patient_avatar = models.ImageField(upload_to='hospital_reviews/', blank=True, null=True)

    class Meta:
        verbose_name = "Patient Testimonial Story"
        verbose_name_plural = "Patient Testimonial Stories"

    def __str__(self):
        return f"Review by {self.patient_name}"


class HospitalGalleryImage(models.Model):
    """
    📸 CLINICAL FACILITIES WIDE GRID LIGHTBOX LOOP
    Stores crisp facility layout portfolio pictures for display.
    """
    store = models.ForeignKey(Modern3StoreFront, on_delete=models.CASCADE, related_name='hospital_gallery')
    gallery_photo = models.ImageField(upload_to='hospital_gallery/')
    image_caption = models.CharField(max_length=150, blank=True, null=True, help_text="Short title popup name label")

    class Meta:
        verbose_name = "Hospital Gallery Image"
        verbose_name_plural = "Hospital Gallery Images"

    def __str__(self):
        return f"Gallery Slot #{self.id} — {self.store.hospital_name}"


class MedicalAppointment(models.Model):
    """
    📥 PATIENT APPOINTMENT TRANSACTION TRACKER
    Captures patient booking metrics securely inside your database core.
    """
    store = models.ForeignKey(Modern3StoreFront, on_delete=models.CASCADE, related_name='hospital_appointments')
    patient_name = models.CharField(max_length=120)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=30)
    appointment_date = models.CharField(max_length=100,
                                        help_text="Date or text string from the calendar picker template link")
    selected_department = models.CharField(max_length=120)
    selected_doctor = models.CharField(max_length=120)
    patient_message = models.TextField(blank=True)

    is_reviewed = models.BooleanField(default=False, verbose_name="Processed / Approved")
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-logged_at']
        verbose_name = "Incoming Patient Appointment"
        verbose_name_plural = "Incoming Patient Appointments"

    def __str__(self):
        return f"Booking: {self.patient_name} -> {self.selected_doctor}"


class HospitalContactMessage(models.Model):
    """
    📥 QUICK MESSAGE FEEDBACK LOOP MAILBOX
    Stores website footer submission forms directly into the database grid.
    """
    store = models.ForeignKey(Modern3StoreFront, on_delete=models.CASCADE, related_name='hospital_mailbox')
    sender_name = models.CharField(max_length=120)
    sender_email = models.EmailField()
    message_subject = models.CharField(max_length=200)
    message_body = models.TextField()

    is_read = models.BooleanField(default=False)
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-received_at']
        verbose_name = "Mailbox Feedback Message"
        verbose_name_plural = "Mailbox Feedback Messages"

    def __str__(self):
        return f"Msg: {self.sender_name} — Subj: {self.message_subject[:30]}"
