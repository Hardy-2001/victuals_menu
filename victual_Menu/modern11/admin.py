from django.contrib import admin
from .models import (
    Modern11SalonTenant,
    Modern11SalonStoreFront,
    Modern11SalonStylist,
    Modern11SalonService,
    Modern11PortfolioWork,
    Modern11SalonBlogArticle,
    Modern11SalonProduct
)

@admin.register(Modern11SalonTenant)
class Modern11SalonTenantAdmin(admin.ModelAdmin):
    """
    🔒 MULTI-TENANT BEAUTY IDENTITY BANK FOR MODERN11
    Onboarding field agents can only spawn and view salon identities
    linked directly to their account, with zero deletion privileges!
    """
    list_display = ('business_name', 'slug_name', 'user', 'assigned_agent', 'created_at')
    search_fields = ('business_name', 'slug_name', 'user__username')
    list_filter = ('created_at',)

    def get_queryset(self, request):
        """🔒 DATA ISOLATION SHIELD: Regular agents only see profiles they onboarded"""
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
        return request.user.is_superuser or (obj is not None and obj.assigned_agent.user == request.user)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


# ==============================================================================
# 👑 SALON VISUAL APP PROFILE DASHBOARD DECK MASTER CONTROLLER
# ==============================================================================

@admin.register(Modern11SalonStoreFront)
class Modern11SalonStoreFrontAdmin(admin.ModelAdmin):
    """
    👑 PREMIUM CONTROL DECK MARKETER PANEL FOR MODERN11
    Groups brand landing layouts, core highlights, performance counters, and coordinates.
    """
    list_display = ('__str__', 'contact_email', 'contact_phone', 'initialized_at')
    search_fields = ('tenant_identity__business_name', 'tenant_identity__slug_name')
    list_filter = ('initialized_at',)

    # 💇‍♀️ SALON FEATURE FIELDSETS LAYOUT CARDS: Maps manage parameters neatly!
    fieldsets = (
        ('🔒 Isolated Salon Identity Link', {
            'fields': ('tenant_identity', 'logo')
        }),
        ('📞 Showroom Communications Radar', {
            'fields': ('contact_phone', 'contact_email', 'contact_address')
        }),
        ('🎨 Home Page Welcome Stage Accents', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_banner_image')
        }),
        ('📝 3-Column Highlight Proposition Badges', {
            'fields': (
                'feature_1_title', 'feature_1_desc',
                'feature_2_title', 'feature_2_desc',
                'feature_3_title', 'feature_3_desc'
            )
        }),
        ('🏢 Corporate Profile Narrative Summary', {
            'fields': ('about_headline', 'about_description_copy', 'about_banner_image')
        }),
        ('🎟️ Flash Special Campaign Strategies', {
            'fields': ('campaign_headline', 'campaign_description')
        }),
        ('📊 Operational Performance Statistics Metrics', {
            'fields': ('stat_makeovers', 'stat_procedures', 'stat_clients', 'stat_treatments')
        }),
        ('🌐 Merchant Social Media Network Links', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url')
        }),
    )

    def get_queryset(self, request):
        """🔒 SUBDOMAIN SECURITY SHIELD: Restricts visibility based on user profile accounts"""
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
        """🔒 DROPDOWN ISOLATION SHIELD: Ensures stores options stay within credential sandboxes"""
        if db_field.name == "tenant_identity" and not request.user.is_superuser:
            kwargs["queryset"] = Modern11SalonTenant.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# ==============================================================================
# 👥 USER-MANAGED SALON BEAUTY EXPERTS ROSTER CONTROL INTERFACE
# ==============================================================================

@admin.register(Modern11SalonStylist)
class Modern11SalonStylistAdmin(admin.ModelAdmin):
    """
    👥 STYLIST TEAM CARD REGISTRY
    Handles secure dealer-isolated updates for showroom hair and aesthetic artists.
    """
    list_display = ('stylist_name', 'stylist_role', 'store')
    search_fields = ('stylist_name', 'stylist_role', 'store__tenant_identity__business_name')
    list_filter = ('stylist_role',)

    fields = ('store', 'stylist_name', 'stylist_role', 'stylist_avatar', 'stylist_bio_summary')

    def get_queryset(self, request):
        """🔒 SHIELDS MERCHANT STORAGE: Users only see and manage their own hair specialists"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 FORMFIELD SHIELD: Restricts salon workspace targets to matching user credentials"""
        if db_field.name == "store" and not request.user.is_superuser:
            kwargs["queryset"] = Modern11SalonStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 💰 DYNAMIC BEAUTY TREATMENT PRICING MENU CONTROL INTERFACE
