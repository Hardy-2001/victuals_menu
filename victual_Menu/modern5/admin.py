from django.contrib import admin
from .models import (
    Modern5PortfolioTenant,
    Modern5VisualDeck,
    Modern5DeveloperSkill,
    Modern5ProjectBentoGrid,
    Modern5ContractMailbox
)

# ==============================================================================
# 🔒 PART 1A: MULTI-TENANT ISOLATED SAAS VAULT CONTROLLER
# ==============================================================================

@admin.register(Modern5PortfolioTenant)
class Modern5PortfolioTenantAdmin(admin.ModelAdmin):
    """
    🔒 MULTI-TENANT PORTFOLIO IDENTITY VAULT FOR MODERN5
    Onboarding field agents can only spawn and view developer identity records
    linked to their account, with zero deletion or tampering privileges!
    """
    list_display = ('developer_name', 'portfolio_slug', 'user', 'assigned_agent', 'created_at')
    search_fields = ('developer_name', 'portfolio_slug', 'user__username')
    list_filter = ('created_at',)

    def get_queryset(self, request):
        """🔒 DATA ISOLATION SHIELD: Regular agents only see developer profiles they onboarded"""
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
# 👑 PART 1B: HIGH-TECH PORTFOLIO VISUAL DESK CONTROL PANEL
# ==============================================================================

# 🎯 REWRITE LINES 35-37 INSIDE modern5/admin.py TO LOOK EXACTLY LIKE THIS:
@admin.register(Modern5VisualDeck)
class Modern5VisualDeckAdmin(admin.ModelAdmin):
    """
    👑 CYBER MATRIX MARKETING PANEL CONTROLLER FOR MODERN5
    """
    # 🟢 FIXED: Changed 'emergency_phone_line' to 'contact_phone_line' to match your model fields perfectly!
    list_display = ('__str__', 'contact_email', 'contact_phone_line', 'initialized_at')
    search_fields = ('tenant_identity__developer_name', 'tenant_identity__portfolio_slug')

    list_filter = ('initialized_at',)

    fieldsets = (
        ('🔒 Isolated Portfolio Identity Link', {
            'fields': ('tenant_identity', 'developer_avatar')
        }),
        ('📞 Cyber Grid Communication Coordinates', {
            'fields': ('contact_email', 'contact_phone_line', 'base_operation_city', 'uptime_status_label')
        }),
        ('🪐 Main Interactive Hero Deck Accents', {
            'fields': ('hero_headline_text', 'hero_subheadline_summary')
        }),
        ('💻 Simulated IDE Console Json Configuration Terminal', {
            'fields': ('ide_window_title', 'ide_custom_json_writeup')
        }),
        ('📊 Real-Time Server Status Performance Counters', {
            'fields': ('count_production_builds', 'count_reusable_modules', 'count_happy_merchants')
        }),
        ('🔗 External Code Repositories & Network Sync Channels', {
            'fields': ('github_url', 'linkedin_url', 'twitter_x_url')
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
            kwargs["queryset"] = Modern5PortfolioTenant.objects.filter(assigned_agent__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# ==============================================================================
# 📁 PART 2A: REPEATING CHILD CONTENT GRIDS LAYER CONTROLLERS (PORTFOLIO APP)
# ==============================================================================

@admin.register(Modern5DeveloperSkill)
class Modern5DeveloperSkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'store')
    search_fields = ('skill_name',)

    def get_queryset(self, request):
        """🔒 USER ISOLATION SHIELD: Regular portfolio vendors only see their own skill records"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'agent_profile'):
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 DROP-DOWN PROTECTION: Restricts visual deck drop-downs strictly to authorized profile rows"""
        if db_field.name == "store" and not request.user.is_superuser:
            if hasattr(request.user, 'agent_profile'):
                kwargs["queryset"] = Modern5VisualDeck.objects.filter(tenant_identity__assigned_agent__user=request.user)
            else:
                kwargs["queryset"] = Modern5VisualDeck.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Modern5ProjectBentoGrid)
class Modern5ProjectBentoGridAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'store')
    search_fields = ('project_title',)

    def get_queryset(self, request):
        """🔒 USER ISOLATION SHIELD: Limits project records display to the authentic owner or agent"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'agent_profile'):
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store" and not request.user.is_superuser:
            if hasattr(request.user, 'agent_profile'):
                kwargs["queryset"] = Modern5VisualDeck.objects.filter(tenant_identity__assigned_agent__user=request.user)
            else:
                kwargs["queryset"] = Modern5VisualDeck.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 📥 PART 2B: INBOUND CLIENT CONTRACT WORK BRIEF LEAD DESK
# ==============================================================================

@admin.register(Modern5ContractMailbox)
class Modern5ContractMailboxAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'project_budget_estimate', 'is_processed', 'store')
    list_editable = ('is_processed',)
    readonly_fields = ('store', 'client_name', 'client_email', 'project_budget_estimate', 'project_brief_body', 'received_at')
    search_fields = ('client_name', 'project_budget_estimate')

    def get_queryset(self, request):
        """🔒 DATA LEAK PROTECTION: Restricts inbound customer contract logs to assigned tenants only"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'agent_profile'):
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)
        return qs.filter(store__tenant_identity__user=request.user)

