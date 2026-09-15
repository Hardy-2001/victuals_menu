from django.db import models
from django.contrib.auth.models import User


# =========================================================================
# 🏢 APP LEVEL SAAS FURNITURE REGISTRY & ACCENTS
# =========================================================================

class Modern8FurnitureTenant(models.Model):
    """
    🗄️ ISOLATED MODERN8 FURNITURE IDENTITY VAULT
    Anchors core credentials, unique studio slugs, and owner linking with agent tracking.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User Account")
    studio_name = models.CharField(max_length=120, unique=True, verbose_name="Furniture Studio Name")
    studio_slug = models.SlugField(max_length=120, unique=True, help_text="e.g., premium-furni, luxury-living")

    # 👑 THE AGENT ANCHOR COLUMN: Links this studio workspace back to the onboarding field agent profile!
    assigned_agent = models.ForeignKey(
        'super_admin.AgentProfile',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='modern8_onboarded_studios',
        help_text="The field agent tracking this premium furniture profile registry",
        verbose_name="Assigned Agent"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "modern8 Furniture Tenant"
        verbose_name_plural = "modern8 Furniture Tenants"

    def __str__(self):
        return f"{self.studio_name} ({self.studio_slug})"


class Modern8FurnitureStoreFront(models.Model):
    """
    💎 PREMIUM FURNITURE APP VISUAL CONTROL DECK FOR MODERN8
    Houses global brand headers, hero text banners, about blocks, contact indices,
    and dynamic 'Why Choose Us' feature columns.
    """
    tenant_identity = models.OneToOneField(
        Modern8FurnitureTenant,
        on_delete=models.CASCADE,
        related_name='studio_profile',
        verbose_name="SaaS Identity Link",
        null=True,
        blank=True
    )

    # Global Communication Default Fallbacks
    studio_email = models.EmailField(default="hello@furni.corex.ng")
    studio_hotline = models.CharField(max_length=30, default="+234 (0) 900 800 7000")
    studio_showroom_address = models.CharField(max_length=255,
                                               default="Block 12, Admiralty Way, Lekki Phase 1, Lagos, Nigeria")
    studio_logo = models.ImageField(upload_to='modern8_studio_logos/', blank=True, null=True)

    # Main Hero Showcase Accents (Home Page Layout)
    hero_headline_title = models.CharField(max_length=255, default="Modern Interior Design Studio")
    hero_subhead_copy = models.TextField(
        default="Donec vitae odio quis nisl dapibus malesuada. Nullam ac aliquet velit.")
    hero_banner_image = models.ImageField(upload_to='modern8_studio_heros/', blank=True, null=True)

    # Modular Content Block: About Us & Services Accent Data
    about_headline = models.CharField(max_length=255, default="Crafted with excellent material.")
    about_description_copy = models.TextField(
        default="Donec vitae odio quis nisl dapibus malesuada. Nullam ac aliquet velit.")
    about_showcase_thumbnail = models.ImageField(upload_to='modern8_about/', blank=True, null=True)

    # 🟢 DYNAMIC "WHY CHOOSE US" CONTENT NODES
    why_choose_us_intro = models.TextField(
        default="Donec vitae odio quis nisl dapibus malesuada. Nullam ac aliquet velit.",
        verbose_name="Why Choose Us Description")

    pillar_1_title = models.CharField(max_length=100, default="Fast & Free Shipping")
    pillar_1_copy = models.TextField(default="Donec vitae odio quis nisl dapibus malesuada. Nullam ac aliquet velit.")

    pillar_2_title = models.CharField(max_length=100, default="Easy to Shop")
    pillar_2_copy = models.TextField(default="Donec vitae odio quis nisl dapibus malesuada. Nullam ac aliquet velit.")

    pillar_3_title = models.CharField(max_length=100, default="24/7 Support")
    pillar_3_copy = models.TextField(default="Donec vitae odio quis nisl dapibus malesuada. Nullam ac aliquet velit.")

    pillar_4_title = models.CharField(max_length=100, default="Hassle Free Returns")
    pillar_4_copy = models.TextField(default="Donec vitae odio quis nisl dapibus malesuada. Nullam ac aliquet velit.")

    initialized_at = models.DateTimeField(auto_now_add=True)



    # 🟢 DYNAMIC "SERVICES PAGE ROW 1" CONTENT NODES


    service_pillar_1_title = models.CharField(max_length=100, default="Fast & Free Shipping")
    service_pillar_1_copy = models.TextField(default="Get your furniture delivered to your door quickly without any extra delivery fees.")

    service_pillar_2_title = models.CharField(max_length=100, default="Easy to Shop")
    service_pillar_2_copy = models.TextField(default="Browse through our showroom catalog online and select your items with ease.")

    service_pillar_3_title = models.CharField(max_length=100, default="24/7 Support")
    service_pillar_3_copy = models.TextField(default="Our dedicated sales team is always active to answer all your inquiries instantly.")

    service_pillar_4_title = models.CharField(max_length=100, default="Hassle Free Returns")
    service_pillar_4_copy = models.TextField(default="Enjoy peace of mind with our stress-free return policy if items do not match.")

    # 🟢 DYNAMIC "SERVICES PAGE ROW 2" CONTENT NODES
    service_pillar_5_title = models.CharField(max_length=100, default="Custom Fabrication")
    service_pillar_5_copy = models.TextField(default="We build unique furniture tailored specifically to your exact home dimensions.")

    service_pillar_6_title = models.CharField(max_length=100, default="Interior Consults")
    service_pillar_6_copy = models.TextField(default="Our design architects help choose materials and maximize your room layout efficiency.")

    service_pillar_7_title = models.CharField(max_length=100, default="Premium Assembly")
    service_pillar_7_copy = models.TextField(default="Our direct team handles unpacking, fitting, and complete installation at your site.")

    service_pillar_8_title = models.CharField(max_length=100, default="Lifetime Warranty")
    service_pillar_8_copy = models.TextField(default="Rest easy knowing all structural materials come with premium protective coverage.")


    class Meta:
        ordering = ['-initialized_at']
        verbose_name = "modern8 Furniture Store Profile"
        verbose_name_plural = "modern8 Furniture Store Profiles"

    @property
    def user(self): return self.tenant_identity.user

    @property
    def studio_name(self): return self.tenant_identity.studio_name

    @property
    def studio_slug(self): return self.tenant_identity.studio_slug

    def __str__(self):
        return f"{self.tenant_identity.studio_name} — Furniture Control Deck"

# =========================================================================
# 🟢 PART 1B: DYNAMIC REPEATING SECTIONS LAYER TABLES
# =========================================================================

class Modern8StudioTeamMember(models.Model):
    """
    👥 USER-MANAGED CORPORATE TEAM PROFILE MATRIX
    Allows agents and business owners to manage their staff roster directly from the admin panel.
    """
    store = models.ForeignKey(Modern8FurnitureStoreFront, on_delete=models.CASCADE, related_name='studio_team_members')
    member_name = models.CharField(max_length=120, verbose_name="Full Name")
    member_role = models.CharField(max_length=120, verbose_name="Corporate Designation", help_text="e.g., CEO, Founder, Senior Decorator")
    member_avatar = models.ImageField(upload_to='modern8_team/', verbose_name="Profile Picture")
    member_bio_short = models.TextField(default="Separated they live in Bookmarksgrove right at the coast of the Semantics.", verbose_name="Short Biography")

    class Meta:
        verbose_name = "modern8 Studio Team Member Card"
        verbose_name_plural = "modern8 Studio Team Member Cards"

    def __str__(self):
        return f"{self.member_name} ({self.member_role}) — {self.store.tenant_identity.studio_name}"


class Modern8FurnitureTestimonial(models.Model):
    """
    💬 CUSTOMER TESTIMONIAL CAROUSEL
    Handles sliding client quotes, corporate roles, and profile icons per store dashboard.
    """
    store = models.ForeignKey(Modern8FurnitureStoreFront, on_delete=models.CASCADE, related_name='studio_testimonials')
    client_name = models.CharField(max_length=100, verbose_name="Client Name")
    client_role = models.CharField(max_length=120, verbose_name="Designation/Company", help_text="e.g., CEO, Co-Founder, XYZ Inc.")
    avatar = models.ImageField(upload_to='modern8_avatars/', blank=True, null=True, verbose_name="User Avatar")
    quote = models.TextField(verbose_name="Testimonial Quote Statement")

    class Meta:
        verbose_name = "modern8 Furniture Testimonial"
        verbose_name_plural = "modern8 Furniture Testimonials"

    def __str__(self):
        return f"Review by {self.client_name} — {self.store.tenant_identity.studio_name}"


# =========================================================================
# 🛍️ DYNAMIC CHILD LAYER REPEATING CONTENT NODES
# =========================================================================

class Modern8FurnitureCategory(models.Model):
    """
    📁 USER-MANAGED DYNAMIC FURNITURE SEGMENTS
    Allows owners to spawn custom sections from the admin panel (e.g., Chairs, Sofas, Beds).
    """
    store = models.ForeignKey(Modern8FurnitureStoreFront, on_delete=models.CASCADE, related_name='studio_categories')
    category_name = models.CharField(max_length=100, verbose_name="Category Type Title")
    category_slug = models.SlugField(max_length=120, help_text="e.g., luxury-chairs, modern-sofas")

    class Meta:
        unique_together = ('store', 'category_slug')
        verbose_name = "modern8 Furniture Category Slot"
        verbose_name_plural = "modern8 Furniture Category Slots"

    def __str__(self):
        return f"{self.category_name} — {self.store.tenant_identity.studio_name}"


class Modern8FurnitureProductListing(models.Model):
    """
    🛋️ SHOWCASE VAULT FOR REPEATING FURNITURE ITEM CARDS
    Links directly to your shop grid system with dynamic features.
    """
    store = models.ForeignKey(Modern8FurnitureStoreFront, on_delete=models.CASCADE, related_name='studio_products')
    product_title = models.CharField(max_length=150, verbose_name="Product Item Title")
    dynamic_category = models.ForeignKey(
        Modern8FurnitureCategory,
        on_delete=models.PROTECT,
        related_name='listed_furniture',
        verbose_name="Furniture Type Category"
    )

    price_numeric = models.DecimalField(max_digits=12, decimal_places=2, default=50000.00, help_text="Set your retail price tag")
    product_thumbnail = models.ImageField(upload_to='modern8_products/', help_text="Upload crisp product picture")
    product_details_text = models.TextField(default="Premium design crafted with elite wood types and materials.")

    # Feature Toggles
    is_in_stock = models.BooleanField(default=True, verbose_name="Available for Dispatch")
    is_featured_on_home = models.BooleanField(default=False, verbose_name="Showcase in Home Slider Aisle")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "modern8 Furniture Product Listing Card"
        verbose_name_plural = "modern8 Furniture Product Listing Cards"

    def __str__(self):
        return f"{self.product_title} [{self.dynamic_category.category_name}]"


class Modern8FurnitureBlogArticle(models.Model):
    """
    📰 RECENT DESIGN BLOG POSTS MODULE
    Handles corporate article updates to showcase on your landing grids.
    """
    store = models.ForeignKey(Modern8FurnitureStoreFront, on_delete=models.CASCADE, related_name='studio_blogs')
    article_title = models.CharField(max_length=250, verbose_name="Article Title")
    author_display_name = models.CharField(max_length=100, default="")
    article_thumbnail = models.ImageField(upload_to='modern8_blogs/')
    published_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = "modern8 Studio Blog Post"
        verbose_name_plural = "modern8 Studio Blog Posts"

    def __str__(self):
        return f"{self.article_title} by {self.author_display_name}"


class Modern8NewsletterSubscription(models.Model):
    """
    ✉️ CLIENT NEWSLETTER RADAR
    Captures footer customer subscriber details natively.
    """
    store = models.ForeignKey(Modern8FurnitureStoreFront, on_delete=models.CASCADE, related_name='studio_subscribers')
    subscriber_name = models.CharField(max_length=120)
    subscriber_email = models.EmailField()
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "modern8 Newsletter Lead"
        verbose_name_plural = "modern8 Newsletter Leads"

    def __str__(self):
        return f"{self.subscriber_name} ({self.subscriber_email})"
