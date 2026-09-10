from django.contrib import admin
from .models import (
    Modern3SlugTenant, Modern3StoreFront, HospitalService, HospitalDepartment,
    MedicalDoctor, HospitalFAQ, HospitalTestimonial, HospitalGalleryImage,
    MedicalAppointment, HospitalContactMessage
)

@admin.register(Modern3SlugTenant)
class Modern3SlugTenantAdmin(admin.ModelAdmin):
    """
    🔒 HOSPITAL MULTI-TENANT IDENTITY VAULT
    Enforces strict access constraints: Agents can only ADD and VIEW identity records
    linked directly to their own account profiles, with zero edit handle tampering or removal!
    """
    list_display = ('hospital_name', 'hospital_slug', 'user', 'assigned_agent', 'created_at')
    search_fields = ('hospital_name', 'hospital_slug', 'user__username')
    list_filter = ('created_at',)

    def get_queryset(self, request):
        """🔒 DATA ISOLATION SHIELD: Only display hospital tenants onboarded by this agent"""
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


@admin.register(Modern3StoreFront)
class Modern3StoreFrontAdmin(admin.ModelAdmin):
    """
    👑 CLINICAL MARKETING DASHBOARD VISUAL CONTROL PANEL
    """
    list_display = ('__str__', 'hospital_email', 'emergency_phone_line', 'initialized_at')
    search_fields = ('tenant_identity__hospital_name', 'tenant_identity__hospital_slug')
    list_filter = ('initialized_at',)

    # 🎯 OVERWRITE YOUR FIELDSETS CONFIGURATION IN modern3/admin.py TO CLEAR THE DUPLICATION ERROR:

    fieldsets = (
        ('🔒 Core Identity Link', {
            'fields': ('tenant_identity', 'hospital_logo')
        }),
        ('📞 Communication & Help Coordinates', {
            'fields': ('hospital_email', 'emergency_phone_line', 'hospital_physical_address')
        }),
        ('🎨 Main Visual Landing Sections', {
            # 🎯 FIXED: Merged into a single, clean box with zero field duplicates!
            'fields': ('hero_title', 'hero_sub_headline', 'hero_background_image')
        }),
        ('📘 Featured "Why Choose Us" Elements', {
            'fields': (
                'why_choose_us_headline', 'why_choose_us_body_text',
                'value_card_one_title', 'value_card_one_body',
                'value_card_two_title', 'value_card_two_body',
                'value_card_three_title', 'value_card_three_body'
            )
        }),
        ('🎬 Interactive Video Profiles', {
            'fields': ('about_main_description', 'about_video_url', 'about_showcase_image')
        }),
        ('📊 Social Proof Statistics Counters', {
            'fields': ('count_doctors', 'count_departments', 'count_research_labs', 'count_awards')
        }),
        ('🗺️ Location Map & Public Contact Form Settings', {
            'fields': ('contact_headline', 'contact_description', 'google_maps_embed_url')
        }),
    )


    def get_queryset(self, request):
            """🔒 DATA ISOLATION SHIELD: Field agents only monitor clinical settings they onboarded"""
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 FORMFIELD PROTECTION: Restricts the selection slot strictly to this agent's clients"""
        if db_field.name == "tenant_identity" and not request.user.is_superuser:
            kwargs["queryset"] = Modern3SlugTenant.objects.filter(assigned_agent__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# 🎯 OVERWRITE EVERYTHING FROM HospitalServiceAdmin DOWN TO THE END OF THE FILE IN modern3/admin.py:

@admin.register(HospitalService)
class HospitalServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'store')
    search_fields = ('service_name',)

    def get_queryset(self, request):
        """🔒 USER ISOLATION SHIELD: Regular vendors only see their own clinical rows"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Check if the user is an onboarding agent or the actual store merchant profile
        if hasattr(request.user, 'agent_profile'):
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store" and not request.user.is_superuser:
            # 🎯 FIXED: Direct merchant-user dropdown lookup bypasses the master profile row lookup block!
            if hasattr(request.user, 'agent_profile'):
                kwargs["queryset"] = Modern3StoreFront.objects.filter(tenant_identity__assigned_agent__user=request.user)
            else:
                kwargs["queryset"] = Modern3StoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(HospitalDepartment)
class HospitalDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'store')
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'agent_profile'):
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store" and not request.user.is_superuser:
            if hasattr(request.user, 'agent_profile'):
                kwargs["queryset"] = Modern3StoreFront.objects.filter(tenant_identity__assigned_agent__user=request.user)
            else:
                kwargs["queryset"] = Modern3StoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(MedicalDoctor)
class MedicalDoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'medical_title', 'store')
    search_fields = ('doctor_name', 'medical_title')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'agent_profile'):
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store" and not request.user.is_superuser:
            if hasattr(request.user, 'agent_profile'):
                kwargs["queryset"] = Modern3StoreFront.objects.filter(tenant_identity__assigned_agent__user=request.user)
            else:
                kwargs["queryset"] = Modern3StoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(HospitalFAQ)
class HospitalFAQAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'store')
    search_fields = ('question_text',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'agent_profile'):
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store" and not request.user.is_superuser:
            if hasattr(request.user, 'agent_profile'):
                kwargs["queryset"] = Modern3StoreFront.objects.filter(tenant_identity__assigned_agent__user=request.user)
            else:
                kwargs["queryset"] = Modern3StoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(HospitalTestimonial)
class HospitalTestimonialAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'patient_title_or_role', 'store')
    search_fields = ('patient_name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'agent_profile'):
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store" and not request.user.is_superuser:
            if hasattr(request.user, 'agent_profile'):
                kwargs["queryset"] = Modern3StoreFront.objects.filter(tenant_identity__assigned_agent__user=request.user)
            else:
                kwargs["queryset"] = Modern3StoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(HospitalGalleryImage)
class HospitalGalleryImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_caption', 'store')
    search_fields = ('image_caption',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'agent_profile'):
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "store" and not request.user.is_superuser:
            if hasattr(request.user, 'agent_profile'):
                kwargs["queryset"] = Modern3StoreFront.objects.filter(tenant_identity__assigned_agent__user=request.user)
            else:
                kwargs["queryset"] = Modern3StoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(MedicalAppointment)
class MedicalAppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'selected_doctor', 'appointment_date', 'is_reviewed', 'store')
    list_editable = ('is_reviewed',)
    readonly_fields = ('store', 'patient_name', 'patient_email', 'patient_phone', 'appointment_date', 'selected_department', 'selected_doctor', 'patient_message', 'logged_at')
    search_fields = ('patient_name', 'selected_doctor')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'agent_profile'):
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)
        return qs.filter(store__tenant_identity__user=request.user)


@admin.register(HospitalContactMessage)
class HospitalContactMessageAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'message_subject', 'is_read', 'received_at', 'store')
    list_editable = ('is_read',)
    readonly_fields = ('store', 'sender_name', 'sender_email', 'message_subject', 'message_body', 'received_at')
    search_fields = ('sender_name', 'message_subject')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'agent_profile'):
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)
        return qs.filter(store__tenant_identity__user=request.user)
