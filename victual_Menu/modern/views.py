from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import ModernStoreFront, ModernCategory, ModernProductItem, ModernSlugTenant






def modern_store_front_view(request, store_slug=None, tenant_slug_token=None):
    """
    👑 NEXT-GEN PREMIUM ARCHETYPE VIEW ROUTER
    Located at: modern/views.py
    """
    # Isolate the clean slug parameter from the middleware routing paths cleanly
    active_slug = store_slug or tenant_slug_token or getattr(request, 'tenant_slug_token', None)

    # 1. First, fetch your main tenant profile row record by its slug path
    tenant_profile = get_object_or_404(ModernSlugTenant, custom_slug__iexact=active_slug)

    # 2. 🟢 THE SOLUTION: Fetch the actual ModernStoreFront instance that is linked to this tenant!
    # (Using your model's reverse lookup relationship)
    store = get_object_or_404(ModernStoreFront, tenant_identity=tenant_profile)

    # 🛑 Premium Account Status Gatekeeper
    if not store.is_premium_active:
        return HttpResponse(
            f"<body style='background:#fcfcfc;color:#4b5563;font-family:sans-serif;text-align:center;padding:80px 20px;'>"
            f"<h2 style='color:#dc2626;font-size:28px;font-weight:900;'>🔒 PRESERVED SERVICE SUSPENDED</h2>"
            f"<p style='font-size:15px;margin-top:10px;'>The modern marketplace profile for <b>{store.store_name}</b> is currently locked.</p>"
            f"</body>",
            status=403
        )

    # Fetch categories and prefetch child products safely
    categories = store.modern_categories.all().prefetch_related('modern_products')

    context = {
        'store': store,
        'categories': categories,
    }

    # 🎯 PREMIUM VISUAL STYLE MATRIX THEME SWITCH
    if store.layout_theme == 'GYM_FITNESS':
        return render(request, 'modern/gym_catalog.html', context)

    # Default fallback viewport canvas layout
    return render(request, 'modern/minimalist_catalog.html', context)



def modern_product_detail_view(request, store_slug=None, product_id=None, tenant_slug_token=None):
    """
    📸 NEXT-GEN PREMIUM SINGLE-PRODUCT ROUTER
    """
    active_slug = store_slug or tenant_slug_token or getattr(request, 'tenant_slug_token', None)
    store = get_object_or_404(ModernSlugTenant, custom_slug__iexact=active_slug)

    is_active = getattr(store, 'is_premium_active', getattr(store, 'is_active', True))
    if not is_active:
        return HttpResponse("🔒 SERVICE SUSPENDED", status=403)

    # 🟢 THE CRITICAL LIVE FIX: Fetches the matching storefront instance table link row!
    # This matches whatever store instance model field connects ModernSlugTenant to ModernStoreFront.
    # We look it up by matching the active slug text.
    storefront_instance = get_object_or_404(ModernStoreFront, custom_slug__iexact=active_slug)

    # 🟢 ALIGNED QUERY RAIL: We now pass the exact ModernStoreFront object instance Django is begging for!
    product = get_object_or_404(ModernProductItem, id=product_id, category__store=storefront_instance)
    profile = getattr(store, 'modern_profile', None)

    # 🎯 SMART CORRELATION ENGINE: Fetches exactly 3 related items from this same category aisle!
    related_products = ModernProductItem.objects.filter(
        category=product.category,
        is_in_stock=True
    ).exclude(id=product.id)[:3]

    context = {
        'store': store,
        'product': product,
        'profile': profile,
        'related_products': related_products,
    }

    layout_theme = getattr(store, 'layout_theme', 'GYM_FITNESS')
    if layout_theme == 'GYM_FITNESS':
        return render(request, 'modern/gym_detail.html', context)

    return render(request, 'modern/minimalist_detail.html', context)



def modern_store_about_view(request, store_slug=None, tenant_slug_token=None):
    """
    ℹ️ DYNAMIC ABOUT US VIEW ROUTER
    """
    active_slug = store_slug or tenant_slug_token or getattr(request, 'tenant_slug_token', None)
    store = get_object_or_404(ModernSlugTenant, custom_slug__iexact=active_slug)

    is_active = getattr(store, 'is_premium_active', getattr(store, 'is_active', True))
    if not is_active:
        return HttpResponse("🔒 SERVICE SUSPENDED", status=403)

    return render(request, 'modern/gym_about.html', {'store': store})
