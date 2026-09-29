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

# ==============================================================================
# 🔒 PART 1A: MULTI-TENANT ISOLATED IDENTITY VAULT MASTER CONTROLLER
# ==============================================================================

@admin.register(Modern11SalonTenant)
class Modern11SalonTenantAdmin(admin.ModelAdmin):
    """
    🔒 SALON MULTI-TENANT IDENTITY BANK FOR MODERN11
    Enforces strict access constraints: Agents can only ADD and VIEW identity records
    linked directly to their own account profiles, with zero edit handle tampering or removal!
    """
    list_display = ('business_name', 'slug_name', 'user', 'assigned_agent', 'created_at')
    search_fields = ('business_name', 'slug_name', 'user__username')
    list_filter = ('created_at',)

    def get_queryset(self, request):
        """🔒 DATA ISOLATION SHIELD: Only display salon tenants onboarded by this agent"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(assigned_agent__user=request.user)

    def save_model(self, request, obj, form, change):
        """🏷️ AUTOMATED SIGNATURE ENGINE: Stamped with agent profile codes on record save"""
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
# 👑 PART 1B: VISUAL MARKET DECK SETTINGS CONTROLLER (SALON STOREFRONT)
# ==============================================================================

@admin.register(Modern11SalonStoreFront)
class Modern11SalonStoreFrontAdmin(admin.ModelAdmin):
    """
    👑 SALON MARKETING DASHBOARD VISUAL CONTROL PANEL FOR MODERN11
    Manages global tenant headers, visual features, campaigns, and retail switches.
    """
    list_display = ('__str__', 'contact_email', 'contact_phone', 'initialized_at')
    search_fields = ('tenant_identity__business_name', 'tenant_identity__slug_name')
    list_filter = ('initialized_at',)

    fieldsets = (
        ('🔒 Core Identity Link', {
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
        """🔒 DATA ISOLATION SHIELD: Field agents only monitor settings they onboarded"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(tenant_identity__assigned_agent__user=request.user)

    def has_add_permission(self, request):
        """🛡️ GENERIC METADATA GATING: Restores agent permission button maps cleanly"""
        if request.user.is_superuser:
            return True
        opts = self.opts
        return request.user.has_perm(f"{opts.app_label}.add_{opts.model_name}")

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    # 🟢 FIXED TENANT DROPDOWN SELECTION FILTER (MATCHES MODERN4 ALIGNMENT LINE-FOR-LINE)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 FORMFIELD PROTECTION: Restricts the selection slot strictly to this agent's clients"""
        if db_field.name == "tenant_identity" and not request.user.is_superuser:
            kwargs["queryset"] = Modern11SalonTenant.objects.filter(assigned_agent__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# ==============================================================================
# 👥 PART 2A: USER-MANAGED SALON BEAUTY EXPERTS ROSTER INTERFACE
# ==============================================================================
# ==============================================================================
# 👥 PART 2A: USER-MANAGED SALON BEAUTY EXPERTS ROSTER INTERFACE
# ==============================================================================

@admin.register(Modern11SalonStylist)
class Modern11SalonStylistAdmin(admin.ModelAdmin):
    """
    👥 STYLIST TEAM CARD REGISTRY
    🔒 DUAL-MODE PRIVACY SHIELD: Automatically balances visibility blocks
    so both field onboarding agents AND individual salon merchants can manage team sheets!
    """
    list_display = ('stylist_name', 'stylist_role', 'store')
    search_fields = ('stylist_name', 'stylist_role', 'store__tenant_identity__business_name')
    list_filter = ('stylist_role',)

    fields = ('store', 'stylist_name', 'stylist_role', 'stylist_avatar', 'stylist_bio_summary')

    def get_queryset(self, request):
        """🔒 DATA ISOLATION: Differentiates records safely based on user credentials"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        # Check if the currently logged-in account has an onboarded agent connection link
        if Modern11SalonTenant.objects.filter(assigned_agent__user=request.user).exists():
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)

        # 🟢 USER PROTECTION GATEWAY: If they are the shop owner, display only their business row!
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 DROP-DOWN PROTECTION: Balances dropdown lists seamlessly for both users and agents"""
        if db_field.name == "store" and not request.user.is_superuser:
            if Modern11SalonTenant.objects.filter(assigned_agent__user=request.user).exists():
                kwargs["queryset"] = Modern11SalonStoreFront.objects.filter(
                    tenant_identity__assigned_agent__user=request.user)
            else:
                # 🟢 MERCHANT FALLBACK ACCENTS: Gives the store user account full authority to view their matching row!
                kwargs["queryset"] = Modern11SalonStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 💰 PART 2B: DYNAMIC BEAUTY TREATMENT PRICING MENU INTERFACE
# ==============================================================================

@admin.register(Modern11SalonService)
class Modern11SalonServiceAdmin(admin.ModelAdmin):
    """
    💰 PRICING MENU DECK INTERFACE
    🔒 DUAL-MODE PRIVACY SHIELD: Ensures the salon user can select their matching store row seamlessly.
    """
    list_display = ('service_title', 'service_price', 'store')
    search_fields = ('service_title', 'store__tenant_identity__business_name')
    list_filter = ('service_price',)

    fields = ('store', 'service_title', 'service_price', 'service_features_list')

    def get_queryset(self, request):
        """🔒 SEGMENT ISOLATION: Filters lists uniformly based on profile context parameters"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        if Modern11SalonTenant.objects.filter(assigned_agent__user=request.user).exists():
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)

        # 🟢 USER PROTECTION GATEWAY: If they are the salon owner, isolate listings to their account profile!
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 FORMFIELD SHIELD: Safely populates options for both merchants and field agents"""
        if db_field.name == "store" and not request.user.is_superuser:
            if Modern11SalonTenant.objects.filter(assigned_agent__user=request.user).exists():
                kwargs["queryset"] = Modern11SalonStoreFront.objects.filter(
                    tenant_identity__assigned_agent__user=request.user)
            else:
                # 🟢 MERCHANT FALLBACK ACCENTS: Restores visibility options for the merchant user account!
                kwargs["queryset"] = Modern11SalonStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 📸 PART 3A: RECENT TREATMENT PORTFOLIO LOOKBOOK GALLERY INTERFACE
# ==============================================================================

@admin.register(Modern11PortfolioWork)
class Modern11PortfolioWorkAdmin(admin.ModelAdmin):
    """
    📸 LOOKBOOK TRANSFORMATION DECK ADMIN
    🔒 DUAL-MODE PRIVACY SHIELD: Dynamically isolates lookbook imagery folders
    for both onboarding staff and terminal shop operators.
    """
    list_display = ('work_title', 'work_category', 'uploaded_at', 'store')
    search_fields = ('work_title', 'store__tenant_identity__business_name')
    list_filter = ('work_category', 'uploaded_at')

    fields = ('store', 'work_title', 'work_category', 'work_image')

    def get_queryset(self, request):
        """🔒 USER ISOLATION: Safely channels data visibility lines based on credentials"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        if Modern11SalonTenant.objects.filter(assigned_agent__user=request.user).exists():
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)

        # 🟢 USER GATEWAY: Isolate gallery to merchant's private ownership if not an agent
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store" and not request.user.is_superuser:
            if Modern11SalonTenant.objects.filter(assigned_agent__user=request.user).exists():
                kwargs["queryset"] = Modern11SalonStoreFront.objects.filter(
                    tenant_identity__assigned_agent__user=request.user)
            else:
                # 🟢 MERCHANT FALLBACK: Opens up selection for the salon workspace user account
                kwargs["queryset"] = Modern11StoreFront.objects.filter(tenant_identity__user=request.user) if hasattr(
                    views, 'Modern11StoreFront') else Modern11SalonStoreFront.objects.filter(
                    tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 📰 PART 3B: RECENT BEAUTY TRENDS & HEALTHY JOURNALISM POSTS INTERFACE
# ==============================================================================

@admin.register(Modern11SalonBlogArticle)
class Modern11SalonBlogArticleAdmin(admin.ModelAdmin):
    """
    📰 BEAUTY JOURNAL POSTS ADMIN MODULE
    🔒 DUAL-MODE PRIVACY SHIELD: Balances editorial entry locks smoothly for agents and store profiles.
    """
    list_display = ('article_title', 'author_display_name', 'published_date', 'store')
    search_fields = ('article_title', 'author_display_name')
    list_filter = ('published_date',)

    fields = ('store', 'article_title', 'author_display_name', 'article_thumbnail', 'article_summary',
              'article_body_content')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        if Modern11SalonTenant.objects.filter(assigned_agent__user=request.user).exists():
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)

        # 🟢 USER GATEWAY: Isolate logs to merchant profile account
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store" and not request.user.is_superuser:
            if Modern11SalonTenant.objects.filter(assigned_agent__user=request.user).exists():
                kwargs["queryset"] = Modern11SalonStoreFront.objects.filter(
                    tenant_identity__assigned_agent__user=request.user)
            else:
                # 🟢 MERCHANT FALLBACK: Unlocks dropdown visibility fields for the private dealer user profile
                kwargs["queryset"] = Modern11SalonStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 🛍️ PART 3C: PREMIUM MULTI-TENANT COSMETICS RETAIL SHOP PRODUCTS INTERFACE
# ==============================================================================

@admin.register(Modern11SalonProduct)
class Modern11SalonProductAdmin(admin.ModelAdmin):
    """
    🛍️ SALON SHOP PRODUCT RETAIL ADMIN
    🔒 DUAL-MODE PRIVACY SHIELD: Complete store dropdown flexibility for both merchant user profiles and field staff.
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
        """🔒 DATA ISOLATION SHIELD: Safely restricts product views dynamically based on role logs"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        if Modern11SalonTenant.objects.filter(assigned_agent__user=request.user).exists():
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)

        # 🟢 USER GATEWAY: Isolate products strictly to the merchant store operator's private inventory
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 FORMFIELD SHIELD: Dynamically isolates selection dropdown items with 100% bug-free accuracy"""
        if db_field.name == "store" and not request.user.is_superuser:
            if Modern11SalonTenant.objects.filter(assigned_agent__user=request.user).exists():
                kwargs["queryset"] = Modern11SalonStoreFront.objects.filter(
                    tenant_identity__assigned_agent__user=request.user)
            else:
                # 🟢 MERCHANT FALLBACK: Restores complete dropdown creation rights for the private merchant account profile!
                kwargs["queryset"] = Modern11SalonStoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
