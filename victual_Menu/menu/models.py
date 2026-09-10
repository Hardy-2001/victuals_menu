from django.db import models
from django.contrib.auth.models import User

class Tenant(models.Model):
    """
    👑 MASTER SAAS CONTROL TABLE
    """
    BUSINESS_CHOICES = [
        ('RESTAURANT', 'Restaurant / Lounge / Bar'),
        ('FASHION', 'Fashion Boutique / Apparel / Store'),
        ('GROCERY', 'Supermarket, Grocery & Pharmacy Operations')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tenant_profile')
    business_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    business_type = models.CharField(max_length=20, choices=BUSINESS_CHOICES, default='RESTAURANT')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # 🎯 LINKED NATIVELY TO SUPER_ADMIN APP: Re-routed foreign link reference safely!
    # 🎯 FIXED: Made completely nullable to allow migrations to pass over old test entries safely!
    assigned_agent = models.ForeignKey(
        'super_admin.AgentProfile',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='onboarded_vendors',
        help_text="The field agent tracking this user account"
    )

    # 💰 VIRTUAL NIGERIAN BANKING BLINKERS
    payment_status = models.CharField(max_length=10, choices=[('UNPAID', '🔴 Unpaid (Expired)'), ('PAID', '🟢 Paid (Active)')],
                                      default='UNPAID', help_text="Blinker indicator status row")
    virtual_account_number = models.CharField(max_length=20, blank=True, default="9920384192", help_text="Unique Providus/Sterling Bank virtual collection card tracking row")
    virtual_bank_name = models.CharField(max_length=30, default="Monnify / Sterling Bank", help_text="Assigned platform bank settlement name")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "SaaS Client Tenant"
        verbose_name_plural = "SaaS Client Tenants"

    def __str__(self):
        return f"{self.business_name} [{self.payment_status}]"


class Category(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categories/', blank=True, null=True, help_text="Upload a banner photo from your computer")
    order = models.IntegerField(default=0)
    whatsapp_number = models.CharField(max_length=20, default="2349020425819", help_text="Enter number with country code, no symbols")

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Categories"
        unique_together = ('tenant', 'name')

    def __str__(self):
        return f"[{self.tenant.business_name}] — {self.name}"


class FoodItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='food_items/', blank=True, null=True, help_text="Upload a dish photo from your computer")
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = "Catalog Item"
        verbose_name_plural = "Items Catalog"

    def __str__(self):
        return f"{self.name} (₦{self.price:,}) — {self.category.tenant.business_name}"


class CustomerFeedback(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='feedbacks')
    RATING_CHOICES = [(i, f"{i} Stars") for i in range(1, 6)]
    table_number = models.CharField(max_length=10, blank=True, null=True, help_text="Optional diner table location")
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    comment = models.TextField(help_text="The core food/experience review text")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Customer Feedback Entries"

    def __str__(self):
        return f"[{self.tenant.business_name}] Table {self.table_number or 'N/A'} - {self.rating} Stars"


class RestaurantProfile(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='profile')
    restaurant_name = models.CharField(max_length=100, default="The Victuals")
    address = models.CharField(max_length=255, default="Somolu, Lagos Mainland", help_text="Physical restaurant location address string")
    logo = models.ImageField(upload_to='branding/', blank=True, null=True, help_text="Upload your venue logo")
    phone_number = models.CharField(max_length=20, default="2349020425819", help_text="For dialing buttons")
    whatsapp_number = models.CharField(max_length=20, default="2349020425819", help_text="For sending order baskets")
    primary_color = models.CharField(max_length=10, default="#dc2626", help_text="Hex color code for pills/buttons")
    outer_bg_color = models.CharField(max_length=10, default="#0c0c0d", help_text="Backdrop margins tone color")
    inner_bg_color = models.CharField(max_length=10, default="#121212", help_text="Inner canvas main background")

    class Meta:
        verbose_name_plural = "Restaurant Configuration Profiles"

    def __str__(self):
        return f"Branding Profile: {self.restaurant_name} ({self.tenant.business_name})"
