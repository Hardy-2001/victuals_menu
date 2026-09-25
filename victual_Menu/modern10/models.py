
from django.db import models
from django.contrib.auth.models import User

# =========================================================================
# 🏢 PART 1A: MULTI-TENANT ISOLATED IDENTITY VAULTS (CAR RENTAL FOCUS)
# =========================================================================

class Modern10CarTenant(models.Model):
    """
    🗄️ ISOLATED MODERN10 AUTOMOTIVE IDENTITY VAULT
    Anchors core credentials, unique dealer slugs, and owner linking with agent tracking.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User Account")
    business_name = models.CharField(max_length=120, unique=True, verbose_name="Automotive Business Name")
    slug_name = models.SlugField(max_length=120, unique=True, help_text="e.g., corex-autos, elite-rentals")

    # 👑 THE AGENT ANCHOR COLUMN: Links this automotive hub workspace back to the onboarding field agent profile!
    assigned_agent = models.ForeignKey(
        'super_admin.AgentProfile',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='modern10_onboarded_studios',
        help_text="The field agent tracking this premium car rentals profile registry",
        verbose_name="Assigned Agent"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "modern10 Car Tenant"
        verbose_name_plural = "modern10 Car Tenants"

    def __str__(self):
        return f"{self.business_name} ({self.slug_name})"

class Modern10CarStoreFront(models.Model):
    """
    💎 PREMIUM AUTOMOTIVE APP VISUAL CONTROL DECK FOR MODERN10
    Houses global brand headers, contact parameters, hero metrics, about statements,
    dynamic 'Why Choose Us' feature text rows, and brand value proposition pillars.
    """
    tenant_identity = models.OneToOneField(
        Modern10CarTenant,
        on_delete=models.CASCADE,
        related_name='studio_profile',
        verbose_name="SaaS Identity Link",
        null=True,
        blank=True
    )

    # Global Communication Default Fallbacks
    contact_email = models.EmailField(default="info@corexautos.ng")
    contact_phone = models.CharField(max_length=30, default="+234 (0) 803 456 7891")
    logo = models.ImageField(upload_to='modern10_logos/', blank=True, null=True)

    # Main Hero Showcase Accents (Home Page Layout)
    hero_title = models.CharField(max_length=255, default="Mercedes-Benz G63 AMG")
    hero_subtitle = models.TextField(default="Find, Book, and Rent Car in Easy Steps")
    hero_banner_image = models.ImageField(upload_to='modern10_heros/', blank=True, null=True)

    # Modular Content Block: About Us Text Specifications
    about_headline = models.CharField(max_length=255, default="We Provide Everything You Need For Ultimate Mobility")
    about_description_copy = models.TextField(default="Operating heavy-duty multi-tenant logistics across Nigeria's economic hubs requires strict technical discipline.")

    # 🟢 DYNAMIC "WHY CHOOSE US" CONTENT NODES
    why_choose_us_intro = models.TextField(
        default="We provide verified documentation, secure payment gateways, and highly vetted drivers for all car rentals.",
        verbose_name="Why Choose Us Description"
    )

    pillar_1_title = models.CharField(max_length=100, default="100% Verified Custom Duty & Tokunbo Clearance Papers")
    pillar_2_title = models.CharField(max_length=100, default="Real-time GPS Fleet Surveillance & Telemetry Support")
    pillar_3_title = models.CharField(max_length=100, default="Comprehensive Insurance Coverage on All Operational Leases")
    pillar_4_title = models.CharField(max_length=100, default="Verified Ownership Transfers and Stress-free Registration")

    # 🟢 DYNAMIC STOREFRONT CORE SERVICE PARAMETER DESCRIPTION INPUTS
    service_1_desc = models.TextField(
        default="Rent luxury cars easily in Lagos, Abuja, and Port Harcourt. Available for weddings, executives, and protocols.",
        verbose_name="Luxury Car Rentals Service Text"
    )
    service_2_desc = models.TextField(
        default="Verified Foreign Used (Tokunbo) and Brand New imports with complete custom clearance papers clearance checks verified.",
        verbose_name="Buying A Vehicle Service Text"
    )
    service_3_desc = models.TextField(
        default="Expert diagnostic centers with certified tracking technicians for computer programming, suspension tuning, and upgrades.",
        verbose_name="Car Maintenance Service Text"
    )
    service_4_desc = models.TextField(
        default="Dedicated road emergency breakdown support networks and real-time fleet surveillance telemetry across all states.",
        verbose_name="Support 24/7 Service Text"
    )

    # 🟢 ADDED: 3 Manageable Brand Feature Paragraph Columns
    feature_main_headline = models.CharField(
        max_length=255,
        default="We Are A Trusted Name In Auto Distribution Matrix",
        verbose_name="Feature Section Headline"
    )
    feature_desc_paragraph_1 = models.TextField(
        default="With thousands of luxury miles navigated across active Nigerian expressways, our platform ensures seamless fleet leasing and direct ownership transfers without traditional documentation delays.",
        verbose_name="Feature Paragraph 1 Copy Text"
    )
    feature_desc_paragraph_2 = models.TextField(
        default="Every single listing undergoes standard multi-point mechanical inspections, structural integrity checks, and custom duty document clearance profiling before joining our catalog view grids.",
        verbose_name="Feature Paragraph 2 Copy Text"
    )

    # 🟢 ADDED: 4 Manageable Floating Badge Text Mappers
    feature_badge_1 = models.CharField(max_length=60, default="V8 Engine Core", verbose_name="Feature Badge 1 Tag Name")
    feature_badge_2 = models.CharField(max_length=60, default="Twin Turbo", verbose_name="Feature Badge 2 Tag Name")
    feature_badge_3 = models.CharField(max_length=60, default="Climate Control", verbose_name="Feature Badge 3 Tag Name")
    feature_badge_4 = models.CharField(max_length=60, default="Armored Option", verbose_name="Feature Badge 4 Tag Name")


    # 🟢 DYNAMIC ABOUT STRATEGIC PANELS: MISSION & VISION COPY
    about_mission_text = models.TextField(
        default="To democratize access to premium automotive leasing and direct luxury ownership transfers across Nigeria by removing traditional documentation friction points and opaque transaction layouts entirely from the marketplace economy.",
        verbose_name="Our Mission Statement Text"
    )
    about_vision_text = models.TextField(
        default="To establish the primary digital multi-tenant infrastructure powering vehicle procurement security, asset surveillance management, and corporate protocol coordination across West Africa with 100% processing transparency.",
        verbose_name="Our Vision Statement Text"
    )

    # 🟢 DYNAMIC HOMEPAGE & ABOUT PLATFORM METRIC INFRASTRUCTURE COUNTERS
    stats_vehicles_count = models.CharField(max_length=30, default="1,922", verbose_name="Counter: Vehicles In Stock")
    stats_sales_count = models.CharField(max_length=30, default="1,500+", verbose_name="Counter: Successful Direct Sales")
    stats_reviews_count = models.CharField(max_length=30, default="1,922", verbose_name="Counter: Verified Dealer Reviews")
    stats_clients_count = models.CharField(max_length=30, default="5,100+", verbose_name="Counter: Happy Platform Clients")

    # 🟢 DYNAMIC FOOTER SOCIAL NETWORKING CHANNELS (ADMIN MANAGED)
    facebook_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Merchant Facebook URL",
        help_text="Optional profile link (e.g., https://facebook.com)."
    )
    twitter_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Merchant Twitter / X URL",
        help_text="Optional profile link (e.g., https://x.com)."
    )
    instagram_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Merchant Instagram URL",
        help_text="Optional profile link (e.g., https://instagram.com)."
    )

    initialized_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-initialized_at']
        verbose_name = "modern10 Car Store Profile"
        verbose_name_plural = "modern10 Car Store Profiles"

    @property
    def user(self): return self.tenant_identity.user

    @property
    def business_name(self): return self.tenant_identity.business_name

    @property
    def slug_name(self): return self.tenant_identity.slug_name

    def __str__(self):
        return f"{self.tenant_identity.business_name} — Car Control Deck"

# =========================================================================
# 🏎️ PART 1B: DYNAMIC CHILD LAYER REPEATING CONTENT NODES
# =========================================================================

class Modern10CarCategory(models.Model):
    """
    📁 USER-MANAGED DYNAMIC VEHICLE SEGMENTS
    Allows owners to spawn custom sections from the admin panel (e.g., SUVs, Sedans, Exotic, Armored Protocol).
    """
    store = models.ForeignKey(Modern10CarStoreFront, on_delete=models.CASCADE, related_name='studio_categories')
    category_name = models.CharField(max_length=100, verbose_name="Category Type Title")
    category_slug = models.SlugField(max_length=120, help_text="e.g., luxury-suvs, tokunbo-sedans")

    class Meta:
        unique_together = ('store', 'category_slug')
        verbose_name = "modern10 Car Category Slot"
        verbose_name_plural = "modern10 Car Category Slots"

    def __str__(self):
        return f"{self.category_name} — {self.store.tenant_identity.business_name}"


class Modern10CarListing(models.Model):
    """
    🚘 SHOWCASE VAULT FOR REPEATING VEHICLE INVENTORY FLEET CARDS
    Manages complete automotive specifications for both rentals and direct purchases.
    """
    PURPOSE_CHOICES = (
        ('RENT', 'For Short-Term Rental / Hire'),
        ('SALE', 'For Direct Purchase / Sale'),
    )

    FUEL_CHOICES = (
        ('PETROL', 'Petrol / Unleaded'),
        ('DIESEL', 'Diesel'),
        ('HYBRID', 'Hybrid Engine'),
        ('ELECTRIC', 'Electric EV Matrix'),
    )

    store = models.ForeignKey(Modern10CarStoreFront, on_delete=models.CASCADE, related_name='studio_products')
    make_and_model = models.CharField(max_length=150, verbose_name="Vehicle Make and Model",
                                      help_text="e.g. Mercedes-Benz G63 AMG")
    dynamic_category = models.ForeignKey(
        Modern10CarCategory,
        on_delete=models.PROTECT,
        related_name='listed_vehicles',
        verbose_name="Vehicle Segment Category"
    )

    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES, default='RENT', verbose_name="Listing Purpose")

    # Local financial denominators
    rental_price_per_day = models.DecimalField(max_digits=12, decimal_places=2, default=0.00,
                                               help_text="Daily hire fee in Naira (if purpose is Rent)")
    sale_price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00,
                                     help_text="Total procurement fee in Naira (if purpose is Sale)")

    # Core technical car metrics specifications
    vehicle_image = models.ImageField(upload_to='modern10_cars/', help_text="Upload crisp automotive picture layout")

    # 4 Optional Gallery Image Fields (Safely insulated against null exceptions)
    gallery_image_1 = models.ImageField(upload_to='modern10_cars/gallery/', blank=True, null=True,
                                        verbose_name="Gallery Picture 1 (Interior Cabin)",
                                        help_text="Optional interior view")
    gallery_image_2 = models.ImageField(upload_to='modern10_cars/gallery/', blank=True, null=True,
                                        verbose_name="Gallery Picture 2 (Engine Bay)",
                                        help_text="Optional mechanical layout view")
    gallery_image_3 = models.ImageField(upload_to='modern10_cars/gallery/', blank=True, null=True,
                                        verbose_name="Gallery Picture 3 (Rear Profile)",
                                        help_text="Optional tail light angle view")
    gallery_image_4 = models.ImageField(upload_to='modern10_cars/gallery/', blank=True, null=True,
                                        verbose_name="Gallery Picture 4 (Extra Details)",
                                        help_text="Optional dashboard/wheel custom angle view")

    year_of_manufacture = models.IntegerField(default=2024, verbose_name="Year Model")
    mileage = models.CharField(max_length=50, default="0 km", help_text="Odometer calculation (e.g. 15,200 km)")
    transmission_automatic = models.BooleanField(default=True, verbose_name="Automatic Transmission",
                                                 help_text="Checked = Auto, Unchecked = Manual")
    horsepower = models.CharField(max_length=30, default="300 hp", verbose_name="Engine Horsepower")
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='PETROL')
    seating_capacity = models.IntegerField(default=5)

    vehicle_details_text = models.TextField(default="Premium design checked with multi-point diagnostics clear.",
                                            verbose_name="Car Overview / Description")

    # 🟢 ADDED: Multi-line feature checklist box (Allows you to insert custom line traits for each car!)
    vehicle_features_checklist = models.TextField(
        default="• Comprehensive Multi-point Diagnostic Log Clear\n• Full Synthetic Engine Oil Suite Complete\n• Keyless Entry Transponder System Ready\n• High-performance Climate Control Configuration",
        verbose_name="Vehicle Features Checklist",
        help_text="Insert custom features line items. Start each parameter line with a bullet point (•) or a clean hyphen (-)."
    )

    # Tracking metrics variables
    stock_reference = models.CharField(max_length=50, default="K99D10459", verbose_name="Stock Reference ID")
    vin_registry = models.CharField(max_length=50, default="3VWKM245686NGR", verbose_name="VIN Registry code")
    showroom_location = models.CharField(max_length=255, default="Lekki Phase 1, Lagos, Nigeria")

    # 🟢 ADDED: Live Google Maps iframe link tracker parameter slot
    google_map_embed_url = models.TextField(
        default="https://google.com",
        verbose_name="Google Maps Iframe Embed URL Only",
        help_text="Go to Google Maps -> Click Share -> Select Embed a map -> Copy ONLY the 'src' link text string inside the quotes (starts with https://google.com...)."
    )

    # Feature Toggles
    is_available = models.BooleanField(default=True, verbose_name="Available for Catalog Grid Display")
    is_featured_on_home = models.BooleanField(default=False, verbose_name="Showcase in Home Sliders")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "modern10 Vehicle Fleet Listing Card"
        verbose_name_plural = "modern10 Vehicle Fleet Listing Cards"

    def __str__(self):
        return f"{self.make_and_model} [{self.get_purpose_display()}] — {self.store.tenant_identity.business_name}"


class Modern10StudioTeamMember(models.Model):
    """
    👥 USER-MANAGED CORPORATE TEAM PROFILE MATRIX
    Allows agents and business owners to manage showroom experts directly.
    """
    store = models.ForeignKey(Modern10CarStoreFront, on_delete=models.CASCADE, related_name='studio_team_members')
    member_name = models.CharField(max_length=120, verbose_name="Full Name")
    member_role = models.CharField(max_length=120, verbose_name="Corporate Designation",
                                   help_text="e.g. Director of Logistics, CEO, Sales Consultant")
    member_avatar = models.ImageField(upload_to='modern10_team/', verbose_name="Profile Picture")

    class Meta:
        verbose_name = "modern10 Studio Team Member Card"
        verbose_name_plural = "modern10 Studio Team Member Cards"

    def __str__(self):
        return f"{self.member_name} ({self.member_role}) — {self.store.tenant_identity.business_name}"


class Modern10CarTestimonial(models.Model):
    """
    💬 CUSTOMER TESTIMONIAL CAROUSEL
    Handles sliding client quotes, corporate roles, and profile icons per store dashboard.
    """
    store = models.ForeignKey(Modern10CarStoreFront, on_delete=models.CASCADE, related_name='studio_testimonials')
    client_name = models.CharField(max_length=100, verbose_name="Client Name")
    client_role = models.CharField(max_length=120, verbose_name="Designation/Company")
    avatar = models.ImageField(upload_to='modern10_avatars/', blank=True, null=True, verbose_name="User Avatar")
    quote = models.TextField(verbose_name="Testimonial Quote Statement")

    class Meta:
        verbose_name = "modern10 Car Testimonial"
        verbose_name_plural = "modern10 Car Testimonials"

    def __str__(self):
        return f"Review by {self.client_name} — {self.store.tenant_identity.business_name}"


class Modern10CarBlogArticle(models.Model):
    """
    📰 RECENT AUTO INDUSTRY BLOG POSTS MODULE
    Handles corporate article updates to showcase on your landing grids.
    """
    store = models.ForeignKey(Modern10CarStoreFront, on_delete=models.CASCADE, related_name='studio_blogs')
    article_title = models.CharField(max_length=250, verbose_name="Article Title")
    author_display_name = models.CharField(max_length=100, default="Alao Chukwuma")
    article_thumbnail = models.ImageField(upload_to='modern10_blogs/')
    article_summary = models.TextField(default="Premium automotive review overview guidelines.")
    article_body_content = models.TextField(default="Full journalism entry logs specifications.")
    published_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = "modern10 Studio Blog Post"
        verbose_name_plural = "modern10 Studio Blog Posts"

    def __str__(self):
        return f"{self.article_title} by {self.author_display_name}"


class Modern10NewsletterSubscription(models.Model):
    """
    ✉️ AUTOMOTIVE CLIENT NEWSLETTER RADAR
    Captures footer customer subscriber details natively.
    """
    store = models.ForeignKey(Modern10CarStoreFront, on_delete=models.CASCADE, related_name='studio_subscribers')
    subscriber_email = models.EmailField()
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "modern10 Newsletter Lead"
        verbose_name_plural = "modern10 Newsletter Leads"

    def __str__(self):
        return f"{self.subscriber_email} — {self.store.tenant_identity.business_name}"
