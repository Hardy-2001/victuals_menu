from django.contrib import admin
from .models import Modern2SlugTenant, RestaurantProfile, RestaurantCategory, FoodMenuItem

@admin.register(Modern2SlugTenant)
class Modern2SlugTenantAdmin(admin.ModelAdmin):
    """
    🔒 MODERN2 RESTAURANT IDENTITY VAULT
    Enforces a strict operational gate: Field Agents can only ADD and VIEW
    identity rows to generate restaurant slugs, with zero editing or deletion access!
    """
    list_display = ('restaurant_name', 'restaurant_slug', 'user', 'assigned_agent', 'created_at')
    search_fields = ('restaurant_name', 'restaurant_slug', 'user__username')
    list_filter = ('created_at',)

    def get_queryset(self, request):
        """🔒 AGENT ISOLATION: Only show restaurant tenants onboarded by this agent natively"""
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


@admin.register(RestaurantProfile)
class RestaurantProfileAdmin(admin.ModelAdmin):
    """
    🍔 CHOWDECK-INSPIRED FOOD STREAM METADATA PROFILE
    """
    list_display = ('__str__', 'cuisine_type', 'delivery_time_range', 'is_restaurant_active')
    search_fields = ('restaurant_identity__restaurant_name', 'restaurant_identity__restaurant_slug')
    list_filter = ('is_restaurant_active', 'cuisine_type')

    fieldsets = (
        ('🔒 Core Identity Link', {'fields': ('restaurant_identity',)}),
        ('🎨 Brand Visuals', {'fields': ('restaurant_logo', 'restaurant_cover_photo')}),
        ('📝 Metrics & Status Badges', {'fields': ('cuisine_type', 'delivery_time_range', 'rating_display_text', 'operational_status_lbl')}),
        ('🏙️ Corporate Footer Details', {'fields': ('footer_phone_line', 'footer_physical_address', 'is_restaurant_active')}),
    )

    def get_queryset(self, request):
        """🔒 AGENT ISOLATION: Only see profiles belonging to your onboarded list"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(restaurant_identity__assigned_agent__user=request.user)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        opts = self.opts
        return request.user.has_perm(f"{opts.app_label}.add_{opts.model_name}")

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 DROP-DOWN FILTER: Restricts selection choices to only show this agent's clients"""
        if db_field.name == "restaurant_identity" and not request.user.is_superuser:
            kwargs["queryset"] = Modern2SlugTenant.objects.filter(assigned_agent__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(RestaurantCategory)
class RestaurantCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'sort_order')
    list_filter = ('restaurant',)
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(restaurant__restaurant_identity__assigned_agent__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "restaurant" and not request.user.is_superuser:
            kwargs["queryset"] = RestaurantProfile.objects.filter(restaurant_identity__assigned_agent__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(FoodMenuItem)
class FoodMenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available')
    list_filter = ('is_available', 'category__restaurant', 'category')
    search_fields = ('name', 'description')

    fieldsets = (
        ('🍛 Dish Specifications', {'fields': ('category', 'name', 'price', 'image')}),
        ('📝 Content & Kitchen Availability', {'fields': ('description', 'is_available')}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(category__restaurant__restaurant_identity__assigned_agent__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category" and not request.user.is_superuser:
            kwargs["queryset"] = RestaurantCategory.objects.filter(restaurant__restaurant_identity__assigned_agent__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
