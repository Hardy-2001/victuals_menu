from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import EmailSenderTenant, EmailSenderPlatformProfile, BroadcastCampaignManifest, NewsletterSubscriber


@admin.register(EmailSenderTenant)
class EmailSenderTenantAdmin(admin.ModelAdmin):
    """🎛️ MAIN TENANT ONBOARDING ENGINE"""
    list_display = ('business_name', 'slug_name', 'assigned_agent', 'created_at')
    list_filter = ('assigned_agent', 'created_at')
    search_fields = ('business_name', 'slug_name')
    prepopulated_fields = {'slug_name': ('business_name',)}


@admin.register(EmailSenderPlatformProfile)
class EmailSenderPlatformProfileAdmin(admin.ModelAdmin):
    """🎛️ WEBSITE CORE CONTENT ENGINE"""
    list_display = ('tenant_identity', 'contact_phone', 'contact_email', 'campaign_limit_per_day', 'is_active_license')
    list_filter = ('is_active_license', 'initialized_at')

    # 🟢 MULTI-TENANT SMTP FIELDSETS SYNC: Grouped secure server parameters cleanly inside the form panel deck!
    fieldsets = (
        ('🔒 Core Identity Link', {
            'fields': ('tenant_identity', 'is_active_license', 'campaign_limit_per_day')
        }),
        ('📞 Showroom Communications Radar', {
            'fields': ('contact_phone', 'contact_email', 'contact_address')
        }),
        ('🎨 Home Page Welcome Stage Accents', {
            'fields': ('hero_title', 'hero_subtitle', 'landing_page_banner')
            # 🟢 INJECTED THE NEW BANNER FIELD UPLOADER HERE
        }),
        ('🔐 Dynamic Isolated SMTP Mailbox Gateway Settings', {
            'fields': ('smtp_server_host', 'smtp_server_port', 'smtp_account_username', 'smtp_account_password',
                       'use_secure_ssl')
        }),
    )


@admin.register(BroadcastCampaignManifest)
class BroadcastCampaignManifestAdmin(admin.ModelAdmin):
    """🎛️ ADMINISTRATIVE CONTROL DECK: MARKETING CAMPAIGN WITH FORM DISPATCH CONTROLS"""
    list_display = ('email_subject_header', 'product_title_heading', 'product_selling_price', 'delivery_status',
                    'total_recipients_count', 'dispatch_action_trigger', 'dispatched_at')
    list_filter = ('delivery_status', 'dispatched_at', 'profile')
    search_fields = ('email_subject_header', 'product_title_heading')
    ordering = ['-dispatched_at']

    # 🟢 ADDED: Declares the button method as a read-only form parameter asset row
    readonly_fields = ('dispatch_action_trigger',)

    fieldsets = (
        ('🔒 Target Tenant Link', {
            'fields': ('profile',)
        }),
        ('📧 Campaign Messaging Headers', {
            'fields': ('email_subject_header', 'product_title_heading', 'product_selling_price',
                       'custom_destination_url')
        }),
        ('🖼️ Visual Brochure Media Assets', {
            'fields': ('broadcast_image_banner', 'email_message_description')
        }),
        # 🟢 INJECTED INSIDE FORM VIEW: Dropped the send trigger right here into your editor field block section!
        ('📊 Operational Delivery Metrics', {
            'fields': ('delivery_status', 'total_recipients_count', 'dispatch_action_trigger')
        }),
    )

    def dispatch_action_trigger(self, obj):
        """🌐 RENDERS THE HIGH-CONTRAST CLICKABLE GREEN SEND ACTION ROUTING BUTTON"""
        if not obj.id:
            return format_html(
                '<span style="color: #666;">Save this campaign item first to unlock dispatch controls.</span>')

        if obj.delivery_status == 'completed':
            return format_html(
                '<span style="color: #28a745; font-weight: bold;"><i class="fa-solid fa-check-double"></i> Sent out</span>{}',
                "")
        elif obj.delivery_status == 'processing':
            return format_html('<span style="color: #ffc107; font-weight: bold;">Processing...</span>{}', "")

        dispatch_url = reverse('dispatch_broadcast_campaign', kwargs={'campaign_id': obj.id})
        return format_html(
            '<a class="button" href="{}" style="background: #28a745 !important; color: #ffffff !important; padding: 8px 16px; font-weight: bold; border-radius: 4px; text-decoration: none; text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; display: inline-block;">🚀 Dispatch Campaign Mail</a>',
            dispatch_url
        )

    dispatch_action_trigger.short_description = "Send Action Switch"


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    """🎛️ ADMINISTRATIVE CONTROL DECK: REGISTERED CLIENTS REGISTER SUITE"""
    list_display = ('client_full_name', 'client_email_address', 'tenant', 'is_active_subscription', 'subscribed_at')
    list_filter = ('is_active_subscription', 'subscribed_at', 'tenant')
    search_fields = ('client_full_name', 'client_email_address')
    ordering = ['-subscribed_at']
