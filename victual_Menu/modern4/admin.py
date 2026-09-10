from django.contrib import admin
from .models import (
    Modern4SlugTenant,
    Modern4StoreFront,
    Modern4HospitalService,
    Modern4MedicalDoctor,
    Modern4HospitalTestimonial,
    Modern4MedicalAppointment,
    Modern4HospitalContactMessage
)

# ==============================================================================
# 🔒 PART 1A: MULTI-TENANT IDENTITY VAULT CONTROLLER
# ==============================================================================

@admin.register(Modern4SlugTenant)
class Modern4SlugTenantAdmin(admin.ModelAdmin):
    """
    🔒 HOSPITAL MULTI-TENANT IDENTITY VAULT FOR MODERN4
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


# ==============================================================================
# 👑 PART 1B: VISUAL MARKET DECK SETTINGS CONTROLLER
# ==============================================================================

@admin.register(Modern4StoreFront)
class Modern4StoreFrontAdmin(admin.ModelAdmin):
    """
    👑 CLINICAL MARKETING DASHBOARD VISUAL CONTROL PANEL FOR MODERN4
    """
    list_display = ('__str__', 'hospital_email', 'emergency_phone_line', 'initialized_at')
    search_fields = ('tenant_identity__hospital_name', 'tenant_identity__hospital_slug')
    list_filter = ('initialized_at',)

    fieldsets = (
        ('🔒 Core Identity Link', {
            'fields': ('tenant_identity', 'hospital_logo')
        }),
        ('📞 Communication & Help Coordinates', {
            'fields': ('hospital_email', 'emergency_phone_line', 'hospital_physical_address')
        }),
        ('🎨 Main Visual Landing Sections', {
            'fields': ('hero_title', 'carousel_img_1', 'carousel_txt_1', 'carousel_img_2', 'carousel_txt_2', 'carousel_img_3', 'carousel_txt_3')
        }),
        ('📘 Featured About Section Elements', {
            'fields': (
                'about_main_title', 'about_description_primary', 'about_description_secondary',
                'about_showcase_image_1', 'about_showcase_image_2',
                'about_check_1', 'about_check_2', 'about_check_3',
                'about_button_text', 'about_button_url'
            )
        }),
        ('🎬 Interactive Core Features Panel', {
            'fields': (
                'feature_main_headline', 'feature_summary_text',
                'feat_card_1_title', 'feat_card_1_sub',
                'feat_card_2_title', 'feat_card_2_sub',
                'feat_card_3_title', 'feat_card_3_sub',
                'feat_card_4_title', 'feat_card_4_sub',
                'feature_banner_img'
            )
        }),
        ('📊 Social Proof Statistics Counters', {
            'fields': ('count_doctors', 'count_staff', 'count_patients')
        }),
        ('🗺️ Master Section Text Control Labels', {
            'fields': ('services_section_title', 'team_section_title', 'appointment_title', 'appointment_description', 'testimonial_section_title', 'newsletter_subtext')
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
            kwargs["queryset"] = Modern4SlugTenant.objects.filter(assigned_agent__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# ==============================================================================
# 📁 PART 2A: REPEATING CHILD CONTENT GRIDS LAYER CONTROLLERS
# ==============================================================================

@admin.register(Modern4HospitalService)
class Modern4HospitalServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'store')
    search_fields = ('service_name',)

    def get_queryset(self, request):
        """🔒 USER ISOLATION SHIELD: Regular vendors only see their own clinical rows"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'agent_profile'):
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)
        return qs.filter(store__tenant_identity__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """🔒 DROP-DOWN PROTECTION: Restricts vendor drop-downs strictly to their profile row"""
        if db_field.name == "store" and not request.user.is_superuser:
            if hasattr(request.user, 'agent_profile'):
                kwargs["queryset"] = Modern4StoreFront.objects.filter(tenant_identity__assigned_agent__user=request.user)
            else:
                kwargs["queryset"] = Modern4StoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Modern4MedicalDoctor)
class Modern4MedicalDoctorAdmin(admin.ModelAdmin):
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
                kwargs["queryset"] = Modern4StoreFront.objects.filter(tenant_identity__assigned_agent__user=request.user)
            else:
                kwargs["queryset"] = Modern4StoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Modern4HospitalTestimonial)
class Modern4HospitalTestimonialAdmin(admin.ModelAdmin):
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
                kwargs["queryset"] = Modern4StoreFront.objects.filter(tenant_identity__assigned_agent__user=request.user)
            else:
                kwargs["queryset"] = Modern4StoreFront.objects.filter(tenant_identity__user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ==============================================================================
# 📥 PART 2B: PATIENT APPOINTMENT TRANSACTION DESK
# ==============================================================================

@admin.register(Modern4MedicalAppointment)
class Modern4MedicalAppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'selected_doctor', 'appointment_date', 'is_reviewed', 'store')
    list_editable = ('is_reviewed',)
    readonly_fields = ('store', 'patient_name', 'patient_email', 'patient_phone', 'appointment_date', 'appointment_time', 'selected_doctor', 'patient_message', 'logged_at')
    search_fields = ('patient_name', 'selected_doctor')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'agent_profile'):
            return qs.filter(store__tenant_identity__assigned_agent__user=request.user)
        return qs.filter(store__tenant_identity__user=request.user)


# ==============================================================================
# 📬 PART 2C: CLIENT FOOTER MAILBOX FEEDBACK CONTROLLER
# ==============================================================================

@admin.register(Modern4HospitalContactMessage)
class Modern4HospitalContactMessageAdmin(admin.ModelAdmin):
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

