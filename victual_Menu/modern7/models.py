from django.db import models
from django.contrib.auth.models import User


# ==============================================================================
# 🔒 APPS REGISTRY SECTOR: MULTI-TENANT INSTITUTION ENGINE
# ==============================================================================

class Modern7SchoolTenant(models.Model):
    """
    🔒 MULTI-TENANT INSTITUTION ENGINE FOR MODERN7
    Isolates student logins, university settings, and course assets
    by sharding data through unique school path slices.
    """
    # 👑 OWNER ACCOUNT CHANNEL: Links the primary merchant or school administrator
    owner_account = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="School Administrator Account",
        related_name="modern7_schools"
    )

    # 🏫 IDENTIFICATION STRINGS
    school_name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Institution Name",
        help_text="e.g., Apex Tech University, Lagos Coding Academy"
    )
    slug_path = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name="Unique School URL Slug",
        help_text="The URL path text. e.g., 'apex-tech' or 'lca' (all lowercase)"
    )

    # 🛡️ SYSTEM SUPER-ADMIN CONTROL: Links back to your global management workspace agents
    onboarding_agent = models.ForeignKey(
        'super_admin.AgentProfile',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='modern7_onboarded_schools',
        help_text="The field agent tracking this custom campus account profile history"
    )

    is_active_node = models.BooleanField(
        default=True,
        verbose_name="Operational Status Switch",
        help_text="Turn off to instantly lock down or suspend this entire school tenant website."
    )

    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-registered_at']
        verbose_name = "modern7 School Tenant"
        verbose_name_plural = "modern7 School Tenants"

    def __str__(self):
        return f"{self.school_name} [/{self.slug_path}]"


# ==============================================================================
# 🎨 BRAND DESIGN SECTOR: DYNAMIC VISUAL SETTINGS DECK
# ==============================================================================

