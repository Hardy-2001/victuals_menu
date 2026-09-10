from django.contrib import admin
from .models import (
    Modern6RealEstateTenant,
    Modern6AgencyStoreFront,
    Modern6PropertyCategory,
    Modern6PropertyListing,
    Modern6TourAppointment
)

# ==============================================================================
# 🔒 PART 1A: MULTI-TENANT ISOLATED SAAS VAULT CONTROLLER
# ==============================================================================

@admin.register(Modern6RealEstateTenant)
class Modern6RealEstateTenantAdmin(admin.ModelAdmin):
    """
    🔒 MULTI-TENANT PROPERTY IDENTITY VAULT FOR MODERN6
    Onboarding field agents can only spawn and view real estate agency identity records
    linked directly to their account, with zero deletion or tampering privileges!
    """
    list_display = ('agency_name', 'agency_slug', 'user', 'assigned_agent', 'created_at')
    search_fields = ('agency_name', 'agency_slug', 'user__username')
    list_filter = ('created_at',)

    def get_queryset(self, request):
        """🔒 DATA ISOLATION SHIELD: Regular agents only see agency profiles they onboarded"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(assigned_agent__user=request.user)

    def save_model(self, request, obj, form, change):
        """🏷️ AUTOMATED SIGNATURE ENGINE: Stamped with agent metadata footprint tags silently"""
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


# ==============================================================================
# 👑 PART 1B: LUXURY AGENCY STOREFRONT MASTER PANEL CONTROLLER
# ==============================================================================

@admin.register(Modern6AgencyStoreFront)
class Modern6AgencyStoreFrontAdmin(admin.ModelAdmin):
    """
    👑 LUXURY MATRIX MARKETING PANEL CONTROLLER FOR MODERN6
    Groups premium brand headers, metadata profiles, counters, and images.
    """
    list_display = ('__str__', 'brokerage_email', 'brokerage_hotline', 'initialized_at')
    search_fields = ('tenant_identity__agency_name', 'tenant_identity__agency_slug')
    list_filter = ('initialized_at',)

    fieldsets = (
        ('🔒 Isolated Agency Identity Link', {
            'fields': ('tenant_identity', 'agency_logo')
        }),
        ('📞 Brokerage Communication Coordinates', {
            'fields': ('brokerage_email', 'brokerage_hotline', 'office_physical_address')
        }),
        ('🎨 Main Luxury Showcase Hero Accents', {
            'fields': ('hero_headline_title', 'hero_subheadline_copy')
        }),
        ('📊 Real-Time Social Proof Performance Counters', {
            'fields': ('count_properties_sold', 'count_active_listings', 'count_verified_brokers')
        }),
    )

    def get_queryset(self, request):
        """🔒 SUBDOMAIN SECURITY SHIELD: Gates visibility based on onboarding agent ownership keys"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(tenant_identity__assigned_agent__user=request.user)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        opts = self.opts
        return request.user.has_perm(f"{opts.app_label}.add_{opts.model_name}")

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 FORMFIELD SAFE DROP-DOWNS: Restricts option dropdown picks exclusively to the agent's account"""
        if db_field.name == "tenant_identity" and not request.user.is_superuser:
            kwargs["queryset"] = Modern6RealEstateTenant.objects.filter(assigned_agent__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 📁 PART 2A: REPEATING CHILD CONTENT GRIDS LAYER CONTROLLERS (REAL ESTATE APP)
# ==============================================================================

@admin.register(Modern6PropertyCategory)
class Modern6PropertyCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_slug', 'store')
    search_fields = ('category_name', 'category_slug')
    prepopulated_fields = {'category_slug': ('category_name',)}

    def get_queryset(self, request):
        """🔒 USER ISOLATION SHIELD: Real estate vendors only see their own category slots"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'agent_profile'):
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 DROP-DOWN PROTECTION: Restricts visual deck options to authorized profile rows"""
        if db_field.name == "store" and not request.user.is_superuser:
            if hasattr(request.user, 'agent_profile'):
                kwargs["queryset"] = Modern6AgencyStoreFront.objects.filter(
                    tenant_identity__assigned_agent__user=request.user)
            else:
                kwargs["queryset"] = Modern6AgencyStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Modern6PropertyListing)
class Modern6PropertyListingAdmin(admin.ModelAdmin):
    list_display = ('property_title', 'dynamic_category', 'location_city', 'price_display_label', 'store')
    search_fields = ('property_title', 'location_city')
    list_filter = ('dynamic_category', 'ambient_glow_color')
    fields = ('store', 'property_title', 'dynamic_category', 'location_city', 'price_numeric', 'price_display_label',
              'property_thumbnail', 'ambient_glow_color', 'property_details_text')
    def get_queryset(self, request):
        """🔒 USER ISOLATION SHIELD: Limits house cards display to the authentic owner or agent"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'agent_profile'):
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store" and not request.user.is_superuser:
            if hasattr(request.user, 'agent_profile'):
                kwargs["queryset"] = Modern6AgencyStoreFront.objects.filter(
                    tenant_identity__assigned_agent__user=request.user)
            else:
                kwargs["queryset"] = Modern6AgencyStoreFront.objects.filter(tenant_identity__user=request.user)

        # 🟢 DROPDOWN PROTECTION: Dynamic Category selection is also filtered to the user's domain row!
        if db_field.name == "dynamic_category" and not request.user.is_superuser:
            if hasattr(request.user, 'agent_profile'):
                kwargs["queryset"] = Modern6PropertyCategory.objects.filter(
                    store__tenant_identity__assigned_agent__user=request.user)
            else:
                kwargs["queryset"] = Modern6PropertyCategory.objects.filter(store__tenant_identity__user=request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 📥 PART 2B: INBOUND CLIENT HOME TOUR REGISTRATION MAILBOX DESK
# ==============================================================================

@admin.register(Modern6TourAppointment)
class Modern6TourAppointmentAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'requested_house_type', 'tour_date', 'is_confirmed', 'store')
    list_editable = ('is_confirmed',)
    readonly_fields = ('store', 'client_name', 'client_email', 'client_phone', 'requested_location',
                       'requested_house_type', 'requested_price_range', 'tour_date', 'client_message', 'logged_at')
    search_fields = ('client_name', 'requested_house_type')

    def get_queryset(self, request):
        """🔒 DATA LEAK PROTECTION: Restricts inbound tour lead bookings to assigned tenants only"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'agent_profile'):
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)
        return qs.filter(store__tenant_identity__user=request.user)

