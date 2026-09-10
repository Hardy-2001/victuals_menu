from django.contrib import admin
from .models import ModernSlugTenant, ModernStoreFront, ModernCategory, ModernProductItem

@admin.register(ModernSlugTenant)
class ModernSlugTenantAdmin(admin.ModelAdmin):
    """
    🔒 MODERN TIER IDENTITY VAULT
    Enforces a strict operational gate: Field Agents can only ADD and VIEW
    identity rows to generate slugs, with zero editing or deletion access!
    """
    list_display = ('store_name', 'custom_slug', 'user', 'assigned_agent', 'created_at')
    search_fields = ('store_name', 'custom_slug', 'user__username')
    list_filter = ('created_at',)

    def get_queryset(self, request):
        """🔒 AGENT ISOLATION: Only show tenants onboarded by this agent natively"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(assigned_agent__user=request.user)

    def save_model(self, request, obj, form, change):
        """🏷️ AUTOMATED AGENT SIGNATURE STAMP"""
        if not request.user.is_superuser and not change:
            agent_prof = getattr(request.user, 'agent_profile', None)
            if agent_prof:
                obj.assigned_agent = agent_prof
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


@admin.register(ModernStoreFront)
class ModernStoreFrontAdmin(admin.ModelAdmin):
    """
    👑 PREMIUM APP VISUAL CONTROL DECK
    """
    list_display = ('__str__', 'layout_theme', 'enable_instructor_booking', 'is_premium_active', 'initialized_at')
    list_filter = ('layout_theme', 'enable_instructor_booking', 'is_premium_active')
    search_fields = ('tenant_identity__store_name', 'tenant_identity__custom_slug')

    fieldsets = (
        ('🔒 Core Identity Link', {'fields': ('tenant_identity',)}),
        ('🎨 Visual Theme Profile', {'fields': ('layout_theme', 'primary_brand_color', 'custom_hero_banner', 'store_logo')}),
        ('🎥 High-End Media Assets', {'fields': ('enable_video_autoplay',)}),
        ('💪 Fitness Service Parameters', {'fields': ('enable_instructor_booking', 'instructor_hourly_rate')}),
        ('📱 Communication & About Profiles', {'fields': ('whatsapp_dispatch_number', 'business_biography', 'about_message', 'is_premium_active')}),
        ('🏙️ Premium Corporate Footer Panel', {'fields': ('footer_phone', 'footer_address', 'instagram_username', 'facebook_username', 'whatsapp_link_number', 'tiktok_username')}),
    )

    def get_queryset(self, request):
        """🔒 AGENT ISOLATION: Only see storefront profiles belonging to your onboarded list"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(tenant_identity__assigned_agent__user=request.user)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return request.user.has_perm('modern.add_modernstorefront')

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 DROP-DOWN FILTER: Restricts selection choices to only show this agent's clients"""
        if db_field.name == "tenant_identity" and not request.user.is_superuser:
            kwargs["queryset"] = ModernSlugTenant.objects.filter(assigned_agent__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ModernCategory)
class ModernCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'store')
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__assigned_agent__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store" and not request.user.is_superuser:
            kwargs["queryset"] = ModernStoreFront.objects.filter(tenant_identity__assigned_agent__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ModernProductItem)
class ModernProductItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'unit_specification', 'is_in_stock')
    list_filter = ('is_in_stock', 'category')
    search_fields = ('name', 'brand_or_manufacturer')

    fieldsets = (
        ('🛍️ General Specs', {'fields': ('category', 'name', 'brand_or_manufacturer', 'price')}),
        ('📸 Media Assets', {'fields': ('image',)}),
        ('📝 Description & State', {'fields': ('unit_specification', 'description', 'is_in_stock')}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(category__store__tenant_identity__assigned_agent__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category" and not request.user.is_superuser:
            kwargs["queryset"] = ModernCategory.objects.filter(store__tenant_identity__assigned_agent__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
