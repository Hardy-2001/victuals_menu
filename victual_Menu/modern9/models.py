from django.db import models
from django.contrib.auth.models import User

# =========================================================================
# 🏢 APP LEVEL SAAS APPAREL REGISTRY & BRAND IDENTITY VAULTS
# =========================================================================

class Modern9ApparelTenant(models.Model):
    """
    🗄️ ISOLATED MODERN9 TAILSTORE IDENTITY SYSTEM
    Anchors owner linking, unique clothing shop subdomains, and tracking agent stats.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Store Owner Account")
    brand_name = models.CharField(max_length=120, unique=True, verbose_name="Apparel Brand Name")
    brand_slug = models.SlugField(max_length=120, unique=True, help_text="e.g., tailstore-lekki, urban-threads")
    assigned_agent = models.ForeignKey(
        'super_admin.AgentProfile',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='modern9_onboarded_shops',
        verbose_name="Assigned Field Agent"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "modern9 Apparel Tenant"
        verbose_name_plural = "modern9 Apparel Tenants"

    # 🟢 FIXED: Bulletproof direct text translation string for admin dropdown matching matrices
    def __str__(self):
        return str(self.brand_name)


class Modern9ApparelStoreFront(models.Model):
    """
    💎 PREMIUM TAILSTORE VISUAL CONSOLE CORE
    Houses global brand typography assets, communication metrics, hero slideshow sliders,
    and brand logo marquee sliders.
    """
    tenant_identity = models.OneToOneField(
        Modern9ApparelTenant,
        on_delete=models.CASCADE,
        related_name='store_profile',
        verbose_name="SaaS Identity Link"
    )

    # Store Communication Defaults
    store_email = models.EmailField(default="support@tailstore.corex.ng")
    store_hotline = models.CharField(max_length=30, default="+234 (0) 800 900 1000")
    store_hq_address = models.CharField(max_length=255, default="123 Street Name, Lagos, Nigeria")
    store_logo_text = models.CharField(max_length=50, default="TailStore")

    # Homepage Hero Banner Slideshow
    hero_title_accent = models.CharField(max_length=100, default="Women")
    hero_description_copy = models.TextField(default="Experience the best in sportswear with our latest collection.")
    hero_slide_image = models.ImageField(upload_to='modern9_heros/', blank=True, null=True)

    # Marketing Middle Promo Banner Ribbon
    promo_headline = models.CharField(max_length=255, default="Welcome to Our Shop")
    promo_background_image = models.ImageField(upload_to='modern9_promos/', blank=True, null=True)

    # DYNAMIC "DISCOVER OUR BRANDS" LOGO ROLLING CAROUSEL IMAGES
    brand_logo_1 = models.ImageField(upload_to='modern9_brands/', blank=True, null=True, verbose_name="Brand Logo 1 (e.g. PHP)")
    brand_logo_2 = models.ImageField(upload_to='modern9_brands/', blank=True, null=True, verbose_name="Brand Logo 2 (e.g. React)")
    brand_logo_3 = models.ImageField(upload_to='modern9_brands/', blank=True, null=True, verbose_name="Brand Logo 3 (e.g. Tailwind)")
    brand_logo_4 = models.ImageField(upload_to='modern9_brands/', blank=True, null=True, verbose_name="Brand Logo 4 (e.g. TS)")
    brand_logo_5 = models.ImageField(upload_to='modern9_brands/', blank=True, null=True, verbose_name="Brand Logo 5 (e.g. HTML5)")
    brand_logo_6 = models.ImageField(upload_to='modern9_brands/', blank=True, null=True, verbose_name="Brand Logo 6 (e.g. JS)")

    initialized_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-initialized_at']
        verbose_name = "modern9 Apparel Store Profile"
        verbose_name_plural = "modern9 Apparel Store Profiles"

    @property
    def user(self): return self.tenant_identity.user

    @property
    def brand_name(self): return self.tenant_identity.brand_name

    @property
    def brand_slug(self): return self.tenant_identity.brand_slug

    # 🟢 FIXED: Safe conditional string rendering avoiding object lookup crashes
    def __str__(self):
        return f"{self.tenant_identity.brand_name} — Apparel Control Deck" if self.tenant_identity else "Unlinked Store Front Profile"
# =========================================================================
# 🛍️ DYNAMIC CHILD LAYER REPEATING CONTENT NODES (CATALOG & MEDIA)
# =========================================================================

class Modern9ApparelCategory(models.Model):
    """
    📁 USER-MANAGED BRAND SEGMENTS
    Allows owners to spawn custom sections from the admin panel (e.g., Men, Women, Accessories).
    """
    store = models.ForeignKey(Modern9ApparelStoreFront, on_delete=models.CASCADE, related_name='shop_categories')
    category_name = models.CharField(max_length=100, verbose_name="Category Name")
    category_slug = models.SlugField(max_length=120, help_text="e.g., men-apparel, active-women")
    category_image = models.ImageField(upload_to='modern9_categories/', blank=True, null=True,
                                       help_text="Upload grid display banner")

    class Meta:
        unique_together = ('store', 'category_slug')
        verbose_name = "modern9 Apparel Category Slot"
        verbose_name_plural = "modern9 Apparel Category Slots"

    # 🟢 FIXED: Safe string fallback to cleanly format section options
    def __str__(self):
        brand = self.store.tenant_identity.brand_name if self.store and self.store.tenant_identity else "Unknown"
        return f"{self.category_name} — {brand}"


class Modern9ApparelProductListing(models.Model):
    """
    👗 SHOWCASE VAULT FOR CLOTHING CARD ITEMS
    Links directly to your TailStore grid views with price comparison markdowns.
    """
    store = models.ForeignKey(Modern9ApparelStoreFront, on_delete=models.CASCADE, related_name='shop_products')
    product_title = models.CharField(max_length=150, verbose_name="Product Item Title")
    dynamic_category = models.ForeignKey(
        Modern9ApparelCategory,
        on_delete=models.PROTECT,
        related_name='listed_apparel',
        verbose_name="Garment Type Category"
    )

    current_price = models.DecimalField(max_digits=12, decimal_places=2, default=29.99,
                                        help_text="Active retail price tag")
    old_slashed_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True,
                                            help_text="Optional cross-out original price (e.g. $49.99)")

    product_thumbnail = models.ImageField(upload_to='modern9_products/',
                                          help_text="Upload crisp product thumbnail picture")
    product_details_text = models.TextField(default="Premium retail quality apparel crafted with elite fabric strands.")

    # Product Segment Toggles
    is_popular = models.BooleanField(default=False, verbose_name="Display in Popular Products Grid")
    is_latest = models.BooleanField(default=True, verbose_name="Display in Latest Products Grid")
    is_in_stock = models.BooleanField(default=True, verbose_name="Available for Dispatch")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "modern9 Apparel Product Listing Card"
        verbose_name_plural = "modern9 Apparel Product Listing Cards"

    # 🟢 FIXED: Streamlined item text layout tracking
    def __str__(self):
        brand = self.store.tenant_identity.brand_name if self.store and self.store.tenant_identity else "Unknown"
        return f"{self.product_title} — {brand}"

class Modern9ApparelBlogArticle(models.Model):
    """
    📰 RECENT MAGAZINE LOOKBOOK POSTS
    Handles fashion trends update articles to showcase on your landing boards.
    """
    store = models.ForeignKey(Modern9ApparelStoreFront, on_delete=models.CASCADE, related_name='shop_blogs')
    article_title = models.CharField(max_length=250, verbose_name="Magazine Article Title")
    article_excerpt = models.TextField(default="Explore the hottest style trends of the active design season.")
    article_thumbnail = models.ImageField(upload_to='modern9_blogs/')
    published_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = "modern9 Studio Blog Post"
        verbose_name_plural = "modern9 Studio Blog Posts"

    # 🟢 FIXED: Direct string fallback for lookup paths
    def __str__(self):
        brand = self.store.tenant_identity.brand_name if self.store and self.store.tenant_identity else "Unknown"
        return f"{self.article_title} — {brand}"


class Modern9ApparelNewsletterLead(models.Model):
    """
    ✉️ PROSPECTIVE CLIENT MAILBOX DIRECTORY
    Captures footer discount subscription inputs natively.
    """
    store = models.ForeignKey(Modern9ApparelStoreFront, on_delete=models.CASCADE, related_name='shop_subscribers')
    subscriber_email = models.EmailField()
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "modern9 Newsletter Lead"
        verbose_name_plural = "modern9 Newsletter Leads"

    # 🟢 FIXED: Direct text mapping for list rows
    def __str__(self):
        brand = self.store.tenant_identity.brand_name if self.store and self.store.tenant_identity else "Unknown"
        return f"{self.subscriber_email} — {brand}"
