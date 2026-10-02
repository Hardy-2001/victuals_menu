from django.db import models
from django.contrib.auth.models import User

# =========================================================================
# 🏢 PART 1: MULTI-TENANT ISOLATED IDENTITY VAULTS (BEAUTY SALON FOCUS)
# =========================================================================

class modern12SalonTenant(models.Model):
    """
    🗄️ ISOLATED modern12 BEAUTY ENTERPRISE IDENTITY VAULT
    Anchors core merchant credentials, unique workspace slugs, and assigned onboarding field agents.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User Account")
    business_name = models.CharField(max_length=120, unique=True, verbose_name="Salon Business Name")
    slug_name = models.SlugField(max_length=120, unique=True, help_text="e.g., corex-salon, elite-makeovers")

    # Links this beauty lounge back to the onboarding field agent profile tracker!
    assigned_agent = models.ForeignKey(
        'super_admin.AgentProfile',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='modern12_onboarded_salons',
        help_text="The field agent tracking this premium beauty salon profile registry",
        verbose_name="Assigned Agent"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "modern12 Salon Tenant"
        verbose_name_plural = "modern12 Salon Tenants"

    def __str__(self):
        return f"{self.business_name} ({self.slug_name})"


class modern12SalonStoreFront(models.Model):
    """
    💎 PREMIUM BEAUTY APP VISUAL CONTROL DECK FOR modern12
    Houses global salon brand headers, contact parameters, hero metrics, story statements,
    marketing campaigns, and social handles manageable per sub-tenant registry.
    """
    tenant_identity = models.OneToOneField(
        modern12SalonTenant,
        on_delete=models.CASCADE,
        related_name='studio_profile',  # 🟢 FIXED: Matches your subdomain context helper engines line-for-line!
        verbose_name="SaaS Identity Link"
    )

    # Global Communication Default Fallbacks
    contact_email = models.EmailField(default="info@prettyautos.ng", verbose_name="Official Support Email")
    contact_phone = models.CharField(max_length=50, default="+234 (0) 803 456 7891", verbose_name="Contact Phone Line")
    contact_address = models.CharField(max_length=255, default="203 Fake St. Lekki Phase 1, Lagos, Nigeria", verbose_name="Physical Depot Address")
    logo = models.ImageField(upload_to='modern12_logos/', blank=True, null=True, verbose_name="Salon Logo Graphic")

    # Main Hero Showcase Accents (Home Page Layout)
    hero_title = models.CharField(max_length=150, default="Beauty Salon", verbose_name="Hero Title Main Headline")
    hero_subtitle = models.CharField(max_length=255, default="Pretty Menu & Premium Grooming Services Tailored For You.", verbose_name="Hero Subtitle Copy Block")
    hero_banner_image = models.ImageField(upload_to='modern12_banners/', blank=True, null=True, verbose_name="Hero Background Parallax Banner")

    # 3-Column Core Service Offer Highlights Cards text fields
    feature_1_title = models.CharField(max_length=100, default="Skin & Beauty Care", verbose_name="Feature 1 Card Title")
    feature_1_desc = models.TextField(default="Premium facial micro-treatment layouts engineered to restore organic cellular glow safely.", verbose_name="Feature 1 Short Copy Text")

    feature_2_title = models.CharField(max_length=100, default="Makeup Pro", verbose_name="Feature 2 Card Title")
    feature_2_desc = models.TextField(default="Red-carpet cosmetic contours and flawless tone blends matched for high-end events.", verbose_name="Feature 2 Short Copy Text")

    feature_3_title = models.CharField(max_length=100, default="Hair Styling", verbose_name="Feature 3 Card Title")
    feature_3_desc = models.TextField(default="Precision texturing, custom weaving, and deep therapeutic scalp care routines.", verbose_name="Feature 3 Short Copy Text")

    # About Us Corporate Story Profile Cards
    about_headline = models.CharField(max_length=200, default="Welcome to Pretty A Beauty Salon Website", verbose_name="About View Section Headline")
    about_description_copy = models.TextField(default="Premium multi-tenant beauty grooming matrices, custom texturing hair hubs, and executive skin styling networks curated out of live inventory profiles to deliver absolute aesthetic luxury.", verbose_name="About Detailed Narrative Paragraph Copy")
    about_banner_image = models.ImageField(upload_to='modern12_about/', blank=True, null=True, verbose_name="About Section Side Accent Graphic")

    # Flash Special Campaigns Options
    campaign_headline = models.CharField(max_length=150, default="Student Discount Strategy", verbose_name="Campaign Promotional Title")
    campaign_description = models.TextField(default="Flash your active university identification credentials on terminal checkouts to claim 25% off all basic haircuts, therapeutic hair coloring, and skin cleansing matrix sessions.", verbose_name="Campaign Copy Statement Block")

    # Operational Performance Metric Counter Trackers
    stat_makeovers = models.CharField(max_length=40, default="1,500+", verbose_name="Stat Counter: Makeup Actions")
    stat_procedures = models.CharField(max_length=40, default="2,840", verbose_name="Stat Counter: Procedures Met")
    stat_clients = models.CharField(max_length=40, default="4,200+", verbose_name="Stat Counter: Glad Platform Clients")
    stat_treatments = models.CharField(max_length=40, default="980", verbose_name="Stat Counter: Skin Treatment Logs")

    # Global Merchant Social Media Sync Channels (Admin Managed)
    facebook_url = models.URLField(blank=True, null=True, verbose_name="Merchant Facebook URL", help_text="Optional profile link.")
    twitter_url = models.URLField(blank=True, null=True, verbose_name="Merchant Twitter / X URL", help_text="Optional profile link.")
    instagram_url = models.URLField(blank=True, null=True, verbose_name="Merchant Instagram URL", help_text="Optional profile link.")


    # =========================================================================
    # ⏳ DYNAMIC WORKING HOURS SYSTEM FIELDS (100% IMAGE PARITY ALIGNED)
    # =========================================================================
    hours_banner_image = models.ImageField(
        upload_to='modern12_hours/',
        blank=True,
        null=True,
        verbose_name="Working Hours Left Side Image Display Banner",
        help_text="Upload a picture of professional barbering equipment to show on the left side panel."
    )
    hours_monday = models.CharField(max_length=50, default="09 AM - 09 PM", verbose_name="Monday Operational Timing")
    hours_tuesday = models.CharField(max_length=50, default="09 AM - 09 PM", verbose_name="Tuesday Operational Timing")
    hours_wednesday = models.CharField(max_length=50, default="09 AM - 09 PM", verbose_name="Wednesday Operational Timing")
    hours_thursday = models.CharField(max_length=50, default="09 AM - 09 PM", verbose_name="Thursday Operational Timing")
    hours_friday = models.CharField(max_length=50, default="09 AM - 09 PM", verbose_name="Friday Operational Timing")
    hours_weekend = models.CharField(max_length=50, default="Closed", verbose_name="Weekend Operational Timing (Sat / Sun)")





    initialized_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-initialized_at']
        verbose_name = "modern12 Salon Store Profile"
        verbose_name_plural = "modern12 Salon Store Profiles"

    @property
    def user(self): return self.tenant_identity.user

    @property
    def business_name(self): return self.tenant_identity.business_name

    @property
    def slug_name(self): return self.tenant_identity.slug_name

    def __str__(self):
        return f"{self.tenant_identity.business_name} — Salon Control Deck"

# =========================================================================
# 💇‍♀️ PART 2: DYNAMIC CHILD LAYER REPEATING CONTENT NODES (SALON GRID)
# =========================================================================

class modern12SalonStylist(models.Model):
    """
    👥 USER-MANAGED CORPORATE TEAM PROFILE MATRIX
    Allows salon business owners to manage hair colorists and makeup experts directly.
    """
    store = models.ForeignKey(modern12SalonStoreFront, on_delete=models.CASCADE, related_name='salon_stylists')
    stylist_name = models.CharField(max_length=120, verbose_name="Expert Full Name")
    stylist_role = models.CharField(max_length=120, verbose_name="Corporate Designation",
                                   help_text="e.g. Master Barber, Cosmetic Lead, Nail Tech Consultant")
    stylist_avatar = models.ImageField(upload_to='modern12_stylists/', verbose_name="Profile Picture")
    stylist_bio_summary = models.TextField(verbose_name="Short Professional Bio", default="Vetted industry specialist.")

    class Meta:
        verbose_name = "modern12 Salon Expert Stylist Card"
        verbose_name_plural = "modern12 Salon Expert Stylist Cards"

    def __str__(self):
        return f"{self.stylist_name} ({self.stylist_role}) — {self.store.tenant_identity.business_name}"


class modern12SalonService(models.Model):
    """
    💰 USER-MANAGED DYNAMIC TREATMENT & PRICING PLANS MENU
    Powers transparent menu cards wired with direct WhatsApp order anchors.
    """
    store = models.ForeignKey(modern12SalonStoreFront, on_delete=models.CASCADE, related_name='salon_services')
    service_title = models.CharField(max_length=120, verbose_name="Grooming Package Title", help_text="e.g. Bridal Glam Package")
    service_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Total treatment fee in Naira")
    service_features_list = models.TextField(
        default="• Full Face Contouring\n• Premium Lash Extensions\n• Setting Spray Matte Fix\n• Professional Touch-up Kit Included",
        verbose_name="Package Features Checklist Lines",
        help_text="Insert features line items. Start each parameter line with a bullet point (•) or a clean hyphen (-)."
    )

    class Meta:
        verbose_name = "modern12 Salon Pricing Tier Card"
        verbose_name_plural = "modern12 Salon Pricing Tier Cards"

    # 🟢 FIXED PYTHON SYNTAX: Swapped the HTML filter out for pure Python numeric format mapping to destroy red error lines!
    def __str__(self):
        try:
            formatted_price = f"{int(self.service_price):,}"
        except (ValueError, TypeError):
            formatted_price = str(self.service_price)
        return f"{self.service_title} (₦{formatted_price}) — {self.store.tenant_identity.business_name}"

class modern12PortfolioWork(models.Model):
    """
    📸 RECENT TREATMENT LOOKBOOK & SHOWCASE GALLERY
    Streams real salon makeover transformations natively across portfolio lookbook rows.
    """
    CATEGORY_CHOICES = (
        ('MAKEUP', 'Cosmetics / Make Up'),
        ('FACIAL', 'Facial & Spa Treatment'),
        ('HAIR', 'Hair Cut / Styling'),
        ('NAIL', 'Nail Art / Pedicure'),
    )

    store = models.ForeignKey(modern12SalonStoreFront, on_delete=models.CASCADE, related_name='portfolio_works')
    work_title = models.CharField(max_length=150, verbose_name="Transformation Title", help_text="e.g. Matte Lips Makeover")
    work_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='HAIR', verbose_name="Lookbook Category")
    work_image = models.ImageField(upload_to='modern12_lookbooks/', help_text="Upload crisp transformation portfolio look")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "modern12 Portfolio Lookbook Image"
        verbose_name_plural = "modern12 Portfolio Lookbook Images"

    def __str__(self):
        return f"{self.work_title} [{self.get_work_category_display()}] — {self.store.tenant_identity.business_name}"


class modern12SalonBlogArticle(models.Model):
    """
    📰 RECENT BEAUTY TRENDS & HEALTHY JOURNALISM MODULE
    Handles inline text-expansion guides to educate showroom readers.
    """
    store = models.ForeignKey(modern12SalonStoreFront, on_delete=models.CASCADE, related_name='salon_articles')
    article_title = models.CharField(max_length=250, verbose_name="Article Title")
    author_display_name = models.CharField(max_length=100, default="Lounge Director")
    article_thumbnail = models.ImageField(upload_to='modern12_blogs/')
    article_summary = models.TextField(default="Premium skin maintenance guide review overview.")
    article_body_content = models.TextField(default="Full journalism entry logs specifications.")
    published_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = "modern12 Salon Blog Post"
        verbose_name_plural = "modern12 Salon Blog Posts"

    def __str__(self):
        return f"{self.article_title} by {self.author_display_name}"

# =========================================================================
# 🛍️ PART 3: DYNAMIC REPEATING SALON INVENTORY RETAIL SUITE (E-COMMERCE)
# =========================================================================

class modern12SalonProduct(models.Model):
    """
    💈 BARBER SALON RETAIL PRODUCT INVENTORY VAULT
    🔒 RESTRICTED OVERHAUL: Powers dynamic product cards (perfumes, grooming care) with
    price tags, descriptions, homepage display controls, and native WhatsApp cart buttons.
    """
    CATEGORY_CHOICES = (
        ('PERFUME', 'Exotic Perfumes / Scents'),
        ('OTHER', 'General Cosmetics & Care'),
    )

    store = models.ForeignKey(modern12SalonStoreFront, on_delete=models.CASCADE, related_name='salon_products')
    product_name = models.CharField(max_length=150, verbose_name="Product Brand & Name",
                                    help_text="e.g. Royal Oud Perfume, Texture Wax")
    # 🟢 FIXED LOGIC: Group choices restricted strictly to perfumes and general barbering cosmetics care!
    product_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER',
                                        verbose_name="Product Category Group")
    product_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00,
                                        help_text="Retail selling fee in Naira")
    product_image = models.ImageField(upload_to='modern12_shop/',
                                      help_text="Upload a crisp, high-resolution product picture")
    product_description = models.TextField(default="Premium salon-grade quality checked and approved.",
                                           verbose_name="Product Description / Details")

    # CHOOSE WHAT APPEARS ON INDEX PAGE: Boolean field control tag matrix
    is_featured_on_home = models.BooleanField(default=False, verbose_name="Showcase on Home Page Product Sliders",
                                              help_text="Check this box to push this retail item directly to your index page view layout.")
    is_in_stock = models.BooleanField(default=True, verbose_name="Item Is Available In Stock Grid")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "modern12 Salon Shop Product"
        verbose_name_plural = "modern12 Salon Shop Products"

    def __str__(self):
        try:
            formatted_price = f"{int(self.product_price):,}"
        except (ValueError, TypeError):
            formatted_price = str(self.product_price)
        return f"{self.product_name} (₦{formatted_price}) — {self.store.tenant_identity.business_name}"
