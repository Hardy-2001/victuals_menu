from django.db import models
from django.contrib.auth.models import User


# ==============================================================================
# 🔒 APP LEVEL SAAS TENANT CORE REGISTRY
# ==============================================================================

class Modern6RealEstateTenant(models.Model):
    """
    🔒 ISOLATED MODERN6 REAL ESTATE IDENTITY VAULT
    Anchors core user credentials, unique agency slugs, and onboarding tracking agents.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User Account")
    agency_name = models.CharField(max_length=120, unique=True, verbose_name="Real Estate Agency Name")
    agency_slug = models.SlugField(max_length=120, unique=True, help_text="e.g., deluxe-homes")

    # 👑 THE ANCHOR COLUMN: Links this agency workspace back to the onboarding field agent profile!
    assigned_agent = models.ForeignKey(
        'super_admin.AgentProfile',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='modern6_onboarded_agencies',
        help_text="The field agent tracking this premium real estate profile registry"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "modern6 Property Tenant"
        verbose_name_plural = "modern6 Property Tenants"

    def __str__(self):
        return f"{self.agency_name} ({self.agency_slug})"


# ==============================================================================
# 💎 VISUAL CONTROL PANEL DESIGN SETTINGS CONFIGURATIONS
# ==============================================================================

class Modern6AgencyStoreFront(models.Model):
    """
    💎 LUXURY REAL ESTATE APP VISUAL CONTROL DECK FOR MODERN6
    Houses global brand headers, emergency contacts, hero taglines, and statistic indicators.
    """
    tenant_identity = models.OneToOneField(
        Modern6RealEstateTenant,
        on_delete=models.CASCADE,
        related_name='agency_profile',
        verbose_name="SaaS Identity Link",
        null=True,
        blank=True
    )

    # 📞 Agency Communication & Coordinates (Nigeria Style Defaults Fallbacks Built-in)
    brokerage_email = models.EmailField(default="brokerage@corex.ng")
    brokerage_hotline = models.CharField(max_length=30, default="+234 (0) 900 800 7000")
    office_physical_address = models.CharField(max_length=255,
                                               default="Block 10, Admiralty Way, Lekki Phase 1, Lagos, Nigeria")
    agency_logo = models.ImageField(upload_to='modern6_agency_logos/', blank=True, null=True)



    # 🎨 Main Luxury Showcase Hero Accents
    hero_headline_title = models.CharField(max_length=255, default="Find Your Dream Safe Haven & Luxury Space")
    hero_subheadline_copy = models.TextField(
        default="Discover premium architectural masterpieces, high-tier residential structures, and secure real estate investment portfolios across Nigeria.")

    # 📊 Social Proof Counter Metrics
    count_properties_sold = models.IntegerField(default=145)
    count_active_listings = models.IntegerField(default=38)
    count_verified_brokers = models.IntegerField(default=12)

    initialized_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-initialized_at']
        verbose_name = "modern6 Agency Store Profile"
        verbose_name_plural = "modern6 Agency Store Profiles"

    @property
    def user(self): return self.tenant_identity.user

    @property
    def agency_name(self): return self.tenant_identity.agency_name

    @property
    def agency_slug(self): return self.tenant_identity.agency_slug

    def __str__(self):
        return f"{self.tenant_identity.agency_name} — Real Estate Control Deck"


# ==============================================================================
# 📁 DYNAMIC CHILD LAYER REPEATING CONTENT NODES (MODERN6 APP SCOPE)
# ==============================================================================

class Modern6PropertyCategory(models.Model):
    """
    🗂️ USER-MANAGED DYNAMIC PROPERTY CATEGORIES
    Allows merchants and agency owners to spawn custom categories from the admin dashboard
    (e.g., 'Luxury Villa', 'Premium Penthouse', 'Duplex Shells') with zero hardcoding.
    """
    store = models.ForeignKey('Modern6AgencyStoreFront', on_delete=models.CASCADE, related_name='agency_categories')
    category_name = models.CharField(max_length=100, verbose_name="Category/House Type Title")
    category_slug = models.SlugField(max_length=120, help_text="e.g., luxury-villa, penthouse")

    class Meta:
        unique_together = ('store', 'category_slug')
        verbose_name = "modern6 Property Category Slot"
        verbose_name_plural = "modern6 Property Category Slots"

    def __str__(self):
        return f"{self.category_name} — {self.store.tenant_identity.agency_name}"


class Modern6PropertyListing(models.Model):
    """
    📸 SHOWCASE VAULT FOR REPEATING PROPERTY CARDS WITH BACKEND NEON GLOW EFFECTS
    Links directly to your user-managed dynamic categories table row seamlessly.
    """
    store = models.ForeignKey('Modern6AgencyStoreFront', on_delete=models.CASCADE, related_name='agency_properties')
    property_title = models.CharField(max_length=150, verbose_name="Property Title")

    # 🟢 DYNAMIC CONNECTION: Swapped the hardcoded tuple choice list for a live ForeignKey lookup connection!
    dynamic_category = models.ForeignKey(
        Modern6PropertyCategory,
        on_delete=models.PROTECT,
        related_name='listed_houses',
        verbose_name="House Type Category"
    )

    location_city = models.CharField(max_length=120, default="Lekki, Lagos",
                                     help_text="e.g., Miami, Florida or Lekki, Lagos")
    price_numeric = models.DecimalField(max_digits=12, decimal_places=2, default=25000000.00,
                                        help_text="For behind-the-scenes filtering operations")
    price_display_label = models.CharField(max_length=100, default="₦25M - ₦50M",
                                           help_text="e.g., $800k - $2M or ₦25M - ₦50M")

    # Visual Media Assets
    property_thumbnail = models.ImageField(upload_to='modern6_properties/',
                                           help_text="Upload property card render mockup picture")
    property_details_text = models.TextField(
        default="Premium architectural luxury asset equipped with modern high-tier residential structures and secure property parameters.",
        verbose_name="Detailed Property Description",
        help_text="Write out the full description details for this house card to display on its detail page."
    )
    # 🎨 AMBIENT NEON GLOW CONTROLLER EFFECT: Lets admins pick custom backlighting style hooks
    GLOW_EFFECT_CHOICES = [
        ('glow-orange', 'Radiant Sunset Orange Glow'),
        ('glow-blue', 'Electric Cyan Blue Glow'),
        ('glow-purple', 'Cyber Neon Purple Glow'),
    ]
    ambient_glow_color = models.CharField(max_length=30, choices=GLOW_EFFECT_CHOICES, default='glow-orange')

    class Meta:
        verbose_name = "modern6 Property Listing Card"
        verbose_name_plural = "modern6 Property Listing Cards"

    def __str__(self):
        return f"{self.property_title} [{self.dynamic_category.category_name}]"


class Modern6TourAppointment(models.Model):
    """
    📥 CLIENT REAL ESTATE TOUR TOUR SCHEDULER
    Captures luxury bento search criteria metrics and details automatically.
    """
    store = models.ForeignKey('Modern6AgencyStoreFront', on_delete=models.CASCADE, related_name='agency_tours')
    client_name = models.CharField(max_length=120)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=30)

    # Search parameters context capture fields
    requested_location = models.CharField(max_length=150)
    requested_house_type = models.CharField(max_length=100)
    requested_price_range = models.CharField(max_length=100)

    tour_date = models.CharField(max_length=100, help_text="Tour scheduling date picked from front deck")
    client_message = models.TextField(blank=True, verbose_name="Additional Brief Notes")

    is_confirmed = models.BooleanField(default=False, verbose_name="Processed / Booked")
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-logged_at']
        verbose_name = "modern6 Property Tour Booking"
        verbose_name_plural = "modern6 Property Tour Bookings"

    def __str__(self):
        return f"Tour Request: {self.client_name} -> {self.requested_house_type}"
