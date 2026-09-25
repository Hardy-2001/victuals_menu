from django.contrib import admin
from .models import (
    Modern10CarTenant,
    Modern10CarStoreFront,
    Modern10CarCategory,
    Modern10CarListing,
    Modern10CarBlogArticle,
    Modern10NewsletterSubscription,
    Modern10StudioTeamMember,
    Modern10CarTestimonial
)

@admin.register(Modern10CarTenant)
class Modern10CarTenantAdmin(admin.ModelAdmin):
    """
    🔒 MULTI-TENANT AUTOMOTIVE IDENTITY VAULT FOR MODERN10
    Onboarding field agents can only spawn and view car dealer identities
    linked directly to their account, with zero deletion privileges!
    """
    list_display = ('business_name', 'slug_name', 'user', 'assigned_agent', 'created_at')
    search_fields = ('business_name', 'slug_name', 'user__username')
    list_filter = ('created_at',)

    def get_queryset(self, request):
        """🔒 DATA ISOLATION SHIELD: Regular agents only see car profiles they onboarded"""
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
# 👑 AUTOMOTIVE HUB CONTROL DECK VISUAL PROFILE MASTER CONTROLLER
# ==============================================================================

@admin.register(Modern10CarStoreFront)
class Modern10CarStoreFrontAdmin(admin.ModelAdmin):
    """
    👑 PREMIUM CONTROL DECK MARKETER PANEL FOR MODERN10
    Groups brand headers, showroom parameters, landing texts, and hero banners.
    """
    list_display = ('__str__', 'contact_email', 'contact_phone', 'initialized_at')
    search_fields = ('tenant_identity__business_name', 'tenant_identity__slug_name')
    list_filter = ('initialized_at',)

    # 🟢 CAR CORE FIELDSETS GRID: Controls car marketplace texts from admin layout cards
    fieldsets = (
        ('🔒 Isolated Dealer Identity Link', {
            'fields': ('tenant_identity', 'logo')
        }),
        ('📞 Showroom Communications Radar', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('🎨 Home Page Hero Vehicle Accents', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_banner_image')
        }),
        # 🟢 UPDATED: Integrated strategic statements and live counters into the corporate profile fields deck cards!
        ('📝 Corporate Profile About Content Blocks', {
            'fields': (
                'about_headline',
                'about_description_copy',
                'about_mission_text',
                'about_vision_text',
                'stats_vehicles_count',
                'stats_sales_count',
                'stats_reviews_count',
                'stats_clients_count'
            )
        }),
        ('🛡️ Why Choose Us Custom Features (Dynamic Pillars)', {
            'fields': (
                'why_choose_us_intro',
                'pillar_1_title',
                'pillar_2_title',
                'pillar_3_title',
                'pillar_4_title'
            )
        }),
        ('🛠️ Core Platform Service Offers Window', {
            'fields': (
                'service_1_desc',
                'service_2_desc',
                'service_3_desc',
                'service_4_desc'
            )
        }),
        ('👑 Core Brand Features & Showcase Accents', {
            'fields': (
                'feature_main_headline',
                'feature_desc_paragraph_1',
                'feature_desc_paragraph_2',
                'feature_badge_1',
                'feature_badge_2',
                'feature_badge_3',
                'feature_badge_4'
            )
        }),
        ('🌐 Merchant Social Media Network Links', {
            'fields': (
                'facebook_url',
                'twitter_url',
                'instagram_url'
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
            kwargs["queryset"] = Modern10CarTenant.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 👥 USER-MANAGED CORPORATE TEAM PROFILE MATRIX CONTROL INTERFACE
# ==============================================================================

@admin.register(Modern10StudioTeamMember)
class Modern10StudioTeamMemberAdmin(admin.ModelAdmin):
    """
    👥 TEAM MEMBER MARKETER BOARD
    Handles secure dealer-isolated updates for corporate showroom team profiles.
    """
    list_display = ('member_name', 'member_role', 'store')
    search_fields = ('member_name', 'member_role', 'store__tenant_identity__business_name')
    list_filter = ('member_role',)

    fields = ('store', 'member_name', 'member_role', 'member_avatar')

    def get_queryset(self, request):
        """🔒 MERCHANT ISOLATION SHIELD: Users only filter their own team items"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 FORMFIELD SHIELD: Restricts store storefront options to matching user row rows"""
        if db_field.name == "store" and not request.user.is_superuser:
            kwargs["queryset"] = Modern10CarStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Modern10CarTestimonial)
class Modern10CarTestimonialAdmin(admin.ModelAdmin):
    """
    💬 DYNAMIC TESTIMONIAL CAROUSEL ADMIN
    Manages customer sliding reviews, company designations, and profile avatars.
    """
    list_display = ('client_name', 'client_role', 'store')
    search_fields = ('client_name', 'client_role', 'store__tenant_identity__business_name')

    def get_queryset(self, request):
        """🔒 USER ISOLATION SHIELD: Merchants only filter their own client testimonial items"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 FORMFIELD SHIELD: Ensures stores options stay within credential sandboxes"""
        if db_field.name == "store" and not request.user.is_superuser:
            kwargs["queryset"] = Modern10CarStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 📁 PART 2B: REPEATING CHILD CONTENT GRIDS LAYER CONTROLLERS (CATALOG & MEDIA)
# ==============================================================================

@admin.register(Modern10CarCategory)
class Modern10CarCategoryAdmin(admin.ModelAdmin):
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
            kwargs["queryset"] = Modern10CarStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Modern10CarListing)
class Modern10CarListingAdmin(admin.ModelAdmin):
    """
    🚘 AUTOMOTIVE INVENTORY VEHICLE CATALOG DECK ADMIN
    Manages pricing strategies, custom descriptions, options and stock codes dynamically.
    """
    list_display = ('make_and_model', 'dynamic_category', 'purpose', 'rental_price_per_day', 'sale_price',
                    'is_available', 'store')
    search_fields = ('make_and_model', 'stock_reference', 'vin_registry')
    list_filter = ('dynamic_category', 'purpose', 'is_available', 'is_featured_on_home')

    fields = (
        'store', 'make_and_model', 'dynamic_category', 'purpose',
        'rental_price_per_day', 'sale_price', 'vehicle_image',
        'gallery_image_1', 'gallery_image_2', 'gallery_image_3', 'gallery_image_4',
        'year_of_manufacture', 'mileage', 'transmission_automatic',
        'horsepower', 'fuel_type', 'seating_capacity',

        # 🟢 REGISTERED: These inputs will now automatically populate inside your admin dashboard screens!
        'vehicle_details_text', 'vehicle_features_checklist', 'google_map_embed_url',

        'stock_reference', 'vin_registry', 'showroom_location',
        'is_available', 'is_featured_on_home'
    )

    def get_queryset(self, request):
        """🔒 SEGMENT ISOLATION SHIELD: Limits product visibility to authorized catalog creators"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store" and not request.user.is_superuser:
            kwargs["queryset"] = Modern10CarStoreFront.objects.filter(tenant_identity__user=request.user)

        # FILTERED SEGMENTS DROPDOWN PICKER: Locks choices inside the merchant's sandbox
        if db_field.name == "dynamic_category" and not request.user.is_superuser:
            kwargs["queryset"] = Modern10CarCategory.objects.filter(store__tenant_identity__user=request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Modern10CarBlogArticle)
class Modern10CarBlogArticleAdmin(admin.ModelAdmin):
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
            kwargs["queryset"] = Modern10CarStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 📥 PART 2C: INBOUND AUTOMOTIVE CLIENT NEWSLETTER REGISTER MAILBOX DESK
# ==============================================================================

@admin.register(Modern10NewsletterSubscription)
class Modern10NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber_email', 'subscribed_at', 'store')
    readonly_fields = ('store', 'subscriber_email', 'subscribed_at')
    search_fields = ('subscriber_email',)

    def get_queryset(self, request):
        """🔒 LEAKAGE COUNTER INTELLIGENCE: Protects incoming customer email addresses"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)
