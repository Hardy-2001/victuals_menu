from django.contrib import admin
from .models import (
    Modern8FurnitureTenant,
    Modern8FurnitureStoreFront,
    Modern8FurnitureCategory,
    Modern8FurnitureProductListing,
    Modern8FurnitureBlogArticle,
    Modern8NewsletterSubscription,
    Modern8StudioTeamMember,       # 🟢 IMPORTED FOR DYNAMIC TEAM SHOWCASE PANEL
    Modern8FurnitureTestimonial    # 🟢 IMPORTED FOR DYNAMIC CLIENT REVIEWS SLIDER
)

@admin.register(Modern8FurnitureTenant)
class Modern8FurnitureTenantAdmin(admin.ModelAdmin):
    """
    🔒 MULTI-TENANT FURNITURE IDENTITY VAULT FOR MODERN8
    Onboarding field agents can only spawn and view furniture studio identity records
    linked directly to their account, with zero deletion or tampering privileges!
    """
    list_display = ('studio_name', 'studio_slug', 'user', 'assigned_agent', 'created_at')
    search_fields = ('studio_name', 'studio_slug', 'user__username')
    list_filter = ('created_at',)

    def get_queryset(self, request):
        """🔒 DATA ISOLATION SHIELD: Regular agents only see furniture profiles they onboarded"""
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
# 👑 PART 1B: STUDIO CONTROL DECK VISUAL PROFILE MASTER CONTROLLER
# ==============================================================================

@admin.register(Modern8FurnitureStoreFront)
class Modern8FurnitureStoreFrontAdmin(admin.ModelAdmin):
    """
    👑 PREMIUM CONTROL DECK MARKETER PANEL FOR MODERN8
    Groups brand aesthetics, color overlays, addresses, and banner assets neatly.
    """
    list_display = ('__str__', 'studio_email', 'studio_hotline', 'initialized_at')
    search_fields = ('tenant_identity__studio_name', 'tenant_identity__studio_slug')
    list_filter = ('initialized_at',)

    # 🟢 EXPANDED FIELDSETS GRID: Controls all marketing text lanes dynamically from your admin cards!
    fieldsets = (
        ('🔒 Isolated Studio Identity Link', {
            'fields': ('tenant_identity', 'studio_logo')
        }),
        ('📞 Corporate Communications Radar', {
            'fields': ('studio_email', 'studio_hotline', 'studio_showroom_address')
        }),
        ('🎨 Main Hero Accent Settings', {
            'fields': ('hero_headline_title', 'hero_subhead_copy', 'hero_banner_image')
        }),
        ('📝 Modular About Page Content Cores', {
            'fields': ('about_headline', 'about_description_copy', 'about_showcase_thumbnail')
        }),
        ('🛡️ Why Choose Us Custom Features (Dynamic Pillars)', {
            'fields': (
                'why_choose_us_intro',
                'pillar_1_title', 'pillar_1_copy',
                'pillar_2_title', 'pillar_2_copy',
                'pillar_3_title', 'pillar_3_copy',
                'pillar_4_title', 'pillar_4_copy'
            )
        }),
        # 🟢 THE REQUESTED SEPARATE GRIDS: Controls all 8 columns on the services template dynamically!
        ('🛠️ Services Page Dynamic Highlight Grid (8 Independent Pillars)', {
            'fields': (
                'service_pillar_1_title', 'service_pillar_1_copy',
                'service_pillar_2_title', 'service_pillar_2_copy',
                'service_pillar_3_title', 'service_pillar_3_copy',
                'service_pillar_4_title', 'service_pillar_4_copy',
                'service_pillar_5_title', 'service_pillar_5_copy',
                'service_pillar_6_title', 'service_pillar_6_copy',
                'service_pillar_7_title', 'service_pillar_7_copy',
                'service_pillar_8_title', 'service_pillar_8_copy',
            )
        }),

    )

    def get_queryset(self, request):
        """🔒 SUBDOMAIN SECURITY SHIELD: Restricts visibility based on tenant account permissions"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(tenant_identity__user=request.user)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        opts = self.opts
        return request.user.has_perm(f"{opts.app_label}.add_{opts.model_name}")

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 FORMFIELD PROTECTION: Locks target options strictly to rows matching active credentials"""
        if db_field.name == "tenant_identity" and not request.user.is_superuser:
            kwargs["queryset"] = Modern8FurnitureTenant.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# ==============================================================================
