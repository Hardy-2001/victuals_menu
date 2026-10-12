from django.db import models
from django.contrib.auth.models import User


# =========================================================================
# 🏢 PART 1: MASTER IDENTITY VAULT (EMAIL MARKETING WEBSITE FOCUS)
# =========================================================================

class EmailSenderTenant(models.Model):
    """
    🗄️ ISOLATED EMAIL MARKETING ENTERPRISE IDENTITY VAULT
    Anchors core merchant credentials, unique workspace subdomains, and field agents.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User Account")
    business_name = models.CharField(max_length=120, unique=True, verbose_name="Business Name")
    slug_name = models.SlugField(max_length=120, unique=True, help_text="e.g., mail-click, promo-hub")

    # Links this email hub back to your central platform agent tracking system!
    assigned_agent = models.ForeignKey(
        'super_admin.AgentProfile',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='email_onboarded_hubs',
        help_text="The field agent tracking this premium email sender platform registry",
        verbose_name="Assigned Agent"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Email Sender Tenant"
        verbose_name_plural = "Email Sender Tenants"

    def __str__(self):
        return f"{self.business_name} ({self.slug_name})"


class EmailSenderPlatformProfile(models.Model):
    """
    💎 WEBSITE CONTENT & DYNAMIC CREDENTIALS CONTROL DECK
    🟢 MULTI-TENANT ISOLATED SMTP: Allows each client to input their own personal
    email server credentials right from the dashboard to send branded mail!
    """
    tenant_identity = models.OneToOneField(
        EmailSenderTenant,  # 🟢
        on_delete=models.CASCADE,
        related_name='studio_profile',
        verbose_name="SaaS Identity Link"
    )

    # 📞 Website Content fields manageable per sub-tenant registry
    contact_email = models.EmailField(default="info@corex.ng", verbose_name="Official Support Email")
    contact_phone = models.CharField(max_length=50, default="+234 (0) 803 456 7891", verbose_name="Contact Phone Line")
    contact_address = models.CharField(max_length=255, default="Lekki Phase 1, Lagos, Nigeria",
                                       verbose_name="Physical Depot Address")

    hero_title = models.CharField(max_length=150, default="Join The Insider Club",
                                  verbose_name="Hero Title Main Headline")
    hero_subtitle = models.CharField(max_length=255,
                                     default="Receive luxury product drops, private coupon codes, and flash discounts.",
                                     verbose_name="Hero Subtitle Copy Block")

    # 🎨 DYNAMIC FRONTEND LANDING PAGE APPEARANCE ASSETS
    hero_title = models.CharField(max_length=150, default="Join The Insider Club",
                                  verbose_name="Hero Title Main Headline")
    hero_subtitle = models.CharField(max_length=255,
                                     default="Receive luxury product drops, private coupon codes, and flash discounts.",
                                     verbose_name="Hero Subtitle Copy Block")

    # 🟢 DYNAMIC LAYOUT THEME IMAGE: Lets the admin completely swap the landing page banner graphic!
    landing_page_banner = models.ImageField(
        upload_to='landing_banners/',
        blank=True,
        null=True,
        verbose_name="Landing Page Right Side Image Banner",
        help_text="Upload a lifestyle or branding picture (like the boy and girl looking at phones) to dynamically display on the page background layout."
    )

    # Existing fields remain intact below...


    campaign_limit_per_day = models.IntegerField(default=300, verbose_name="Free Daily Sending Allowance Limit")
    is_active_license = models.BooleanField(default=True, verbose_name="App Subscription Status")

    # =========================================================================
    # 🔐 ISOLATED MERCHANT SMTP PORTAL ACCOUNT KEYS (NO MORE HARDCODING)
    # =========================================================================
    smtp_server_host = models.CharField(max_length=255, default="mail.corex.ng",
                                        verbose_name="Merchant SMTP Host Server")
    smtp_server_port = models.IntegerField(default=465, verbose_name="Merchant SMTP Port Number")
    smtp_account_username = models.CharField(max_length=255, verbose_name="Merchant Sender Email Account (USER)")
    smtp_account_password = models.CharField(max_length=255,
                                             verbose_name="Merchant Sender Password / API Key (PASSWORD)")
    use_secure_ssl = models.BooleanField(default=True, verbose_name="Use Secure SSL Encryption Conn Connection")

    initialized_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-initialized_at']
        verbose_name = "Email Sender Platform Profile"
        verbose_name_plural = "Email Sender Platform Profiles"

    @property
    def user(self): return self.tenant_identity.user

    @property
    def business_name(self): return self.tenant_identity.business_name

    @property
    def slug_name(self): return self.tenant_identity.slug_name

    def __str__(self):
        return f"{self.tenant_identity.business_name} — Mailing Control Deck"


# =========================================================================
# 📨 PART 2: DYNAMIC CAMPAIGN & SUBSCRIBER SCHEMAS
# =========================================================================

class BroadcastCampaignManifest(models.Model):
    """🖼️ DYNAMIC EMAIL CAMPAIGN ARCHIVE MATRIX"""
    STATUS_CHOICES = [
        ('pending', 'Pending Queued Execution'),
        ('processing', 'Actively Dispatched Routing'),
        ('completed', 'Transmission Matrix Success'),
        ('failed', 'System Delivery Failure Breakdown'),
    ]

    profile = models.ForeignKey(EmailSenderPlatformProfile, on_delete=models.CASCADE, related_name='campaigns')
    email_subject_header = models.CharField(max_length=255, verbose_name="Email Subject Line Header")
    product_title_heading = models.CharField(max_length=200, verbose_name="Product Marketing Name / Title")
    product_selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00,
                                                verbose_name="Product Price Tag (₦)")
    broadcast_image_banner = models.ImageField(upload_to='campaign_broadcasts/',
                                               verbose_name="Email Marketing Display Image")
    email_message_description = models.TextField(verbose_name="Campaign Offer / Detailed Product Description Copy")
    custom_destination_url = models.URLField(max_length=500, default="https://corex.ng",
                                             verbose_name="Button Action Destination Redirect Link URL")

    delivery_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending',
                                       verbose_name="Broadcast Delivery State")
    total_recipients_count = models.IntegerField(default=0, verbose_name="Total Targeted Customers Count")
    dispatched_at = models.DateTimeField(auto_now_add=True, verbose_name="Dispatched Timestamp")

    class Meta:
        ordering = ['-dispatched_at']
        verbose_name = "Email Broadcast Campaign"
        verbose_name_plural = "Email Broadcast Campaigns"

    def __str__(self):
        return f"{self.email_subject_header[:30]}... ({self.delivery_status})"


class NewsletterSubscriber(models.Model):
    """👤 PUBLIC WEBSITE CAPTURE RECORD SHEET"""
    tenant = models.ForeignKey(EmailSenderTenant, on_delete=models.CASCADE, related_name='email_subscribers')
    client_full_name = models.CharField(max_length=150, verbose_name="Subscriber Full Name")
    client_email_address = models.EmailField(verbose_name="Verified Customer Email Address")
    is_active_subscription = models.BooleanField(default=True, verbose_name="Subscription Active Status")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Joined Timestamp")

    class Meta:
        ordering = ['-subscribed_at']
        unique_together = ('tenant', 'client_email_address')
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"

    def __str__(self):
        return f"{self.client_full_name} ({self.client_email_address}) — {self.tenant.business_name}"
