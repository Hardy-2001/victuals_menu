
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import (
    Modern10CarTenant,
    Modern10CarStoreFront,
    Modern10CarCategory,
    Modern10CarListing,
    Modern10CarBlogArticle,
    Modern10NewsletterSubscription,
    Modern10StudioTeamMember,
    Modern10CarTestimonial
)


# =========================================================================
# 🔒 SHARED HELPER LAYER: GETS COMMON AUTOMOTIVE STORE CONTEXT AUTOMATICALLY
# =========================================================================
def get_car_store_context(request, slug=None):
    """🔒 HELPER: Safely extracts tenant automotive records uniformly for all sub-views"""
    tenant_slug = getattr(request, 'tenant_slug_token', slug)

    # 🟢 FIXED: Automatically fall back to our 'modern10' default token parameter if blank
    if not tenant_slug:
        tenant_slug = 'modern10'

    active_slug_record = get_object_or_404(Modern10CarTenant, slug_name__iexact=tenant_slug)
    platform_config = get_object_or_404(Modern10CarStoreFront, tenant_identity=active_slug_record)

    studio_categories = Modern10CarCategory.objects.filter(store=platform_config)

    # Core Fleet catalog listing filter query parameters
    product_listings = Modern10CarListing.objects.filter(store=platform_config, is_available=True)
    studio_blogs = Modern10CarBlogArticle.objects.filter(store=platform_config)[:3]

    # Dynamic child rows stamped for custom layout modules
    testimonials = Modern10CarTestimonial.objects.filter(store=platform_config)
    studio_team_members = Modern10StudioTeamMember.objects.filter(store=platform_config)

    return {
        'active_tenant': active_slug_record,
        'platform_config': platform_config,
        'studio_categories': studio_categories,
        'product_listings': product_listings,
        'studio_blogs': studio_blogs,
        'testimonials': testimonials,
        'studio_team_members': studio_team_members,
    }


# =========================================================================
# 🏎️ PART 1: DYNAMIC AUTOS LANDING DASHBOARD CONTROLLER VIEW
# =========================================================================
def modern10_index_view(request, slug=None):
    """🏡 Renders your dynamic index.html home storefront layout with 100% database-driven dropdowns"""
    if not slug:
        slug = 'modern10'
    context = get_car_store_context(request, slug)

    # 🟢 DYNAMIC MATRIX EXTRACTION: Pulls authentic properties ONLY from this merchant's actual fleet records
    available_listings = context['product_listings']

    # We strip out duplicates using .distinct() so the list choices stay clean and professional
    context['dynamic_years'] = available_listings.values_list('year_of_manufacture', flat=True).distinct().order_by(
        '-year_of_manufacture')
    context['dynamic_brands'] = available_listings.values_list('make_and_model', flat=True).distinct().order_by(
        'make_and_model')
    context['dynamic_locations'] = available_listings.values_list('showroom_location', flat=True).distinct().order_by(
        'showroom_location')
    context['dynamic_mileage'] = available_listings.values_list('mileage', flat=True).distinct().order_by('mileage')

    # Binds the sorted full record set for advanced model search selections
    context['dynamic_fleet_options'] = available_listings.order_by('make_and_model')

    # Inline dynamic dual search landing inputs filtering interceptor
    purpose_param = request.GET.get('purpose')
    if purpose_param in ['RENT', 'SALE']:
        context['product_listings'] = available_listings.filter(purpose=purpose_param)

    return render(request, 'modern10/index.html', context)


# =========================================================================
# 🚙 PART 1B: MULTI-PAGE AUTOMOTIVE TEMPLATE SUB-VIEW ROUTERS
# These match your clicked frontend layout menu targets flawlessly!
# =========================================================================