# 🟢 PART 2A: NEW SEPARATE CONTROLLERS FOR REPEATING GRIDS (TEAM & TESTIMONIALS)
# ==============================================================================

@admin.register(Modern8StudioTeamMember)
class Modern8StudioTeamMemberAdmin(admin.ModelAdmin):
    """
    👥 DYNAMIC TEAM CARDS DECK ADMIN
    Allows onboarding agents and studio owners to register their active executives.
    """
    list_display = ('member_name', 'member_role', 'store')
    search_fields = ('member_name', 'member_role', 'store__tenant_identity__studio_name')

    def get_queryset(self, request):
        """🔒 USER ISOLATION SHIELD: Regular managers only see team cards belonging to their sandbox"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 PROTECTED DROPDOWN PICKER: Blocks visual crossover selection targets"""
        if db_field.name == "store" and not request.user.is_superuser:
            kwargs["queryset"] = Modern8FurnitureStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Modern8FurnitureTestimonial)
class Modern8FurnitureTestimonialAdmin(admin.ModelAdmin):
    """
    💬 DYNAMIC TESTIMONIAL CAROUSEL ADMIN
    Manages customer sliding reviews, company designations, and profile avatars.
    """
    list_display = ('client_name', 'client_role', 'store')
    search_fields = ('client_name', 'client_role', 'store__tenant_identity__studio_name')

    def get_queryset(self, request):
        """🔒 USER ISOLATION SHIELD: Merchants only filter their own client testimonial items"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 FORMFIELD SHIELD: Ensures stores options stay within credential sandboxes"""
        if db_field.name == "store" and not request.user.is_superuser:
            kwargs["queryset"] = Modern8FurnitureStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 📁 PART 2B: REPEATING CHILD CONTENT GRIDS LAYER CONTROLLERS (CATALOG & MEDIA)
# ==============================================================================

@admin.register(Modern8FurnitureCategory)
class Modern8FurnitureCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_slug', 'store')
    search_fields = ('category_name', 'category_slug')
    prepopulated_fields = {'category_slug': ('category_name',)}

    def get_queryset(self, request):
        """🔒 USER ISOLATION SHIELD: Merchant profiles only filter their own category segments"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 DROPDOWN DROPOUT SHIELD: Blocks visual crossover select targets"""
        if db_field.name == "store" and not request.user.is_superuser:
            kwargs["queryset"] = Modern8FurnitureStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Modern8FurnitureProductListing)
class Modern8FurnitureProductListingAdmin(admin.ModelAdmin):
    list_display = ('product_title', 'dynamic_category', 'price_numeric', 'is_in_stock', 'is_featured_on_home', 'store')
    search_fields = ('product_title',)
    list_filter = ('dynamic_category', 'is_in_stock', 'is_featured_on_home')
    fields = ('store', 'product_title', 'dynamic_category', 'price_numeric', 'product_thumbnail',
              'product_details_text', 'is_in_stock', 'is_featured_on_home')

    def get_queryset(self, request):
        """🔒 SEGMENT ISOLATION SHIELD: Limits product visibility to authorized catalog creators"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store" and not request.user.is_superuser:
            kwargs["queryset"] = Modern8FurnitureStoreFront.objects.filter(tenant_identity__user=request.user)

        # FILTERED SEGMENTS DROPDOWN PICKER: Locks choices inside the merchant's sandbox
        if db_field.name == "dynamic_category" and not request.user.is_superuser:
            kwargs["queryset"] = Modern8FurnitureCategory.objects.filter(store__tenant_identity__user=request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Modern8FurnitureBlogArticle)
class Modern8FurnitureBlogArticleAdmin(admin.ModelAdmin):
    list_display = ('article_title', 'author_display_name', 'published_date', 'store')
    search_fields = ('article_title', 'author_display_name')
    list_filter = ('published_date',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store" and not request.user.is_superuser:
            kwargs["queryset"] = Modern8FurnitureStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 📥 PART 2C: INBOUND CLIENT NEWSLETTER REGISTER MAILBOX DESK
# ==============================================================================

@admin.register(Modern8NewsletterSubscription)
class Modern8NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber_name', 'subscriber_email', 'subscribed_at', 'store')
    readonly_fields = ('store', 'subscriber_name', 'subscriber_email', 'subscribed_at')
    search_fields = ('subscriber_name', 'subscriber_email')

    def get_queryset(self, request):
        """🔒 LEAKAGE COUNTER INTELLIGENCE: Protects incoming customer email addresses"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)
