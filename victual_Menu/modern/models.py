from django.db import models
from django.contrib.auth.models import User


class ModernSlugTenant(models.Model):
    """
    🔒 ISOLATED MODERN TIER IDENTITY VAULT
    Stores the core merchant user relationship and the unique URL custom slug handle.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User Account")
    store_name = models.CharField(max_length=120, unique=True, verbose_name="Business Name")
    custom_slug = models.SlugField(max_length=120, unique=True, help_text="e.g., alpha-fitness-hub")

    # 👑 THE MISSING ARCHITECTURAL ANCHOR LINK COLUMN:
    # Connects your gym merchants directly to your field agent table records perfectly!
    assigned_agent = models.ForeignKey(
        'super_admin.AgentProfile',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='modern_onboarded_vendors',
        help_text="The field agent tracking this premium user profile account registry"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Modern SaaS Tenant"
        verbose_name_plural = "Modern SaaS Tenants"

    def __str__(self):
        return f"{self.store_name} ({self.custom_slug})"


class ModernStoreFront(models.Model):
    """
    💎 NEXT-GENERATION MULTI-TIER ENTERPRISE SAAS SYSTEM
    Houses visual profiles, layouts, and communication coordinates.
    """
    LAYOUT_CHOICES = [
        ('MINIMALIST', 'Minimalist Tech Hub (Gadgets & Gear)'),
        ('LUXURY_DARK', 'Midnight Premium Suite (Gold & Charcoal)'),
        ('CREATIVE_VIBE', 'Neon Pop Creative (Streetwear & Cafes)'),
        ('GYM_FITNESS', 'Iron Pulse Suite (Gym Gear & Instructor Booking)')
    ]

    # 🎯 LINKED TO YOUR IDENTITY REGISTRY TABLE
    tenant_identity = models.OneToOneField(
        ModernSlugTenant,
        on_delete=models.CASCADE,
        related_name='modern_profile',
        verbose_name="SaaS Identity Link",
        null=True,
        blank=True
    )

    # 🎨 Visual Parameter Fields
    layout_theme = models.CharField(max_length=25, choices=LAYOUT_CHOICES, default='MINIMALIST')
    primary_brand_color = models.CharField(max_length=10, default="#000000",
                                           help_text="Hex color code for your main text headings and elements")
    custom_hero_banner = models.ImageField(upload_to='modern_banners/', blank=True, null=True,
                                           help_text="Wide top banner backdrop graphic card")

    # Dynamic Merchant Brand Logo file loader!
    store_logo = models.ImageField(
        upload_to='modern_logos/',
        blank=True,
        null=True,
        help_text="Upload your official brand logo image to display directly below the store name header row"
    )

    # Premium Video Feature Assets
    promo_video_url = models.URLField(blank=True, null=True,
                                      help_text="Link your TikTok, YouTube showcase, or raw mp4 product display clip")
    enable_video_autoplay = models.BooleanField(default=False)

    # Fitness & Operational Booking Features
    enable_instructor_booking = models.BooleanField(
        default=False,
        help_text="🎯 OPTIONAL: Toggle to activate a private 'Book a Gym Instructor/Director' registration shelf for clients"
    )
    instructor_hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=5000.00,
        help_text="The consulting or personal training session booking fee baseline"
    )

    # 📱 Contact Coordinates & Tracking
    whatsapp_dispatch_number = models.CharField(max_length=20, default="234")
    business_biography = models.TextField(blank=True,
                                          help_text="Brief headline slogan displayed inside the hero banner image overlay")

    # Completely separate text field for the long-form About page!
    about_message = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed company profile, mission statement, or store history displayed exclusively on the About Us page"
    )
    is_premium_active = models.BooleanField(default=True)
    initialized_at = models.DateTimeField(auto_now_add=True)

    # 🏙️ PREMIUM INTEGRATED FOOTER FIELDS
    footer_phone = models.CharField(max_length=20, default="+234",
                                    help_text="Store contact line displayed in the footer")
    footer_address = models.CharField(max_length=255, default="Lagos, Nigeria",
                                      help_text="Physical store location address text string")

    # 📲 Social Media Handle Text Rails
    instagram_username = models.CharField(max_length=100, blank=True, null=True,
                                          help_text="Username only (e.g., frankling_fitness)")
    whatsapp_link_number = models.CharField(max_length=20, blank=True, null=True,
                                            help_text="WhatsApp contact line (e.g., 23480...)")
    tiktok_username = models.CharField(max_length=100, blank=True, null=True, help_text="TikTok handle username only")

    # Facebook Handle Tracking Column!
    facebook_username = models.CharField(max_length=100, blank=True, null=True,
                                         help_text="Facebook username or page handle only")

    class Meta:
        ordering = ['-initialized_at']
        verbose_name = "Modern Store Profile"
        verbose_name_plural = "Modern Store Profiles"

    # 🧠 BACKWARD COMPATIBILITY PROPERTIES:
    # These map the old fields onto the new table so none of your existing views or loops break!
    @property
    def user(self): return self.tenant_identity.user
    @property
    def store_name(self): return self.tenant_identity.store_name
    @property
    def custom_slug(self): return self.tenant_identity.custom_slug

    def __str__(self):
        return f"{self.tenant_identity.store_name} [{self.layout_theme}]"


class ModernCategory(models.Model):
    """
    📁 MODERN PREMIUM CATEGORY TABLE
    Organizes high-end shop sections (e.g., Gym Equipment, Supplements, Apparels).
    """
    store = models.ForeignKey(ModernStoreFront, on_delete=models.CASCADE, related_name='modern_categories')
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Modern Category"
        verbose_name_plural = "Modern Categories"

    def __str__(self):
        return f"{self.name} — {self.store.tenant_identity.store_name}"


class ModernProductItem(models.Model):
    """
    🛍️ GLOBAL NEXT-GEN ITEMS MATRIX
    Handles high-resolution showcase pictures, pricing, and custom product labels.
    """
    category = models.ForeignKey(ModernCategory, on_delete=models.CASCADE, related_name='modern_products')
    name = models.CharField(max_length=120)
    brand_or_manufacturer = models.CharField(max_length=60, blank=True, null=True,
                                             help_text="e.g., Nike, Gymshark, Optimum Nutrition")
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Set your retail price tag")
    image = models.ImageField(upload_to='modern_products/', blank=True, null=True,
                              help_text="Upload crisp, high-resolution product images")
    description = models.TextField(blank=True, help_text="Detailed overview layout explanation of item metrics")
    unit_specification = models.CharField(max_length=50, blank=True, null=True,
                                          help_text="e.g., 20KG Pair, 60 Capsules, 2.2L Jug")
    is_in_stock = models.BooleanField(default=True, verbose_name="Available for Dispatch")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Modern Product Item"
        verbose_name_plural = "Modern Product Items"

    def __str__(self):
        return f"{self.name} — ₦{self.price}"