def modern10_car_view(request, slug=None):
    """🚙 Renders your dynamic car.html automotive inventory fleet grids catalog"""
    if not slug:
        slug = 'modern10'
    context = get_car_store_context(request, slug)

    # 🕵️‍♂️ Advanced Sidebar Filter Query Interceptors (Multi-Parameter Parsing)
    search_q = request.GET.get('q')
    brand_param = request.GET.get('brand')
    model_param = request.GET.get('model')
    body_style_param = request.GET.get('body_style')
    condition_param = request.GET.get('condition')
    transmission_param = request.GET.get('transmission')
    mileage_param = request.GET.get('mileage')
    engine_param = request.GET.get('engine')
    color_param = request.GET.get('color')
    purpose_param = request.GET.get('purpose')

    if search_q:
        context['product_listings'] = context['product_listings'].filter(make_and_model__icontains=search_q)
    if brand_param:
        context['product_listings'] = context['product_listings'].filter(make_and_model__icontains=brand_param)
    if model_param:
        context['product_listings'] = context['product_listings'].filter(make_and_model__icontains=model_param)
    if condition_param:
        context['product_listings'] = context['product_listings'].filter(
            vehicle_details_text__icontains=condition_param)
    if purpose_param:
        context['product_listings'] = context['product_listings'].filter(purpose=purpose_param)

    return render(request, 'modern10/car.html', context)


def modern10_about_view(request, slug=None):
    """🏢 Renders your dynamic about.html corporate description matrix"""
    if not slug:
        slug = 'modern10'
    context = get_car_store_context(request, slug)
    return render(request, 'modern10/about.html', context)