# ==============================================================================

@admin.register(Modern11SalonService)
class Modern11SalonServiceAdmin(admin.ModelAdmin):
    """
    💰 PRICING MENU DECK INTERFACE
    Manages custom package treatments, prices, and checklist attributes cleanly.
    """
    list_display = ('service_title', 'service_price', 'store')
    search_fields = ('service_title', 'store__tenant_identity__business_name')
    list_filter = ('service_price',)

    fields = ('store', 'service_title', 'service_price', 'service_features_list')

    def get_queryset(self, request):
        """🔒 SEGMENT ISOLATION SHIELD: Limits service parameters to authorized workspace owners"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store" and not request.user.is_superuser:
            kwargs["queryset"] = Modern11SalonStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 📸 RECENT TREATMENT PORTFOLIO LOOKBOOK GALLERY CONTROL INTERFACE
# ==============================================================================

@admin.register(Modern11PortfolioWork)
class Modern11PortfolioWorkAdmin(admin.ModelAdmin):
    """
    📸 LOOKBOOK TRANSFORMATION DECK ADMIN
    Manages lookbook classification grids and image assets without security cross-leaks.
    """
    list_display = ('work_title', 'work_category', 'uploaded_at', 'store')
    search_fields = ('work_title', 'store__tenant_identity__business_name')
    list_filter = ('work_category', 'uploaded_at')

    fields = ('store', 'work_title', 'work_category', 'work_image')

    def get_queryset(self, request):
        """🔒 USER ISOLATION SHIELD: Merchant profiles only filter their own gallery look transformations"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store" and not request.user.is_superuser:
            kwargs["queryset"] = Modern11SalonStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 📰 RECENT BEAUTY TRENDS & HEALTHY JOURNALISM POSTS INTERFACE
# ==============================================================================

@admin.register(Modern11SalonBlogArticle)
class Modern11SalonBlogArticleAdmin(admin.ModelAdmin):
    """
    📰 BEAUTY JOURNAL POSTS ADMIN MODULE
    Handles article summaries and collapsible layout content strings cleanly.
    """
    list_display = ('article_title', 'author_display_name', 'published_date', 'store')
    search_fields = ('article_title', 'author_display_name')
    list_filter = ('published_date',)

    fields = ('store', 'article_title', 'author_display_name', 'article_thumbnail', 'article_summary', 'article_body_content')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store" and not request.user.is_superuser:
            kwargs["queryset"] = Modern11SalonStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 🛍️ PREMIUM BEAUTY RETAIL SHOP PRODUCTS CONTROL INTERFACE
# ==============================================================================

@admin.register(Modern11SalonProduct)
class Modern11SalonProductAdmin(admin.ModelAdmin):
    """
    🛍️ SALON SHOP PRODUCT RETAIL ADMIN
    Manages stock prices, item details, category groups, and homepage display toggles.
    """
    list_display = ('product_name', 'product_category', 'product_price', 'is_featured_on_home', 'is_in_stock', 'store')
    search_fields = ('product_name', 'product_category', 'store__tenant_identity__business_name')
    list_filter = ('product_category', 'is_featured_on_home', 'is_in_stock')

    fields = (
        'store',
        'product_name',
        'product_category',
        'product_price',
        'product_image',
        'product_description',
        'is_featured_on_home',
        'is_in_stock'
    )

    def get_queryset(self, request):
        """🔒 SHIELDS MERCHANT STORAGE: Users only see and manage their own retail goods"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 FORMFIELD SHIELD: Restricts store storefront options to matching user row records"""
        if db_field.name == "store" and not request.user.is_superuser:
            kwargs["queryset"] = Modern11SalonStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
