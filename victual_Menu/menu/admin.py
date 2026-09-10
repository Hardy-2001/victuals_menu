from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission
from django.db.models import Q
from .models import Tenant, Category, FoodItem, CustomerFeedback, RestaurantProfile

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    """
    🛡️ AUTOMATED SAAS CLIENT REGISTRY & PAYWALL ENGINE
    """
    list_display = ('business_name', 'business_type', 'assigned_agent', 'payment_status', 'created_at')
    search_fields = ('business_name', 'slug')
    list_editable = ('business_type', 'payment_status')

    def display_billing_blinker(self, obj):
        if obj.payment_status == 'PAID':
            return format_html('<span style="background-color:#22c55e; color:#fff; font-size:11px; font-weight:bold; padding:4px 10px; border-radius:12px; text-transform:uppercase;">🟢 Paid</span>')
        return format_html('<span style="background-color:#ef4444; color:#fff; font-size:11px; font-weight:bold; padding:4px 10px; border-radius:12px;">🔴 Unpaid</span>')
    display_billing_blinker.short_description = "Virtual Account Status"

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ('user', 'business_name', 'slug', 'business_type', 'assigned_agent', 'payment_status',
                    'virtual_account_number', 'virtual_bank_name', 'is_active')
        return ('user', 'business_name', 'slug', 'business_type')

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not change:
            agent_prof = getattr(request.user, 'agent_profile', None)
            if agent_prof:
                obj.assigned_agent = agent_prof
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(assigned_agent__user=request.user)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'tenant_display', 'order', 'whatsapp_number')
    list_editable = ('order', 'whatsapp_number')
    ordering = ('tenant', 'order')

    def tenant_display(self, obj):
        return obj.tenant.business_name
    tenant_display.short_description = "Restaurant Owner"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name='Field Agents').exists() or hasattr(request.user, 'agent_profile'):
            return qs.filter(tenant__assigned_agent__user=request.user)
        return qs.filter(tenant__user=request.user)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not change:
            if hasattr(request.user, 'tenant_profile'):
                obj.tenant = request.user.tenant_profile
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tenant" and not request.user.is_superuser:
            if request.user.groups.filter(name='Field Agents').exists() or hasattr(request.user, 'agent_profile'):
                kwargs["queryset"] = Tenant.objects.filter(assigned_agent__user=request.user)
            else:
                kwargs["queryset"] = Tenant.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('display_thumb', 'name', 'category', 'price', 'is_available')
    list_editable = ('price', 'is_available')
    search_fields = ('name', 'description')

    def display_thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height: 35px; object-fit: cover; border-radius: 6px;" />', obj.image.url)
        return "No Image"
    display_thumb.short_description = "Preview"

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('category__tenant', 'is_available')
        return ()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name='Field Agents').exists() or hasattr(request.user, 'agent_profile'):
            return qs.filter(category__tenant__assigned_agent__user=request.user)
        return qs.filter(category__tenant__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category" and not request.user.is_superuser:
            if request.user.groups.filter(name='Field Agents').exists() or hasattr(request.user, 'agent_profile'):
                kwargs["queryset"] = Category.objects.filter(tenant__assigned_agent__user=request.user)
            else:
                kwargs["queryset"] = Category.objects.filter(tenant__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(CustomerFeedback)
class CustomerFeedbackAdmin(admin.ModelAdmin):
    list_display = ('tenant_display', 'table_number', 'display_stars', 'comment_excerpt', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment', 'table_number')
    readonly_fields = ('tenant', 'table_number', 'rating', 'comment', 'created_at')

    def tenant_display(self, obj):
        return obj.tenant.business_name
    tenant_display.short_description = "Restaurant"

    def display_stars(self, obj):
        return "⭐" * obj.rating
    display_stars.short_description = "Rating"

    def comment_excerpt(self, obj):
        return obj.comment[:50] + "..." if len(obj.comment) > 50 else obj.comment
    comment_excerpt.short_description = "Diner Comment"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name='Field Agents').exists() or hasattr(request.user, 'agent_profile'):
            return qs.filter(tenant__assigned_agent__user=request.user)
        return qs.filter(tenant__user=request.user)


@admin.register(RestaurantProfile)
class RestaurantProfileAdmin(admin.ModelAdmin):
    list_display = ('restaurant_name', 'tenant_display', 'phone_number', 'whatsapp_number', 'primary_color')
    def tenant_display(self, obj):
        return obj.tenant.business_name
    tenant_display.short_description = "Tenant Account"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name='Field Agents').exists() or hasattr(request.user, 'agent_profile'):
            return qs.filter(tenant__assigned_agent__user=request.user)
        return qs.filter(tenant__user=request.user)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='Field Agents').exists() or hasattr(request.user, 'agent_profile'):
            return True
        return not RestaurantProfile.objects.filter(tenant__user=request.user).exists()

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and hasattr(obj, 'tenant'):
            agent_prof = getattr(request.user, 'agent_profile', None)
            if agent_prof and obj.tenant:
                obj.tenant.assigned_agent = agent_prof
                obj.tenant.save()
        super().save_model(request, obj, form, change)

# 🎯 CRITICAL UNREGISTER COMMAND
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class CustomSaaSUserAdmin(UserAdmin):
    """
    🛡️ AUTOMATED MULTI-APP AGENT USER ISOLATION
    Ensures created users stay visible to agents across Menu, Modern, and Modern2,
    even when saved as Staff, while remaining hidden from other agents.
    """

    def get_queryset(self, request):
        """
        🔒 BULLETPROOF USER STREAM ISOLATION
        """
        qs = super().get_queryset(request)

        # 👑 Super Admin (HARDY) sees absolutely everything platform-wide
        if request.user.is_superuser:
            return qs

        # 🛡️ FIXED DISAPPEARING ACT:
        # Keeps all regular merchant accounts (staff or non-staff) visible to
        # the agent so they can build their multi-app SaaS tenants smoothly,
        # while preventing agents from seeing other agents or editing themselves!
        return qs.filter(
            is_superuser=False
        ).exclude(id=request.user.id).distinct()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "user_permissions" and not request.user.is_superuser:
            kwargs["queryset"] = Permission.objects.filter(
                content_type__app_label='menu',
                content_type__model__in=['category', 'fooditem', 'customerfeedback']
            )
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if request.user.is_superuser:
            return fieldsets

        new_fieldsets = []
        for name, opts in fieldsets:
            if name == 'Permissions':
                fields = list(opts.get('fields', []))
                if 'is_superuser' in fields:
                    fields.remove('is_superuser')
                opts = opts.copy()
                opts['fields'] = tuple(fields)
            new_fieldsets.append((name, opts))
        return tuple(new_fieldsets)


# 🏙️ Master Portal Interface Header Text Branding Parameters
admin.site.site_header = "Multi-Store Platform SaaS — Operational Portal"
admin.site.site_title = "Global SaaS Operational Hub"
admin.site.index_title = "Multi-Tenant Business Operations & Storefront Controls"