def modern10_blog_view(request, slug=None):
    """📰 Renders your dynamic blog.html media automotive article boards"""
    if not slug:
        slug = 'modern10'
    context = get_car_store_context(request, slug)
    context['studio_blogs'] = Modern10CarBlogArticle.objects.filter(store=context['platform_config'])
    return render(request, 'modern10/blog.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import Modern10CarStoreFront

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage
from .models import Modern10CarStoreFront


def modern10_contact_view(request, slug):
    """
    📬 HIGH-PERFORMANCE MULTI-TENANT ROUTING EMAIL ENGINE
    Authenticates through the platform post office but safely isolates delivery straight to the merchant's email!
    """
    # 🟢 Step 1: Pull the precise dynamic storefront configuration database records via active slug
    platform_config = get_object_or_404(Modern10CarStoreFront, tenant_identity__slug_name=slug)
    active_tenant = platform_config.tenant_identity

    if request.method == 'POST':
        user_name = request.POST.get('name', '').strip()
        user_email = request.POST.get('email', '').strip()
        user_phone = request.POST.get('phone', '').strip()
        user_message = request.POST.get('message', '').strip()

        # 🟢 ISOLATED MERCHANT TARGET: Dynamically pulls the exact store email you typed into the admin desk dashboard!
        merchant_target_email = platform_config.contact_email

        if merchant_target_email:
            try:
                # 🪐 Step 2: Build a professional, high-end notification message block summary
                email_subject = f"🚨 New Car Procurement Lead: {user_name} [Subdomain Channel: {active_tenant.slug_name}]"

                email_body_content = (
                    f"Hello {active_tenant.business_name} Showroom Management Team,\n\n"
                    f"An elite client has just transmitted a secure inquiry message form via your digital subdomain showroom portal.\n"
                    f"Review the transactional parameter summaries detailed down below:\n\n"
                    f"=================================================================\n"
                    f"👤 BUYER CONTACT DETAILS\n"
                    f"=================================================================\n"
                    f"• Full Name:    {user_name}\n"
                    f"• Phone Number: {user_phone}\n"
                    f"• Email Box:    {user_email}\n\n"
                    f"=================================================================\n"
                    f"📝 CUSTOM MESSAGE PAYLOAD STATEMENT\n"
                    f"=================================================================\n"
                    f"\"{user_message}\"\n\n"
                    f"-----------------------------------------------------------------\n"
                    f"SaaS Subdomain Route Tracker Identity: [{active_tenant.slug_name.upper()}-FLEET-PORTAL]\n"
                    f"Action Required: Hit 'Reply' inside your email application to message the client directly."
                )

                # ⚡ Step 3: Dispatch payload through central host post channels
                email_payload = EmailMessage(
                    subject=email_subject,
                    body=email_body_content,
                    # Masked name label string text overlay parameters
                    from_email=f"{active_tenant.business_name} Portal <system@corexautos.ng>",
                    to=[merchant_target_email],
                    # 🟢 ISOLATION ASSURANCE: The text will drop ONLY inside Frank's email box!
                    reply_to=[user_email],  # Let's the dealer reply straight to the customer with 1 click!
                )

                email_payload.send(fail_silently=False)
                messages.success(request,
                                 "Your showroom procurement message request has been securely transmitted straight to our dealer desk operators!")

            except Exception as mail_exception:
                messages.error(request,
                               "Outbound server authorization check is pending settings authentication credentials.")
        else:
            messages.error(request,
                           "Dealer mailbox tracking coordinates are unassigned inside administration profiles.")

        return redirect('modern10_contact_view', slug=slug)

    context = {
        'platform_config': platform_config,
        'active_tenant': active_tenant,
    }
    return render(request, 'modern10/contact.html', context)


# =========================================================================
# ✉️ PART 2: CLIENT NEWSLETTER LEADS CAPTURE REGISTER RECEIVER
# =========================================================================

def modern10_submit_newsletter(request, slug=None):
    """📬 Captures customer footer email inputs from screen cards and saves leads safely."""
    if request.method == "POST":
        tenant_slug = getattr(request, 'tenant_slug_token', slug)

        if not tenant_slug:
            tenant_slug = 'modern10'

        active_slug_record = get_object_or_404(Modern10CarTenant, slug_name__iexact=tenant_slug)
        platform_config = get_object_or_404(Modern10CarStoreFront, tenant_identity=active_slug_record)

        subscriber_email = request.POST.get('subscriber_email')

        if subscriber_email:
            Modern10NewsletterSubscription.objects.create(
                store=platform_config,
                subscriber_email=subscriber_email
            )
            messages.success(request,
                             f"Identity Registered! You've successfully subscribed to our automotive catalog updates.")

        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')


# =========================================================================
# 🔍 PART 3: PREMIUM VEHICLE ITEM DETAILS SPECIFICATIONS VIEW
# =========================================================================

def modern10_car_details_view(request, slug=None, pk=None):
    """🛒 FULL DETAIL INVENTORY VIEWPORT FOR MODERN10"""
    tenant_slug = getattr(request, 'tenant_slug_token', slug)

    if not tenant_slug:
        tenant_slug = 'modern10'

    active_slug_record = get_object_or_404(Modern10CarTenant, slug_name__iexact=tenant_slug)
    platform_config = get_object_or_404(Modern10CarStoreFront, tenant_identity=active_slug_record)

    # Gather baseline context parameters
    studio_categories = Modern10CarCategory.objects.filter(store=platform_config)
    product_listings = Modern10CarListing.objects.filter(store=platform_config, is_available=True)
    studio_blogs = Modern10CarBlogArticle.objects.filter(store=platform_config)[:3]

    # Pull the single clicked car item tracking row matching this primary key
    selected_car_item = get_object_or_404(Modern10CarListing, pk=pk, store=platform_config)

    testimonials = Modern10CarTestimonial.objects.filter(store=platform_config)
    studio_team_members = Modern10StudioTeamMember.objects.filter(store=platform_config)

    context = {
        'active_tenant': active_slug_record,
        'platform_config': platform_config,
        'studio_categories': studio_categories,
        'product_listings': product_listings,
        'studio_blogs': studio_blogs,
        'testimonials': testimonials,
        'studio_team_members': studio_team_members,
        'car': selected_car_item,  # Binds clicked row directly to your HTML template parameters!
    }

    return render(request, 'modern10/car-details.html', context)


def modern10_blog_details_view(request, slug=None, pk=None):
    """📖 FULL READING JOURNAL VIEWPORT FOR ARTICLES"""
    tenant_slug = getattr(request, 'tenant_slug_token', slug)

    if not tenant_slug:
        tenant_slug = 'modern10'

    active_slug_record = get_object_or_404(Modern10CarTenant, slug_name__iexact=tenant_slug)
    platform_config = get_object_or_404(Modern10CarStoreFront, tenant_identity=active_slug_record)

    selected_article = get_object_or_404(Modern10CarBlogArticle, pk=pk, store=platform_config)
    context = get_car_store_context(request, tenant_slug)
    context['article'] = selected_article

    return render(request, 'modern10/blog-details.html', context)
