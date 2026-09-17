from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import (
    Modern9ApparelTenant,
    Modern9ApparelStoreFront,
    Modern9ApparelCategory,
    Modern9ApparelProductListing,
    Modern9ApparelBlogArticle,
    Modern9ApparelNewsletterLead
)


def get_tenant_configuration(slug):
    """🔒 SAAS CONTEXT ROUTER SHIELD
    Fetches the persistent brand profile setup from the live PostgreSQL storage server.
    """
    tenant = get_object_or_404(Modern9ApparelTenant, brand_slug=slug)
    config = get_object_or_404(Modern9ApparelStoreFront, tenant_identity=tenant)
    return tenant, config


def index_view(request, slug):
    """🏠 TAILSTORE MAIN LANDING DASHBOARD
    Streams dynamic lookbooks, category slots, trending items, and blog boards live.
    """
    active_tenant, platform_config = get_tenant_configuration(slug)

    # Extract isolated child entries matching this merchant only
    shop_categories = Modern9ApparelCategory.objects.filter(store=platform_config)
    shop_products = Modern9ApparelProductListing.objects.filter(store=platform_config, is_in_stock=True)
    shop_blogs = Modern9ApparelBlogArticle.objects.filter(store=platform_config)

    context = {
        'active_tenant': active_tenant,
        'platform_config': platform_config,
        'shop_categories': shop_categories,
        'shop_products': shop_products,
        'shop_blogs': shop_blogs,
    }
    return render(request, 'modern9/index.html', context)


def shop_view(request, slug):
    """🛍️ CLOTHING CATALOG MATRIX GRID VIEW
    Filters garments securely by category queries with zero crossover leakages.
    """
    active_tenant, platform_config = get_tenant_configuration(slug)
    shop_categories = Modern9ApparelCategory.objects.filter(store=platform_config)

    # Base Query: Lock visibility strictly inside this tenant's sandbox
    product_queryset = Modern9ApparelProductListing.objects.filter(store=platform_config)

    # Apply URL Parameter Segment Filters safely if present
    category_slug_query = request.GET.get('category_slug')
    if category_slug_query:
        product_queryset = product_queryset.filter(dynamic_category__category_slug=category_slug_query)

    context = {
        'active_tenant': active_tenant,
        'platform_config': platform_config,
        'shop_categories': shop_categories,
        'shop_products': product_queryset,
        'selected_category': category_slug_query,
    }
    return render(request, 'modern9/shop.html', context)


def single_product_view(request, slug, pk):
    """👗 GARMENT DETAIL SPECIFICATIONS LOOKUP
    Loads full resolution layout details, measurement indices, and cross-sell loops.
    """
    active_tenant, platform_config = get_tenant_configuration(slug)

    # Secure row isolation validation lookup matching database keys
    selected_furniture_item = get_object_or_404(Modern9ApparelProductListing, store=platform_config, pk=pk)

    # Generate cross-sell catalogs matching this workspace layout arena smoothly
    all_shop_products = Modern9ApparelProductListing.objects.filter(store=platform_config, is_in_stock=True).exclude(
        pk=pk)

    context = {
        'active_tenant': active_tenant,
        'platform_config': platform_config,
        'selected_furniture_item': selected_furniture_item,
        'shop_products': all_shop_products,
    }
    return render(request, 'modern9/single-product-page.html', context)


def cart_view(request, slug):
    """🛒 SHOPPING BAG REVIEW & WHATSAPP GENERATION DISPATCHER
    Loads the requested garment metadata specs to prepare the instant checkout payload.
    """
    active_tenant, platform_config = get_tenant_configuration(slug)

    # Pull targeted product primary key off URL request strings if routing from catalogs
    product_pk_query = request.GET.get('product_pk')
    selected_furniture_item = None

    if product_pk_query:
        selected_furniture_item = Modern9ApparelProductListing.objects.filter(store=platform_config,
                                                                              pk=product_pk_query).first()

    context = {
        'active_tenant': active_tenant,
        'platform_config': platform_config,
        'selected_furniture_item': selected_furniture_item,
    }
    return render(request, 'modern9/cart.html', context)


def subscribe_newsletter_view(request, slug):
    """✉️ INBOUND CLIENT LEAD CAPTURE DIRECTORY
    Validates and registers footer email entries into your permanent database tracking paths.
    """
    _, platform_config = get_tenant_configuration(slug)

    if request.method == 'POST':
        email_input_string = request.POST.get('subscriber_email', '').strip()

        if email_input_string:
            # Check if this customer is already registered inside this specific store partition row
            already_registered = Modern9ApparelNewsletterLead.objects.filter(store=platform_config,
                                                                             subscriber_email=email_input_string).exists()

            if not already_registered:
                Modern9ApparelNewsletterLead.objects.create(store=platform_config, subscriber_email=email_input_string)
                messages.success(request,
                                 "🎉 Welcome to the Style Club! Your ₦50,000 discount voucher has been generated successfully.")
            else:
                messages.info(request, "Your email is already locked into our style update network index lists!")

    return redirect('modern9:storefront_with_slug', slug=slug)
