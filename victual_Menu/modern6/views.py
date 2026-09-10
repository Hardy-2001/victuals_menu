from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import (
    Modern6RealEstateTenant,
    Modern6AgencyStoreFront,
    Modern6PropertyCategory,
    Modern6PropertyListing,
    Modern6TourAppointment
)


# ==============================================================================
# 💎 PART 1: LUXURY REAL ESTATE DISPLAY ENGINE VIEW
# ==============================================================================

def modern6_agency_storefront_view(request, slug=None):
    """
    🏡 DYNAMIC REAL ESTATE HUB ROUTER FOR MODERN6
    Queries isolated agency metrics, fetches custom categories, and handles live filtering.
    """
    # 🧬 1. Extract the active case-insensitive tenant slug parameter
    tenant_slug = getattr(request, 'tenant_slug_token', slug)

    if not tenant_slug:
        tenant_slug = 'estateify'  # Perfect local fallback anchor matches your mockup image label

    # 🧬 2. Look up the matching isolated identity rows from your private tenant vault
    active_slug_record = get_object_or_404(Modern6RealEstateTenant, agency_slug__iexact=tenant_slug)

    # 🧬 3. Query the single visual deck control panel assigned exclusively to this record ID
    platform_config = Modern6AgencyStoreFront.objects.filter(tenant_identity=active_slug_record).first()

    if not platform_config:
        platform_config = Modern6AgencyStoreFront.objects.create(tenant_identity=active_slug_record)

    # 🧬 4. Gather user-managed categories and full properties arrays matching this context
    agency_categories = Modern6PropertyCategory.objects.filter(store=platform_config)
    property_listings = Modern6PropertyListing.objects.filter(store=platform_config)

    # 🏙️ LIVE COMPRESSION SEARCH FILTER: Intercept parameters coming directly from your custom search box panel
    search_location = request.GET.get('search_location', '').strip()
    search_category_slug = request.GET.get('search_category_slug', '').strip()
    search_price_tier = request.GET.get('search_price_tier', '').strip()

    if search_location:
        property_listings = property_listings.filter(location_city__icontains=search_location)

    if search_category_slug:
        property_listings = property_listings.filter(dynamic_category__category_slug=search_category_slug)

    if search_price_tier:
        property_listings = property_listings.filter(price_display_label=search_price_tier)

    # Bundle active data entries neatly into your template context engine canvas
    context = {
        'active_tenant': active_slug_record,
        'platform_config': platform_config,
        'agency_categories': agency_categories,
        'property_listings': property_listings,
        # Preserve input tokens to display selection parameters on screen cards
        'selected_location': search_location,
        'selected_category': search_category_slug,
        'selected_price': search_price_tier,
    }

    return render(request, 'modern6/index.html', context)


# ==============================================================================
# 📥 PART 2: SECURE CLIENT TOUR RESERVATION TRANSACTION VIEW
# ==============================================================================

def modern6_book_property_tour(request, slug=None):
    """
    🔒 LUXURY PORTAL TOUR RESERVATION MAILBOX RECEIVER
    Extracts form inputs from user submissions and schedules asset inspections safely.
    """
    if request.method == "POST":
        tenant_slug = getattr(request, 'tenant_slug_token', slug)

        # 🛸 Fallback constraint anchor tracking
        if not tenant_slug:
            tenant_slug = 'estateify'

        # Look up matching isolated visual profile deck table nodes
        active_slug_record = get_object_or_404(Modern6RealEstateTenant, agency_slug__iexact=tenant_slug)
        platform_config = get_object_or_404(Modern6AgencyStoreFront, tenant_identity=active_slug_record)

        # 📥 Read raw form inputs parameters from the booking widget overlay
        client_name = request.POST.get('client_name')
        client_email = request.POST.get('client_email')
        client_phone = request.POST.get('client_phone')

        # Capture context metrics from the luxury search picker card panels
        requested_location = request.POST.get('location_type', 'Miami, Florida')
        requested_house_type = request.POST.get('house_type', 'Luxury Villa')
        requested_price_range = request.POST.get('price_range', '$800k - $2M')

        tour_date = request.POST.get('tour_date', 'As soon as possible')
        client_message = request.POST.get('client_message', '')

        # 🚀 Write input metrics into your custom modern6 tour appointment transaction table row
        Modern6TourAppointment.objects.create(
            store=platform_config,
            client_name=client_name,
            client_email=client_email,
            client_phone=client_phone,
            requested_location=requested_location,
            requested_house_type=requested_house_type,
            requested_price_range=requested_price_range,
            tour_date=tour_date,
            client_message=client_message
        )

        # Trigger an elegant web confirmation alert response banner
        messages.success(request,
                         f"Request Logged! Our elite brokerage team will contact you shortly to confirm your tour.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect('/')


# ==============================================================================
# 💎 PART 4: PREMIUM REAL ESTATE PROPERTY DETAILS VAULT ENGINE VIEW
# ==============================================================================

def modern6_property_detail_view(request, slug=None, pk=None):
    """
    📸 ISOLATED REAL ESTATE PROPERTY DETAIL VIEW FOR MODERN6
    Queries isolated house details row index cards, aggregates category items,
    and handles live WhatsApp metadata routing variables cleanly.
    """
    tenant_slug = getattr(request, 'tenant_slug_token', slug)
    if not tenant_slug:
        tenant_slug = 'estateify'

    active_slug_record = get_object_or_404(Modern6RealEstateTenant, agency_slug__iexact=tenant_slug)
    platform_config = get_object_or_404(Modern6AgencyStoreFront, tenant_identity=active_slug_record)

    # Fetch target primary row index card details matching this app context safely
    house = get_object_or_404(Modern6PropertyListing, pk=pk, store=platform_config)

    # Gather alternative choice rows in identical category bins excluding the self row index tracker
    similar_houses = Modern6PropertyListing.objects.filter(
        store=platform_config,
        dynamic_category=house.dynamic_category
    ).exclude(pk=house.pk)[:3]

    context = {
        'active_tenant': active_slug_record,
        'platform_config': platform_config,
        'house': house,
        'similar_houses': similar_houses,
    }
    return render(request, 'modern6/property_detail.html', context)


