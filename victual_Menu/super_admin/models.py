from django.db import models
from django.contrib.auth.models import User


class AgentProfile(models.Model):
    """
    💼 STATE AGENT SYSTEM IDENTIFICATION PROFILE
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_profile')
    agent_code = models.CharField(max_length=15, unique=True,
                                  help_text="Unique Identification Code (e.g., ABUJA01, ENUGU05)")
    assigned_state = models.CharField(max_length=40, help_text="Primary deployment operational zone")
    phone_number = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Field Agent Profile"
        verbose_name_plural = "Field Agent Profiles"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.agent_code}) - 📍 {self.assigned_state}"


class PlatformSetting(models.Model):
    """
    👑 DEVELOPER SUPER ADMIN MASTER SETTINGS
    Controls the high-tech server console landing page properties globally.
    """
    admin_phone = models.CharField(max_length=20, default="2349020425819", help_text="Your developer calling line")
    admin_whatsapp = models.CharField(max_length=20, default="2349020425819",
                                      help_text="Your developer destination order link line")
    mock_rented_shops_base = models.IntegerField(default=14,
                                                 help_text="Base number of shops rented to display on marketing layouts (Editable)")
    #    # 👑 THE AUTOMATED SERVER COMPONENT IMAGE VAULT:
    # Hosts your 10 interactive theme-shifting background layer graphics natively!
    server_state_default = models.ImageField(upload_to='server_states/', blank=True, null=True,
                                             help_text="🛡️ STATE 1: Base Default Server Console Image (e.g., Matrix Green)")
    server_state_blue = models.ImageField(upload_to='server_states/', blank=True, null=True,
                                          help_text="⚡ STATE 2: Shield Intercept Image (e.g., Tactical Cobalt Blue)")
    server_state_purple = models.ImageField(upload_to='server_states/', blank=True, null=True,
                                            help_text="🔮 STATE 3: Core Overload Image (e.g., Deep Citadel Purple)")
    server_state_emerald = models.ImageField(upload_to='server_states/', blank=True, null=True,
                                             help_text="💎 STATE 4: System Locked Image (e.g., Emerald Guard Green)")
    server_state_amber = models.ImageField(upload_to='server_states/', blank=True, null=True,
                                           help_text="🔥 STATE 5: Thermal Overclock Image (e.g., Cyberpunk Amber Orange)")

    # 🟢 EXTRA 5 REQUISITIONS BACKGROUND IMAGE FIELDS (Brings your total up to 10 image slots!)
    server_state_six = models.ImageField(upload_to='server_states/', blank=True, null=True,
                                         help_text="📡 STATE 6: Core Matrix Extension Image Shard")
    server_state_seven = models.ImageField(upload_to='server_states/', blank=True, null=True,
                                           help_text="🌌 STATE 7: Deep Cosmic Eclipse Image Shard")
    server_state_eight = models.ImageField(upload_to='server_states/', blank=True, null=True,
                                           help_text="🛡️ STATE 8: Perimeter Firewall Security Image Shard")
    server_state_nine = models.ImageField(upload_to='server_states/', blank=True, null=True,
                                          help_text="⚡ STATE 9: Quantum Network Grid Image Shard")
    server_state_ten = models.ImageField(upload_to='server_states/', blank=True, null=True,
                                         help_text="💎 STATE 10: Supreme Enterprise Protocol Image Shard")


    # 🟢 NEW: DYNAMIC HEADER NAVIGATION DRAWERS VALUE STREAMS
    services_text = models.TextField(
        default="▪️ CORE ENGINE ONBOARDING: Fast automation scripts for store creation.\n▪️ COMPREHENSIVE MEDICAL SUITE: Dynamic scheduling, specialist rosters, and intake management.",
        help_text="Line-separated text list of platform operational services for the header nav dropdown drawer panel."
    )
    security_text = models.TextField(
        default="🔒 FIREWALL GATEWAY: Real-time traffic monitoring filtering matrix entries.\n🔒 AGENT ISOLATION: Strict cryptographic boundaries protecting merchant datasets.",
        help_text="Infrastructure security guidelines, firewall policies, or network certifications text configuration."
    )
    about_text = models.TextField(
        default="This platform functions as a robust multi-tenant enterprise orchestration dashboard designed to provision data-isolated clinical and business store fronts natively.",
        help_text="Brief corporate developer synopsis, mission statement, or platform specifications description text."
    )
    # 🎯 ADD THIS TO YOUR PlatformSetting MODEL INSIDE super_admin/models.py:
    platform_logo = models.ImageField(
        upload_to='platform_branding/',
        blank=True,
        null=True,
        help_text="Upload a premium translucent PNG logo to display beside Corex Server."
    )

    class Meta:
        verbose_name = "Master SaaS Platform Setting"
        verbose_name_plural = "Master SaaS Platform Settings"

    def __str__(self):
        return "Global SaaS Marketing Configurations"

class ShowcaseTemplate(models.Model):
    """
    💡 DYNAMIC MARKETING SHOWCASE BULB NODES
    """
    label_name = models.CharField(max_length=30, help_text="e.g., DINER MENU, BELLMED CLINIC")
    showcase_image = models.ImageField(upload_to='templates_gallery/', help_text="Upload the main screenshot mockup")

    # 🌐 NEW FIELD: Paste the exact live link of the sub-website here!
    live_site_url = models.URLField(max_length=500, blank=True, null=True,
                                    help_text="Paste the live preview link (e.g., http://127.0.0)")

    class Meta:
        verbose_name = "Showcase Template Card"
        verbose_name_plural = "Showcase Template Cards"

    def __str__(self):
        return self.label_name
class InfrastructureMailLog(models.Model):
    """
    📬 INBOUND CONSOLE MAIL PROTOCOL LOGS
    Saves incoming console emails directly into the super admin vault.
    """
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    message_body = models.TextField()
    logged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Core Infrastructure Mail"
        verbose_name_plural = "Core Infrastructure Mails"
        ordering = ['-logged_at']

    def __str__(self):
        return f"Mail from {self.sender_name} — {self.logged_at.strftime('%Y-%m-%d %H:%M')}"


class UserBillingNotice(models.Model):
    """
    👑 SUPER ADMIN PRIVATE PAYMENT CONTROLLER MODEL
    """
    merchant_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='super_billing_notices')
    bank_name = models.CharField(max_length=100, help_text="Your master corporate receiving bank name")
    account_number = models.CharField(max_length=20, help_text="Your main corporate account numbers line")
    account_name = models.CharField(max_length=150, help_text="Your corporate bank account name")
    subscription_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_instructions = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Billing Notice"
        verbose_name_plural = "User Billing Notices"

    def __str__(self):
        return f"Billing Notice — {self.merchant_user.username}"

    from django.db import models

class DomainEngine(models.Model):
    APP_CHOICES = [
        ('store', '🍉 LIST_STORE (Menu App)'),
        ('modern', '💪 LIST_MODERN (Gym App)'),
        ('modern2', '🍔 LIST_MODERN2 (Restaurant App)'),
        ('modern3', '🏥 LIST_MODERN3 (Hospital App)'),
        ('modern4', '❤️ LIST_MODERN4 (LoveCare App)'),
        ('modern5', '🎨 LIST_MODERN5 (Portfolio App)'),
        ('modern6', '🏡 LIST_MODERN6 (Homeland App)'),
        ('modern7', '🎓 LIST_MODERN7 (School App)'),
        ('modern8',' 🏡 LIST_MODERN8 (Funiture App'),
        ('modern9',' 🏡 LIST_MODERN9 (fashion App'),
    ]

    slug_name = models.CharField(max_length=100, unique=True,
                                 help_text="The lowercase subdomain text (e.g., foodco, bellmed)")
    app_target = models.CharField(max_length=20, choices=APP_CHOICES, default='modern5',
                                  help_text="Choose which list routing engine this belongs to")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Domain Engine Router"
        verbose_name_plural = "Domain Engine Routers"

    def __str__(self):
        return f"{self.slug_name} ➔ {self.app_target}"