class Modern7PlatformConfigDeck(models.Model):
    """
    🎨 CAMPUS SETTINGS VISUAL CONTROL DECK FOR MODERN7
    Stores unique school text lines, layout metrics counters,
    map iframe embed codes, and uploaded graphic assets safely.
    """
    # 🔗 THE ANCHOR KEY: Links this look deck back to its primary parent school tenant
    tenant_link = models.OneToOneField(
        Modern7SchoolTenant,
        on_delete=models.CASCADE,
        related_name='visual_config',
        verbose_name="School Profile Anchor"
    )

    # 🏢 BRAND IDENTITY SLOTS
    institution_name = models.CharField(max_length=200, default="Eduleb Academy", verbose_name="Public Branding Name")
    brand_logo = models.ImageField(upload_to='modern7/logos/', blank=True, null=True, verbose_name="Navbar Brand Logo")
    footer_summary_text = models.TextField(
        default="Premium educational multi-tenant learning framework dedicated to structuring high-value conceptual mastery modules.",
        verbose_name="Footer Short Bio Paragraph"
    )

    # 📞 CAMPUS COORDINATES & CONTACT CHANNELS
    support_phone = models.CharField(max_length=40, default="+234 700 900 8888", verbose_name="Direct Phone Hotline")
    whatsapp_number = models.CharField(max_length=40, default="2347009008888",
                                       verbose_name="WhatsApp Business Digit Tracker (No spaces/plus)")
    support_email = models.EmailField(default="registrar@campus-node.edu.ng", verbose_name="Public Admissions Mailbox")
    office_address = models.TextField(default="Block 14, Admiralty Way, Lekki Phase 1, Lagos, Nigeria",
                                      verbose_name="Physical Facility Address")
    google_map_embed_iframe = models.TextField(
        blank=True,
        null=True,
        verbose_name="Google Map Embed Code (Iframe script)",
        help_text="Paste your direct Google Maps share iframe tag node row block safely here."
    )

    # 🚀 HERO COCKPIT PANEL LAYOUT STRINGS
    hero_tagline_accent = models.CharField(max_length=100, default="Smart Study",
                                           verbose_name="Hero Tagline Callout Accent")
    hero_main_title = models.CharField(max_length=255, default="Where Knowledge Meets the Web",
                                       verbose_name="Hero Typography Main Title")
    hero_description_text = models.TextField(
        default="We offer a brand new approach to the most basic learning paradigms. Choose from a wide range of learning options and gain new skills!",
        verbose_name="Hero Content Overview text")
    hero_background = models.ImageField(upload_to='modern7/hero/', blank=True, null=True,
                                        verbose_name="Landing Cockpit Background Frame Image")
    hero_side_illustration = models.ImageField(upload_to='modern7/hero/', blank=True, null=True,
                                               verbose_name="Hero Right Side Illustration Graphic Banner")

    # 📊 REAL-TIME VALUE FEATURE indicator fields
    count_active_students = models.CharField(max_length=30, default="4,500+",
                                             verbose_name="Metrics Tracker: Student Count")
    count_online_courses = models.CharField(max_length=30, default="134",
                                            verbose_name="Metrics Tracker: Class Total Count")
    count_academic_programs = models.CharField(max_length=30, default="299",
                                               verbose_name="Metrics Tracker: Programs Total Count")
    count_certified_students = models.CharField(max_length=30, default="684",
                                                verbose_name="Metrics Tracker: Certified Alumni Count")
    count_enrolled_students = models.CharField(max_length=30, default="941",
                                               verbose_name="Metrics Tracker: Total Lifetime Registrations")

    # 🏢 VALUE PROPOSITION HEADLINES
    features_title = models.CharField(max_length=255, default="Start your journey With us",
                                      verbose_name="Journey Matrix Section Heading")
    features_summary = models.TextField(
        default="We offer a brand new approach to the most basic learning paradigms. Choose from a wide range of learning options and gain new skills!",
        verbose_name="Journey Section Summary Text Copy")

    # Value features text slots
    feat_one_title = models.CharField(max_length=150, default="Expert <br />Teachers",
                                      verbose_name="Feature 1 Typography Title")
    feat_one_desc = models.TextField(
        default="Lorem ipsum dolor sit amet, consectetur notted adipisicing elit ut labore.",
        verbose_name="Feature 1 description info text")
    feat_two_title = models.CharField(max_length=150, default="Quality <br />Education",
                                      verbose_name="Feature 2 Typography Title")
    feat_two_desc = models.TextField(
        default="Lorem ipsum dolor sit amet, consectetur notted adipisicing elit ut labore.",
        verbose_name="Feature 2 description info text")
    feat_three_title = models.CharField(max_length=150, default="Remote <br />Learning",
                                        verbose_name="Feature 3 Typography Title")
    feat_three_desc = models.TextField(
        default="Lorem ipsum dolor sit amet, consectetur notted adipisicing elit ut labore.",
        verbose_name="Feature 3 description info text")
    feat_four_title = models.CharField(max_length=150, default="Life Time <br />Support",
                                       verbose_name="Feature 4 Typography Title")
    feat_four_desc = models.TextField(
        default="Lorem ipsum dolor sit amet, consectetur notted adipisicing elit ut labore.",
        verbose_name="Feature 4 description info text")

    # 🏙️ ABOUT US SECTION CONTENT METRICS OVERVIEWS
    about_illustration = models.ImageField(upload_to='modern7/about/', blank=True, null=True,
                                           verbose_name="About Panel Presentation Artwork Graphic")
    about_headline_title = models.CharField(max_length=255,
                                            default="We Are Providing The Online Course In Global World",
                                            verbose_name="About Section Title Typography Header")
    about_description_one = models.TextField(
        default="We offer a brand new approach to the most basic learning paradigms. Choose from a wide range of learning options and gain new skills!",
        verbose_name="About Summary Description Column 1")
    about_description_two = models.TextField(
        default="Our multi-tenant school parameters ensure professional-grade operational integrity at absolute zero wait system lag times.",
        verbose_name="About Summary Description Column 2")
    about_bullet_one = models.CharField(max_length=255, default="Get access to <b>12,000+</b> of our top courses",
                                        verbose_name="About Bullet Highlight line 1")
    about_bullet_two = models.CharField(max_length=255,
                                        default="Popular topic to learn now in our online courses for student",
                                        verbose_name="About Bullet Highlight line 2")
    about_bullet_three = models.CharField(max_length=255, default="Find the right instructor for you",
                                          verbose_name="About Bullet Highlight line 3")

    # 🛡️ THE EXTRA CAROUSEL SOCIALS STRINGS OVERLAYS
    twitter_x_url = models.URLField(default="https://x.com", verbose_name="X / Twitter Tracking Account Link")
    facebook_url = models.URLField(default="https://facebook.com", verbose_name="Facebook Tracking Account Link")
    instagram_url = models.URLField(default="https://instagram.com", verbose_name="Instagram Tracking Account Link")
    linkedin_url = models.URLField(default="https://linkedin.com", verbose_name="LinkedIn Tracking Account Link")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "modern7 Custom View Configuration"
        verbose_name_plural = "modern7 Custom View Configurations"

    def __str__(self):
        return f"Config Deck Config Node — {self.tenant_link.school_name}"


