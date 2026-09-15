from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import (
    Modern8FurnitureTenant,
    Modern8FurnitureStoreFront,
    Modern8FurnitureCategory,
    Modern8FurnitureProductListing,
    Modern8FurnitureBlogArticle,
    Modern8NewsletterSubscription,
    Modern8StudioTeamMember,  # 🟢 IMPORTED FOR DYNAMIC TEAM SHOWCASE
    Modern8FurnitureTestimonial  # 🟢 IMPORTED FOR DYNAMIC CLIENT REVIEWS
)


# =========================================================================
# 🔒 SHARED HELPER LAYER: GETS COMMON STORE CONTEXT AUTOMATICALLY
# =========================================================================
def get_furniture_store_context(request, slug=None):
    """🔒 HELPER: Safely extracts tenant data records uniformly for all sub-views"""
    tenant_slug = getattr(request, 'tenant_slug_token', slug)
    if not tenant_slug or tenant_slug == 'modern8':
        tenant_slug = 'furnify'  # Perfect local developer fallback sandbox token

    active_slug_record = get_object_or_404(Modern8FurnitureTenant, studio_slug__iexact=tenant_slug)
    platform_config = get_object_or_404(Modern8FurnitureStoreFront, tenant_identity=active_slug_record)

    studio_categories = Modern8FurnitureCategory.objects.filter(store=platform_config)
    product_listings = Modern8FurnitureProductListing.objects.filter(store=platform_config, is_in_stock=True)
    studio_blogs = Modern8FurnitureBlogArticle.objects.filter(store=platform_config)[:3]

    # 🟢 EXTRACT DYNAMIC DATA ENTRIES STAMPED FOR THE NEW SECTIONS
    testimonials = Modern8FurnitureTestimonial.objects.filter(store=platform_config)
    studio_team_members = Modern8StudioTeamMember.objects.filter(store=platform_config)

    return {
        'active_tenant': active_slug_record,
        'platform_config': platform_config,
        'studio_categories': studio_categories,
        'product_listings': product_listings,
        'studio_blogs': studio_blogs,
        'testimonials': testimonials,  # Added safely to context vault
        'studio_team_members': studio_team_members,  # Added safely to context vault
    }


# =========================================================================
# 🛋️ PART 1: ADVANCED FURNITURE LANDING & FILTER ENGINE VIEW
# =========================================================================

def modern8_furniture_storefront_view(request, slug=None):
    """🏡 Renders your dynamic index.html layout home channel"""
    context = get_furniture_store_context(request, slug)

    # Keep your original inline product category filtering logic fully active!
    search_category_slug = request.GET.get('category_slug')
    if search_category_slug:
        context['product_listings'] = context['product_listings'].filter(
            dynamic_category__category_slug=search_category_slug)
        context['selected_category'] = search_category_slug

    return render(request, 'modern8/index.html', context)


# =========================================================================
# 🟢 PART 1B: MULTI-PAGE TEMPLATE SUB-VIEW ROUTERS
# These match your clicked layout menu targets flawlessly!
# =========================================================================

def modern8_shop_view(request, slug=None):
    """🛍️ Renders your dynamic shop.html product grids catalog"""
    context = get_furniture_store_context(request, slug)
    search_category_slug = request.GET.get('category_slug')
    if search_category_slug:
        context['product_listings'] = context['product_listings'].filter(
            dynamic_category__category_slug=search_category_slug)
        context['selected_category'] = search_category_slug
    return render(request, 'modern8/shop.html', context)


def modern8_about_view(request, slug=None):
    """🏢 Renders your dynamic about.html corporate description matrix"""
    context = get_furniture_store_context(request, slug)
    return render(request, 'modern8/about.html', context)


def modern8_services_view(request, slug=None):
    """🛠️ Renders your dynamic services.html 8-pillar highlight cards"""
    context = get_furniture_store_context(request, slug)
    return render(request, 'modern8/services.html', context)


def modern8_blog_view(request, slug=None):
    """📰 Renders your dynamic blog.html media article boards"""
    context = get_furniture_store_context(request, slug)
    return render(request, 'modern8/blog.html', context)


