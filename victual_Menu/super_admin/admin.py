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


# =========================================================================
# 🛡️ GLOBAL CUSTOMER SHIELD: AGENTS ONLY SEE LOGINS THEY ONBOARDED
# =========================================================================
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class SecureSaaSUserAdmin(UserAdmin):
    """
    🔐 GLOBAL SECURITY ISOLATION VIEWPORT & FORMS MULTI-LOCKDOWN
    1. Restricts the User list view so agents only see their own creations.
    2. Dynamically hides raw permissions and superuser checkboxes from agents.
    3. Keeps the Groups widget visible inside user edits but completely vanishes
       the 'Groups' app option from the agent's sidebar dashboard links block.
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if not hasattr(request.user, 'agent_profile'):
            return qs.filter(id=request.user.id)

        my_agent_profile = request.user.agent_profile
        allowed_user_ids = set()
        allowed_user_ids.add(request.user.id)

        for model in apps.get_models():
            try:
                has_agent_field = any(f.name == 'assigned_agent' for f in model._meta.get_fields())
                has_user_field = any(f.name == 'user' for f in model._meta.get_fields())

                if has_agent_field and has_user_field:
                    tenant_rows = model.objects.filter(assigned_agent=my_agent_profile).select_related('user')
                    for row in tenant_rows:
                        if row.user:
                            allowed_user_ids.add(row.user.id)
            except Exception:
                continue

        user_content_type = ContentType.objects.get_for_model(qs.model)
        agent_creation_logs = LogEntry.objects.filter(
            user=request.user,
            content_type=user_content_type,
            action_flag=ADDITION
        ).values_list('object_id', flat=True)

        for obj_id in agent_creation_logs:
            try:
                allowed_user_ids.add(int(obj_id))
            except (ValueError, TypeError):
                continue

        return qs.filter(id__in=allowed_user_ids)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if request.user.is_superuser:
            return fieldsets

        clean_fieldsets = []
        for title, fields_dict in fieldsets:
            if title in [None, 'Personal info', 'Important dates']:
                clean_fieldsets.append((title, fields_dict))
            elif title == 'Permissions':
                mutated_fields = list(fields_dict['fields'])
                if 'is_superuser' in mutated_fields: mutated_fields.remove('is_superuser')
                if 'user_permissions' in mutated_fields: mutated_fields.remove('user_permissions')
                if 'groups' not in mutated_fields: mutated_fields.append('groups')

                clean_fieldsets.append((title, {'fields': tuple(mutated_fields)}))

        return clean_fieldsets

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """🛡️ Filters available options inside the Groups selection boxes dynamically"""
        if db_field.name == "groups" and not request.user.is_superuser:
            kwargs["queryset"] = db_field.related_model.objects.exclude(
                name__iexact="Agents"
            ).order_by('name')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    # 🛑 THE SIDEBAR VANISHING ACT: Completely blocks agents from accessing Groups module menu lists
    def has_module_permission(self, request):
        """🛡️ Hides or shows the app room block header link list dynamically"""
        if request.user.is_superuser:
            return True
        # If an agent is logged in, let them access the app section so they can see Users
        return True

    def has_view_permission(self, request, obj=None):
        return True


# 🚀 CUSTOM INTERCEPT ENGINE FOR THE GROUPS REGISTRY CONTROLLER TO HIDE THE SIDEBAR ROW COMPLETELY
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin


class SecureSaaSGroupAdmin(GroupAdmin):
    """
    🔐 HIDDEN SECURITY DECK
    Completely vanishes the Groups management row from the agent's sidebar.
    """

    def has_module_permission(self, request):
        # 👑 Superuser can manage groups, field agents are blocked entirely from seeing the row links!
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None): return request.user.is_superuser

    def has_add_permission(self, request): return request.user.is_superuser

    def has_change_permission(self, request, obj=None): return request.user.is_superuser

    def has_delete_permission(self, request, obj=None): return request.user.is_superuser


# 🚀 Swap both standard auth systems out to lock down the dashboard completely
try:
    admin.site.unregister(User)
    admin.site.unregister(Group)
except admin.site.NotRegistered:
    pass

admin.site.register(User, SecureSaaSUserAdmin)
admin.site.register(Group, SecureSaaSGroupAdmin)

# =========================================================================
# 🎛️ GLOBAL FIXED FORM FIELDS INTERCEPTOR FOR ALL UNIQUE APP TENANTS
# =========================================================================
from django.contrib.admin import ModelAdmin
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType

# 1. Save a reference to Django's original built-in formfield method
_original_formfield_for_foreignkey = ModelAdmin.formfield_for_foreignkey


def secure_global_formfield_interceptor(self, db_field, request, **kwargs):
    """
    🔐 CORE SHIELD: Automatically intercepts dropdown fields across all separate
    app tenant forms natively without breaking Python's class inheritance tree.
    """
    # 👑 If you log in as the master developer superuser, never restrict dropdown lists
    if request.user.is_superuser:
        return _original_formfield_for_foreignkey(self, db_field, request, **kwargs)

    # 🕵️‍♂️ Check if this logged-in staff user has a corresponding active agent profile record
    if hasattr(request.user, 'agent_profile'):
        my_agent_profile = request.user.agent_profile

        # 1. 🔒 LOCK ASSIGNED AGENT DROPDOWN: Force agents to select ONLY themselves
        if db_field.name == "assigned_agent":
            kwargs["queryset"] = db_field.related_model.objects.filter(user=request.user)

        # 2. 🔒 LOCK USER ACCOUNT DROPDOWN: Only show user login profiles created by THIS agent
        elif db_field.name == "user":
            user_content_type = ContentType.objects.get_for_model(User)

            # Extract all User account record IDs that this agent has ever created via Admin Logs
            my_onboarded_user_ids = LogEntry.objects.filter(
                user=request.user,
                content_type=user_content_type,
                action_flag=ADDITION
            ).values_list('object_id', flat=True)

            # Convert string array IDs securely back to an integers list
            clean_ids = [request.user.id]  # Always include the agent themselves as a safe option
            for obj_id in my_onboarded_user_ids:
                try:
                    clean_ids.append(int(obj_id))
                except (ValueError, TypeError):
                    continue

            kwargs["queryset"] = db_field.related_model.objects.filter(id__in=clean_ids).order_by('username')

    # 🚀 Pass the modified fields execution cleanly back to Django's original core processing method
    return _original_formfield_for_foreignkey(self, db_field, request, **kwargs)


# 🟢 OVERRIDE JUMP: Safely patch the base ModelAdmin method globally across the entire project ecosystem
ModelAdmin.formfield_for_foreignkey = secure_global_formfield_interceptor

