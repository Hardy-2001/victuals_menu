from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives,get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import EmailSenderTenant, EmailSenderPlatformProfile, BroadcastCampaignManifest, NewsletterSubscriber


# =========================================================================
# 🏠 PART 1: PUBLIC FRONTEND CAPTURE LANDING PAGE CONTROLLER
# =========================================================================
def email_sender_index_view(request, slug=None):
    """🏡 Renders the frontend newsletter subscriber capture template layout."""
    if not slug:
        slug = 'sanity'  # Fallback testing subdomain slug slug tracking handle

    # Capture the active workspace application tenant mapping safely
    active_tenant = get_object_or_404(EmailSenderTenant, slug_name__iexact=slug)
    profile_config = get_object_or_404(EmailSenderPlatformProfile, tenant_identity=active_tenant)

    if request.method == 'POST':
        full_name_input = request.POST.get('subscriber_name', '').strip()
        email_address_input = request.POST.get('subscriber_email', '').strip().lower()

        if full_name_input and email_address_input:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                tenant=active_tenant,
                client_email_address=email_address_input,
                defaults={'client_full_name': full_name_input, 'is_active_subscription': True}
            )

            if created:
                messages.success(request, f"🎉 Success! Welcome to the loop, {full_name_input}!")
            else:
                if not subscriber.is_active_subscription:
                    subscriber.is_active_subscription = True
                    subscriber.client_full_name = full_name_input
                    subscriber.save()
                    messages.success(request,
                                     f"⚡ Welcome back! Your subscription status has been reactivated successfully.")
                else:
                    messages.info(request, "ℹ️ You are already a registered insider list profile on our system.")

            return redirect('email_sender_index_view', slug=active_tenant.slug_name)

    context = {
        'active_tenant': active_tenant,
        'profile_config': profile_config,
    }
    return render(request, 'email_sender_app/index.html', context)


# =========================================================================
# 📨 PART 2: DYNAMIC HTML EMAIL DISPATCH ENGINE CONTROLLER
# =========================================================================
def dispatch_broadcast_campaign(request, campaign_id):
    """
    ⚡ BACKEND ENGINE ROUTINE: Dynamically parses uploaded images, titles, and price vectors
    into a rich HTML layout block and dispatches it via the tenant's private isolated SMTP gateway!
    """
    campaign = get_object_or_404(BroadcastCampaignManifest, id=campaign_id)
    tenant = campaign.profile.tenant_identity  # Resolves cleanly to your isolated EmailSenderTenant record

    # 👤 Filter active subscriber list records for this tenant exclusively
    active_mailing_list = NewsletterSubscriber.objects.filter(
        tenant=tenant,
        is_active_subscription=True
    )

    if not active_mailing_list.exists():
        messages.warning(request, "⚠️ Dispatch Halted: There are no active subscribers registered on this list yet.")
        return redirect('/admin/email_sender_app/broadcastcampaignmanifest/')

    # 🖼️ CRITICAL CONVERSION: Transforms relative image file media directory paths into absolute web URLs
    absolute_image_url = request.build_absolute_uri(campaign.broadcast_image_banner.url)

    # 📦 Pack data entries inside the context dictionary map layer
    email_context = {
        'business_name': tenant.business_name,
        'subject_header': campaign.email_subject_header,
        'product_title': campaign.product_title_heading,
        'product_price': f"{int(campaign.product_selling_price):,}",
        'product_image': absolute_image_url,
        'product_description': campaign.email_message_description,
        # 🔗 DYNAMIC ACTION LINK: Binds the inbox action button directly onto your admin custom destination url entry!
        'subdomain_link': campaign.custom_destination_url
    }

    # 🎨 Compile rich visual HTML brochure code strings dynamically via local templates
    html_presentation_body = render_to_string('email_sender_app/campaign_email.html', email_context)
    plain_text_fallback = strip_tags(html_presentation_body)

    recipient_emails_array = [sub.client_email_address for sub in active_mailing_list]

    try:
        # Update delivery status properties to active state to prevent double-send overlaps
        campaign.delivery_status = 'processing'
        campaign.save()

        # 🪐 DYNAMIC ENVELOPE CONNECTION ENGINE: Opens an isolated connection wrapper using THIS specific client's credentials!
        merchant_mail_connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=campaign.profile.smtp_server_host,
            port=campaign.profile.smtp_server_port,
            username=campaign.profile.smtp_account_username,
            password=campaign.profile.smtp_account_password,
            use_tls=not campaign.profile.use_secure_ssl,  # TLS triggers if SSL is False
            use_ssl=campaign.profile.use_secure_ssl,
        )

        # Determine a safe baseline email address for the main 'To' field route requirements
        primary_recipient = recipient_emails_array[0] if recipient_emails_array else campaign.profile.smtp_account_username

        # 🚀 ASYNC MULTI-ALTERNATIVES ROUTER PORTAL GATEWAY BOUND TO THE ISOLATED CONNECTION POOL
        email_payload = EmailMultiAlternatives(
            subject=campaign.email_subject_header,
            body=plain_text_fallback,
            from_email=f"{tenant.business_name} <{campaign.profile.smtp_account_username}>",
            to=[primary_recipient],  # Primary recipient placeholder
            bcc=recipient_emails_array,  # Delivers message privately to everyone at once via BCC blind carbon copies
            connection=merchant_mail_connection  # <-- 100% Isolated dynamic client-driven routing gate!
        )

        email_payload.attach_alternative(html_presentation_body, "text/html")
        email_payload.send()

        # Update logs upon clean distribution passes
        campaign.delivery_status = 'completed'
        campaign.total_recipients_count = len(recipient_emails_array)
        campaign.save()

        messages.success(request,
                         f"🚀 Marketing brochure successfully dispatched to {len(recipient_emails_array)} valid inbox profiles via your private branded email gateway!")

    except Exception as network_error:
        campaign.delivery_status = 'failed'
        campaign.save()
        messages.error(request, f"❌ System Delivery Failure Breakdown: {str(network_error)}")

    return redirect('/admin/email_sender_app/broadcastcampaignmanifest/')