def modern8_contact_view(request, slug=None):
    """📞 Renders your dynamic contact.html phone hotline layout fields"""
    context = get_furniture_store_context(request, slug)
    return render(request, 'modern8/contact.html', context)


def modern8_cart_view(request, slug=None):
    """🛒 Renders your dynamic cart.html interactive calculation table"""
    context = get_furniture_store_context(request, slug)
    return render(request, 'modern8/cart.html', context)


# =========================================================================
# ✉️ PART 2: CLIENT NEWSLETTER REGISTER SUBMISSION RECEIVER
# =========================================================================

def modern8_submit_newsletter(request, slug=None):
    """📬 Captures customer footer inputs from screen cards and saves leads safely."""
    if request.method == "POST":
        tenant_slug = getattr(request, 'tenant_slug_token', slug)
        if not tenant_slug or tenant_slug == 'modern8':
            tenant_slug = 'furnify'

        active_slug_record = get_object_or_404(Modern8FurnitureTenant, studio_slug__iexact=tenant_slug)
        platform_config = get_object_or_404(Modern8FurnitureStoreFront, tenant_identity=active_slug_record)

        subscriber_name = request.POST.get('subscriber_name', 'Valued Customer')
        subscriber_email = request.POST.get('subscriber_email')

        if subscriber_email:
            Modern8NewsletterSubscription.objects.create(
                store=platform_config,
                subscriber_name=subscriber_name,
                subscriber_email=subscriber_email
            )
            messages.success(request,
                             f"Thank you {subscriber_name}! You've successfully subscribed to our design catalog trends.")

        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')


# =========================================================================
# 🔍 PART 3: PREMIUM FURNITURE ITEM DETAILS SHOWCASE VIEW
# =========================================================================
def modern8_furniture_detail_view(request, slug=None, pk=None):
    """
    🛒 REDIRECTING PRODUCT DETAIL VIEW FOR MODERN8
    Bypasses the details viewport page layout completely.
    When an item card or thumbnail is clicked, this view instantly captures the product
    metadata context metrics and streams your interactive calculation cart page instead!
    """
    tenant_slug = getattr(request, 'tenant_slug_token', slug)
    if not tenant_slug or tenant_slug == 'modern8':
        tenant_slug = 'furnify'  # Perfect local fallback sandbox token

    # 1. Fetch active isolated visual control deck entries safely
    active_slug_record = get_object_or_404(Modern8FurnitureTenant, studio_slug__iexact=tenant_slug)
    platform_config = get_object_or_404(Modern8FurnitureStoreFront, tenant_identity=active_slug_record)

    # 2. Gather child catalog database items matching this store profile
    studio_categories = Modern8FurnitureCategory.objects.filter(store=platform_config)
    product_listings = Modern8FurnitureProductListing.objects.filter(store=platform_config, is_in_stock=True)
    studio_blogs = Modern8FurnitureBlogArticle.objects.filter(store=platform_config)[:3]

    # 3. Pull the specific item row info matching this clicked primary key
    selected_furniture_item = get_object_or_404(Modern8FurnitureProductListing, pk=pk, store=platform_config)

    # 4. Pull dynamic team and testimonials records context keys for cart wrapper layout
    testimonials = Modern8FurnitureTestimonial.objects.filter(store=platform_config)
    studio_team_members = Modern8StudioTeamMember.objects.filter(store=platform_config)

    # Bundle active metrics seamlessly into your template context canvas
    context = {
        'active_tenant': active_slug_record,
        'platform_config': platform_config,
        'studio_categories': studio_categories,
        'product_listings': product_listings,
        'studio_blogs': studio_blogs,
        'testimonials': testimonials,
        'studio_team_members': studio_team_members,
        'selected_furniture_item': selected_furniture_item,  # Stamped safely for custom cart pre-loads!
    }

    # 🟢 DIRECT ENTRY TRAFFIC VECTOR: Renders your clean cart template screen layout instantly!
    return render(request, 'modern8/cart.html', context)
