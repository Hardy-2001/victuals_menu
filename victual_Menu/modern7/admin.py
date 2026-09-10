from django.contrib import admin
from .models import (
    Modern7SchoolTenant,
    Modern7PlatformConfigDeck,
    Modern7CourseCategory,
    Modern7FacultyInstructor,
    Modern7CourseListing,
    Modern7StudentEnquiryLead,
    Modern7CourseReview
)


# ==============================================================================
# 🔒 ADMIN SECTOR 1: MULTI-TENANT REGISTRY & LAYOUT CONFIG DECK
# ==============================================================================

class Modern7PlatformConfigDeckInline(admin.StackedInline):
    """🛠️ Embedded Visual settings deck inline engine inside the parent school view."""
    model = Modern7PlatformConfigDeck
    can_delete = False
    verbose_name = "Storefront Design Settings Profile Configuration Node"
    verbose_name_plural = "Storefront Design Settings Profile Configuration Nodes"


@admin.register(Modern7SchoolTenant)
class Modern7SchoolTenantAdmin(admin.ModelAdmin):
    """🎛️ Dashboard manager panel tracking operational schools and tenant URLs."""
    list_display = ('school_name', 'slug_path', 'owner_account', 'onboarding_agent', 'is_active_node', 'registered_at')
    list_filter = ('is_active_node', 'onboarding_agent', 'registered_at')
    search_fields = ('school_name', 'slug_path', 'owner_account__username')
    prepopulated_fields = {'slug_path': ('school_name',)}
    list_editable = ('is_active_node',)

    # 🟢 INLINE COUPLING: Automatically attaches visual theme configuration tools when a school profile is loaded
    inlines = [Modern7PlatformConfigDeckInline]


@admin.register(Modern7PlatformConfigDeck)
class Modern7PlatformConfigDeckAdmin(admin.ModelAdmin):
    """🎛️ Isolated design layout dashboard rows controller."""
    list_display = ('institution_name', 'tenant_link', 'support_phone', 'support_email', 'updated_at')
    search_fields = ('institution_name', 'tenant_link__school_name', 'support_email')

    fieldsets = (
        ('Branding Identity Core Nodes', {
            'fields': ('tenant_link', 'institution_name', 'brand_logo', 'footer_summary_text')
        }),
        ('Campus Coordinates & Contact Channels', {
            'fields': ('support_phone', 'whatsapp_number', 'support_email', 'office_address', 'google_map_embed_iframe')
        }),
        ('Hero Landing Cockpit Typography Layout', {
            'fields': ('hero_tagline_accent', 'hero_main_title', 'hero_description_text', 'hero_background',
                       'hero_side_illustration')
        }),
        ('Real-Time Value Features Numerical Counters Metrics', {
            'fields': ('count_active_students', 'count_online_courses', 'count_academic_programs',
                       'count_certified_students', 'count_enrolled_students')
        }),
        ('Value Proposition Headlines Boxes Text Lines', {
            'fields': ('features_title', 'features_summary', 'feat_one_title', 'feat_one_desc', 'feat_two_title',
                       'feat_two_desc', 'feat_three_title', 'feat_three_desc', 'feat_four_title', 'feat_four_desc')
        }),
        ('About Us Presentation Content Overviews', {
            'fields': ('about_illustration', 'about_headline_title', 'about_description_one', 'about_description_two',
                       'about_bullet_one', 'about_bullet_two', 'about_bullet_three')
        }),
        ('Social Platforms Media Channels Anchors', {
            'fields': ('twitter_x_url', 'facebook_url', 'instagram_url', 'linkedin_url')
        }),
    )


# ==============================================================================
# 📂 ADMIN SECTOR 2: ACADEMIC BUCKETS & FACULTY PROFILE SYSTEM
# ==============================================================================

