from django.contrib import admin
from .models import (
    Modern9ApparelTenant,
    Modern9ApparelStoreFront,
    Modern9ApparelCategory,
    Modern9ApparelProductListing,
    Modern9ApparelBlogArticle,
    Modern9ApparelNewsletterLead
)


# ==============================================================================
# 🏢 PART 1: CORE SAAS TENANT IDENTITY & GLOBAL STORE FRONT INTERFACE MAPPERS
# ==============================================================================

@admin.register(Modern9ApparelTenant)
class Modern9ApparelTenantAdmin(admin.ModelAdmin):
    """
    🔐 IDENTITY REGISTRY CONTROLLER
    Maintains official onboarding brand credentials, sub-slugs, and tracking metrics.
    """
    list_display = ('brand_name', 'brand_slug', 'user', 'assigned_agent', 'created_at')
    search_fields = ('brand_name', 'brand_slug', 'user__username', 'assigned_agent__user__username')
    prepopulated_fields = {'brand_slug': ('brand_name',)}

    def get_queryset(self, request):
        """🔒 SUPERUSER ISOLATION: Onboarding field agents only track their own storefront blocks"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(assigned_agent__user=request.user)


@admin.register(Modern9ApparelStoreFront)
class Modern9ApparelStoreFrontAdmin(admin.ModelAdmin):
    """
    💎 APPAREL PLATFORM VISUAL CONTROL DECK
    Arranges corporate headers, lookbook slideshow graphics, and logistics tracks into blocks.
    """
    list_display = ('brand_name', 'store_email', 'store_hotline', 'initialized_at')

    fieldsets = (
        ('🏢 Core Multi-Tenant Anchor Link', {
            'fields': ('tenant_identity',)
        }),
        ('📞 Communication Profiles & Headlines', {
            'fields': ('store_logo_text', 'store_email', 'store_hotline', 'store_hq_address')
        }),
        ('🎨 Premium Apparel Hero Slideshow Lookbook', {
            'fields': ('hero_title_accent', 'hero_description_copy', 'hero_slide_image')
        }),
        ('📢 Marketing Middle Promotional Divider Ribbon', {
            'fields': ('promo_headline', 'promo_background_image')
        }),
        ('🚚 Dynamic Logistic Partners (6 Independent Marquee Slots)', {
            'fields': ('brand_logo_1', 'brand_logo_2', 'brand_logo_3', 'brand_logo_4', 'brand_logo_5', 'brand_logo_6'),
            'description': 'Upload transparent brand icons to showcase your regional shipping networks cleanly.'
        }),
    )

    def get_queryset(self, request):
        """🔒 USER SANITY SHIELD: Restricts profile management targets strictly to authorized owners"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 TESTING MODE APPLIED: Allows all generated tenant slugs to populate options locally!"""
        if db_field.name == "tenant_identity":
            # 🟢 Temporarily bypasses owner-matching restriction so agent01 can configure modern09
            kwargs["queryset"] = Modern9ApparelTenant.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 🛍️ PART 2: DYNAMIC APPAREL CATEGORIES, MERCHANDISE INVENTORIES & LEAD REVIEWS
# ==============================================================================

@admin.register(Modern9ApparelCategory)
class Modern9ApparelCategoryAdmin(admin.ModelAdmin):
    """
    📁 USER-MANAGED SECTIONS MANAGER
    Allows catalog managers to add category spots natively into their store.
    """
    list_display = ('category_name', 'category_slug', 'get_store_brand')
    search_fields = ('category_name', 'category_slug', 'store__tenant_identity__brand_name')
    prepopulated_fields = {'category_slug': ('category_name',)}

    def get_store_brand(self, obj):
        return obj.store.tenant_identity.brand_name
    get_store_brand.short_description = 'Apparel Brand'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)


@admin.register(Modern9ApparelProductListing)
class Modern9ApparelProductListingAdmin(admin.ModelAdmin):
    """
    👗 GARMENT INVENTORY MATRIX PANEL
    Gives direct control over pricing tiers, promo text badges, and feature positions.
    """
    list_display = ('product_title', 'get_category_name', 'current_price', 'old_slashed_price', 'is_popular', 'is_latest', 'is_in_stock')
    list_filter = ('is_popular', 'is_latest', 'is_in_stock', 'dynamic_category')
    search_fields = ('product_title', 'product_details_text', 'store__tenant_identity__brand_name')
    list_editable = ('is_popular', 'is_latest', 'is_in_stock')

    def get_category_name(self, obj):
        return obj.dynamic_category.category_name
    get_category_name.short_description = 'Garment Type'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 TESTING MODE APPLIED: Allows all options to load during local test runs!"""
        if db_field.name == "store":
            # 🟢 Temporarily load all profiles so agent01 can add products to modern09
            kwargs["queryset"] = Modern9ApparelStoreFront.objects.all()
        if db_field.name == "dynamic_category":
            # 🟢 Temporarily load all categories during this local test run
            kwargs["queryset"] = Modern9ApparelCategory.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Modern9ApparelBlogArticle)
class Modern9ApparelBlogArticleAdmin(admin.ModelAdmin):
    """
    📰 LOOKBOOK MAGAZINE CONTROLLER
    Maintains media logs, fashion trend advice, and seasonal lookbook write-ups.
    """
    list_display = ('article_title', 'published_date', 'get_store_brand')
    search_fields = ('article_title', 'article_excerpt', 'store__tenant_identity__brand_name')

    def get_store_brand(self, obj):
        return obj.store.tenant_identity.brand_name
    get_store_brand.short_description = 'Apparel Brand'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)


@admin.register(Modern9ApparelNewsletterLead)
class Modern9ApparelNewsletterLeadAdmin(admin.ModelAdmin):
    """
    ✉️ PROSPECTIVE CLIENT MAILBOX DIRECTORY
    Tracks captured customer email addresses with timestamp references cleanly.
    """
    list_display = ('subscriber_email', 'subscribed_at', 'get_store_brand')
    search_fields = ('subscriber_email', 'store__tenant_identity__brand_name')
    readonly_fields = ('subscriber_email', 'subscribed_at', 'store')

    def get_store_brand(self, obj):
        return obj.store.tenant_identity.brand_name
    get_store_brand.short_description = 'Apparel Brand'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__tenant_identity__user=request.user)

