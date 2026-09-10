from django.db import models
from django.contrib.auth.models import User


class Modern2SlugTenant(models.Model):
    """
    🔒 ISOLATED MODERN2 RESTAURANT IDENTITY VAULT
    Stores the core food vendor user relationships and unique URL routing slugs.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User Account")
    restaurant_name = models.CharField(max_length=120, unique=True, verbose_name="Restaurant Name")
    restaurant_slug = models.SlugField(max_length=120, unique=True, help_text="e.g., foodco-hq")

    # 👑 THE MISSING ARCHITECTURAL ANCHOR LINK COLUMN:
    # Connects your food merchants directly to your field agent table records perfectly!
    assigned_agent = models.ForeignKey(
        'super_admin.AgentProfile',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='modern2_onboarded_vendors',
        help_text="The field agent tracking this premium food user profile account registry"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Modern2 SaaS Tenant"
        verbose_name_plural = "Modern2 SaaS Tenants"

    def __str__(self):
        return f"{self.restaurant_name} ({self.restaurant_slug})"


class RestaurantProfile(models.Model):
    """
    🍔 CHOWDECK-INSPIRED PROFESSIONAL RESTAURANT ENGINE
    Handles elite food stream configurations with complete multi-tenant separation.
    """
    # 🎯 LINKED TO YOUR IDENTITY REGISTRY TABLE
    restaurant_identity = models.OneToOneField(
        Modern2SlugTenant,
        on_delete=models.CASCADE,
        related_name='restaurant_profile',
        verbose_name="SaaS Identity Link",
        null=True,
        blank=True
    )

    # 🎨 Visual Brand Identity Parameters
    restaurant_logo = models.ImageField(
        upload_to='restaurant_logos/',
        blank=True,
        null=True,
        help_text="Upload your official restaurant image icon asset"
    )
    restaurant_cover_photo = models.ImageField(
        upload_to='restaurant_covers/',
        blank=True,
        null=True,
        help_text="The square card display image shown next to restaurant meta details"
    )

    # 📝 Meta Identifiers & Operational Badges
    cuisine_type = models.CharField(max_length=100, default="African Restaurant",
                                    help_text="e.g., African Restaurant, Fast Food, Pastries")
    delivery_time_range = models.CharField(max_length=40, default="15 - 30 mins",
                                           help_text="Estimated preparation and dispatch speed marker")
    rating_display_text = models.CharField(max_length=20, default="4.5 (10k+ ratings)", help_text="e.g., 4.3 (13.1K+)")
    operational_status_lbl = models.CharField(max_length=50, default="OPENS 10:00 AM",
                                              help_text="e.g., CLOSED • OPENS 10:00 AM")

    # 🏙️ Corporate Footer Contact Parameters
    footer_phone_line = models.CharField(max_length=20, default="+234")
    footer_physical_address = models.CharField(max_length=255, default="Lagos, Nigeria")

    is_restaurant_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Professional Restaurant Profile"
        verbose_name_plural = "Professional Restaurant Profiles"

    # 🧠 BACKWARD COMPATIBILITY PROPERTIES:
    @property
    def user(self): return self.restaurant_identity.user

    @property
    def restaurant_name(self): return self.restaurant_identity.restaurant_name

    @property
    def restaurant_slug(self): return self.restaurant_identity.restaurant_slug

    def __str__(self):
        return self.restaurant_identity.restaurant_name

class RestaurantCategory(models.Model):
    """
    📁 CHOWDECK-STYLE STREAM ROW CATEGORY BLOCK
    Organizes menu sections (e.g., Swallow, Rice, Soup, Proteins, Sides, Drinks).
    """
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, related_name='food_categories')
    name = models.CharField(max_length=80)
    sort_order = models.IntegerField(default=0,
                                     help_text="Controls the left-to-right alignment order inside the navigation bar strip")

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = "Restaurant Category"
        verbose_name_plural = "Restaurant Categories"

    def __str__(self):
        return f"{self.name} — {self.restaurant.restaurant_identity.restaurant_name}"


class FoodMenuItem(models.Model):
    """
    🍛 HIGH-DENSITY KITCHEN ITEM NODE
    Stores recipe titles, description blocks, prices, and food thumbnail photos.
    """
    category = models.ForeignKey(RestaurantCategory, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, help_text="Brief ingredient overview or dish explanation")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Set price tag amount in Naira")
    image = models.ImageField(upload_to='menu_food_items/', blank=True, null=True,
                              help_text="Square aspect ratio food image asset")
    is_available = models.BooleanField(default=True, verbose_name="In Kitchen Stock")

    class Meta:
        verbose_name = "Food Menu Item"
        verbose_name_plural = "Food Menu Items"

    def __str__(self):
        return f"{self.name} — ₦{self.price}"
