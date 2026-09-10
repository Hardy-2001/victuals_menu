from django.contrib import admin
from django.contrib.auth.models import User
from .models import AgentProfile, PlatformSetting, ShowcaseTemplate, UserBillingNotice


@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    """
    👑 AGENT RECRUITMENT CONTROL BOARD
    Visible only to the root developer Super Admin.
    """
    list_display = ('agent_code', 'get_name', 'assigned_state', 'phone_number')
    search_fields = ('agent_code', 'user__username', 'assigned_state')

    def get_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_name.short_description = "Agent Name"

    def has_module_permission(self, request):
        return request.user.is_superuser


# 🎯 OVERWRITE THE PlatformSettingAdmin CLASS IN super_admin/admin.py WITH THIS EXPLICIT VERSION:

@admin.register(PlatformSetting)
class PlatformSettingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'admin_phone', 'admin_whatsapp', 'mock_rented_shops_base')
    fields = (
        'platform_logo',
        'admin_phone',
        'admin_whatsapp',
        'mock_rented_shops_base',
        'server_state_default',
        'server_state_blue',
        'server_state_purple',
        'server_state_emerald',
        'server_state_amber',
        # 🟢 EXTRA 5 BACKGROUND IMAGES: Injected cleanly into your admin panel sequence layout row!
        'server_state_six',
        'server_state_seven',
        'server_state_eight',
        'server_state_nine',
        'server_state_ten',
        'services_text',
        'security_text',
        'about_text'
    )



@admin.register(ShowcaseTemplate)
class ShowcaseTemplateAdmin(admin.ModelAdmin):
    list_display = ('label_name', 'showcase_image')
    search_fields = ('label_name',)

    def has_module_permission(self, request):
        return request.user.is_superuser


from .models import InfrastructureMailLog


@admin.register(InfrastructureMailLog)
class InfrastructureMailLogAdmin(admin.ModelAdmin):
    """
    🛡️ CENTRAL CONTROL MAIL INTERCEPT DECK
    """
    list_display = ('sender_name', 'sender_email', 'logged_at')
    readonly_fields = ('sender_name', 'sender_email', 'message_body', 'logged_at')
    search_fields = ('sender_name', 'sender_email')

    # Restrict additions inside the portal since mails should only stream from the frontend form
    def has_add_permission(self, request):
        return False


@admin.register(UserBillingNotice)
class UserBillingNoticeAdmin(admin.ModelAdmin):
    """
    👑 SUPER ADMIN PRIVATE PAYMENT CONTROLLER
    """
    list_display = ('merchant_user', 'bank_name', 'account_number', 'subscription_amount', 'last_updated')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(merchant_user=request.user)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='Field Agents').exists():
            return False
        return True

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()
        return ('merchant_user', 'bank_name', 'account_number', 'account_name', 'subscription_amount', 'payment_instructions')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "merchant_user":
            kwargs["queryset"] = User.objects.all().order_by('username')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


from django.contrib import admin
from .models import DomainEngine


@admin.register(DomainEngine)
class DomainEngineAdmin(admin.ModelAdmin):
    list_display = ['slug_name', 'app_target', 'created_at']
    search_fields = ['slug_name']
    list_filter = ['app_target']