# ==============================================================================
# 📂 ACADEMIC ARCHITECTURE: CATEGORIES & FACULTY INSTRUCTOR REGS
# ==============================================================================

class Modern7CourseCategory(models.Model):
    """
    📂 DYNAMIC COURSE BUCKETS PER SCHOOL
    Allows individual campus tenants to customize their learning tracks
    and group lecture classes cleanly into filter catalogs.
    """
    school_tenant = models.ForeignKey(
        Modern7SchoolTenant,
        on_delete=models.CASCADE,
        related_name="custom_categories",
        verbose_name="School Context Anchor"
    )
    category_name = models.CharField(max_length=100, verbose_name="Category Group Name",
                                     help_text="e.g., Software Engineering, Digital Marketing")
    category_slug = models.SlugField(max_length=120, verbose_name="Filter URL Slug Token",
                                     help_text="e.g., 'software-eng' or 'marketing'")
    category_icon = models.ImageField(upload_to="modern7/categories/", blank=True, null=True,
                                      verbose_name="Small Dynamic Roster Icon Graphic")

    class Meta:
        unique_together = ('school_tenant', 'category_slug')
        verbose_name = "modern7 Course Category"
        verbose_name_plural = "modern7 Course Categories"

    def __str__(self):
        return f"{self.category_name} ({self.school_tenant.school_name})"


class Modern7FacultyInstructor(models.Model):
    """
    👨‍🏫 CLASS INSTRUCTOR BIOGRAPHY ROSTER MODEL
    Houses teacher profiles, bio portfolios, student counters, and social channel networks.
    """
    school_tenant = models.ForeignKey(
        Modern7SchoolTenant,
        on_delete=models.CASCADE,
        related_name="campus_instructors",
        verbose_name="School Context Anchor"
    )
    full_name = models.CharField(max_length=150, verbose_name="Instructor Full Name")
    professional_title = models.CharField(max_length=150, default="Senior Web Lecturer",
                                          verbose_name="Faculty Professional Title Designation")
    profile_avatar = models.ImageField(upload_to="modern7/instructors/", blank=True, null=True,
                                       verbose_name="Teacher Profile Card Portrait Picture")
    biography_summary = models.TextField(verbose_name="Teacher Short Bio Resume Profile")

    # Statistical counters on individual card sheets
    count_courses_text = models.CharField(max_length=50, default="04 Courses",
                                          verbose_name="Teacher Card Metric: Active Classes Count")
    count_students_text = models.CharField(max_length=50, default="27 Students",
                                           verbose_name="Teacher Card Metric: Active Student Pool")

    # Instructor specific communication channel coordinates links
    twitter_url = models.URLField(blank=True, null=True, verbose_name="Teacher X Account URL Link")
    facebook_url = models.URLField(blank=True, null=True, verbose_name="Teacher Facebook Account URL Link")
    linkedin_url = models.URLField(blank=True, null=True, verbose_name="Teacher LinkedIn Account URL Link")

    class Meta:
        verbose_name = "modern7 Faculty Instructor"
        verbose_name_plural = "modern7 Faculty Instructors"

    def __str__(self):
        return f"{self.full_name} ({self.school_tenant.school_name})"


# ==============================================================================
# 🎓 ACADEMIC SYLLABI LISTINGS & STUDENT TRANSACTION LEADS MAILBOX
# ==============================================================================