@admin.register(Modern7CourseCategory)
class Modern7CourseCategoryAdmin(admin.ModelAdmin):
    """🎛️ Dashboard layout configuration manager for academic learning buckets."""
    list_display = ('category_name', 'category_slug', 'school_tenant')
    list_filter = ('school_tenant',)
    search_fields = ('category_name', 'category_slug', 'school_tenant__school_name')
    prepopulated_fields = {'category_slug': ('category_name',)}


@admin.register(Modern7FacultyInstructor)
class Modern7FacultyInstructorAdmin(admin.ModelAdmin):
    """🎛️ Dashboard manager panel tracking professor biographies and social channel networks."""
    list_display = ('full_name', 'professional_title', 'school_tenant', 'count_courses_text', 'count_students_text')
    list_filter = ('school_tenant', 'professional_title')
    search_fields = ('full_name', 'professional_title', 'school_tenant__school_name')

    fieldsets = (
        ('Tutor Base Credentials Profile Card Picture', {
            'fields': ('school_tenant', 'full_name', 'professional_title', 'profile_avatar', 'biography_summary')
        }),
        ('Instructor Card Metrics Numbers Indicators', {
            'fields': ('count_courses_text', 'count_students_text')
        }),
        ('Instructor Direct Communication Links Channels', {
            'fields': ('twitter_url', 'facebook_url', 'linkedin_url')
        }),
    )


# ==============================================================================
# 🎓 ADMIN SECTOR 3: COURSE LISTINGS, LEADS, & REVIEW DASHBOARDS
# ==============================================================================

@admin.register(Modern7CourseListing)
class Modern7CourseListingAdmin(admin.ModelAdmin):
    """🎛️ Master dashboard panel to publish, edit, and organize core campus courses."""
    list_display = ('course_title', 'dynamic_category', 'assigned_instructor', 'price_display_label', 'school_tenant',
                    'is_visible_on_catalog')
    list_filter = ('school_tenant', 'dynamic_category', 'is_certified', 'is_visible_on_catalog')
    search_fields = ('course_title', 'school_tenant__school_name', 'dynamic_category__category_name')
    list_editable = ('is_visible_on_catalog',)

    fieldsets = (
        ('Course Core Meta Specifications', {
            'fields': ('school_tenant', 'dynamic_category', 'assigned_instructor', 'course_title', 'course_thumbnail')
        }),
        ('Detailed Curriculum Copy sheets Text Blocks', {
            'fields': ('course_description_main', 'course_description_secondary', 'course_overview_text',
                       'curriculum_syllabus_text')
        }),
        ('Training Specs Metrics Indicators', {
            'fields': ('duration_label', 'count_modules_text', 'count_students_registered', 'seats_available')
        }),
        ('Pricing Fees & Trailer Preview Video', {
            'fields': ('price_display_label', 'is_certified', 'embed_video_url_id')
        }),
    )


@admin.register(Modern7StudentEnquiryLead)
class Modern7StudentEnquiryLeadAdmin(admin.ModelAdmin):
    """🎛️ Dynamic lead tracking mailbox capturing student registrations from forms."""
    list_display = ('client_name', 'client_email', 'lead_subject', 'school_tenant', 'is_processed_flag', 'submitted_at')
    list_filter = ('is_processed_flag', 'school_tenant', 'submitted_at')
    search_fields = ('client_name', 'client_email', 'lead_subject', 'message_content')
    list_editable = ('is_processed_flag',)
    readonly_fields = ('submitted_at',)


@admin.register(Modern7CourseReview)
class Modern7CourseReviewAdmin(admin.ModelAdmin):
    """🎛️ Moderation interface panel to approve or block student feedback scoring rows."""
    list_display = ('student_name', 'target_course', 'rating_score', 'is_approved_for_public', 'created_at')
    list_filter = ('rating_score', 'is_approved_for_public', 'created_at')
    search_fields = ('student_name', 'student_email', 'feedback_comment_text', 'target_course__course_title')
    list_editable = ('is_approved_for_public',)
    readonly_fields = ('created_at',)