class Modern7CourseListing(models.Model):
    """
    🎓 LESSON TRACK LISTING ENGINE FOR MODERN7
    Houses master lesson details, duration specs, lecture modules,
    price labels, and embedded trailer preview video codes.
    """
    school_tenant = models.ForeignKey(
        Modern7SchoolTenant,
        on_delete=models.CASCADE,
        related_name="campus_courses",
        verbose_name="School Context Anchor"
    )
    dynamic_category = models.ForeignKey(
        Modern7CourseCategory,
        on_delete=models.PROTECT,
        related_name="category_courses",
        verbose_name="Category Target Bucket Link"
    )
    assigned_instructor = models.ForeignKey(
        Modern7FacultyInstructor,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="instructor_courses",
        verbose_name="Assigned Lecturer Node"
    )

    # 📝 COURSE CONTENT SPECIFICATIONS
    course_title = models.CharField(max_length=255, verbose_name="Course Title Heading Name")
    course_thumbnail = models.ImageField(upload_to="modern7/courses/",
                                         verbose_name="High-Res Course Feature Cover Picture Image")

    course_description_main = models.TextField(verbose_name="Primary Core Introduction Description Paragraph Copy")
    course_description_secondary = models.TextField(
        verbose_name="Secondary Structural Curriculum Description Paragraph Copy")

    course_overview_text = models.TextField(blank=True, null=True,
                                            verbose_name="Interactive Overview Tab Main Content Copy")
    curriculum_syllabus_text = models.TextField(
        blank=True,
        null=True,
        verbose_name="Curriculum Syllabus Syllabus Tab Rich Text (HTML Allowed)",
        help_text="Write out your module outlines using paragraphs or list nodes cleanly."
    )

    # ⏳ TIME & CAPACITY SCHEDULING SPEC DATA TRACKS
    duration_label = models.CharField(max_length=100, default="2 Hrs 30 Min",
                                      verbose_name="Lecture Duration Specs String (e.g. 10 weeks, 4 Hrs)")
    count_modules_text = models.CharField(max_length=100, default="12 Lectures",
                                          verbose_name="Total Training Modules String (e.g. 45 Classes)")
    count_students_registered = models.CharField(max_length=50, default="1,000+ Enrolled",
                                                 verbose_name="Card Indicator: Enrolled Capacity Number String")
    seats_available = models.IntegerField(default=30, verbose_name="Open Registration Seats Available Capacity")

    # 💰 VALUE LABEL TRACKING FIELDS
    price_display_label = models.CharField(max_length=60, default="$99",
                                           verbose_name="Course Fee Price Display Text Label (e.g. $49, Free)")
    is_certified = models.BooleanField(default=True,
                                       verbose_name="Provides Professional Certification Stamps Upon Graduation")
    embed_video_url_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="YouTube Trailer Video Video ID String Only",
        help_text="Provide ONLY the 11-character video ID from the URL code block text. e.g. 'RXv_uIN6e-Y'"
    )

    is_visible_on_catalog = models.BooleanField(default=True, verbose_name="Visible on School storefront Roster View")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "modern7 Course Listing"
        verbose_name_plural = "modern7 Course Listings"

    def __str__(self):
        return f"{self.course_title} — {self.school_tenant.school_name}"


class Modern7StudentEnquiryLead(models.Model):
    """
    📥 STUDENT REGISTRATION INTAKE LEADS MAILBOX
    Captures inbound queries submitted straight from your multi-tenant contact form tables.
    """
    school_tenant = models.ForeignKey(
        Modern7SchoolTenant,
        on_delete=models.CASCADE,
        related_name="contact_leads",
        verbose_name="School Context Anchor"
    )
    client_name = models.CharField(max_length=150, verbose_name="Student Applicant Name")
    client_email = models.EmailField(verbose_name="Student Communication Mailbox Address")
    lead_subject = models.CharField(max_length=255, verbose_name="Message Subject Title Track")
    message_content = models.TextField(verbose_name="Applicant Enquiry Message Content text Body")

    is_processed_flag = models.BooleanField(default=False,
                                            verbose_name="Admissions Registrar Processed Status Indicator Mark")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "modern7 Contact Enquiry Lead"
        verbose_name_plural = "modern7 Contact Enquiry Leads"

    def __str__(self):
        return f"Lead: {self.client_name} -> {self.school_tenant.school_name} [{self.lead_subject[:20]}]"


class Modern7CourseReview(models.Model):
    """
    📥 STUDENT TEXTUAL REVIEWS FEEDBACK MAILBOX
    Saves authentic scorable feedback comments submitted straight from specific course details forms.
    """
    target_course = models.ForeignKey(
        Modern7CourseListing,
        on_delete=models.CASCADE,
        related_name="course_reviews",
        verbose_name="Target Lecture Class Node"
    )
    student_name = models.CharField(max_length=150, verbose_name="Student Reviewer Name")
    student_email = models.EmailField(verbose_name="Student Verification Email Address")
    rating_score = models.IntegerField(default=5, verbose_name="Star Review Score Metric (1-5 Rating)")
    feedback_comment_text = models.TextField(verbose_name="Review Feedback Text Comment Body Copy Description")

    is_approved_for_public = models.BooleanField(default=True,
                                                 verbose_name="Approved to Stream on Public View Frontboards")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "modern7 Student Course Review"
        verbose_name_plural = "modern7 Student Course Reviews"

    def __str__(self):
        return f"Review by {self.student_name} ({self.rating_score} Stars) for {self.target_course.course_title[:20]}"

