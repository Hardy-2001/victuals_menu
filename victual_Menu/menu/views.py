from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# 📦 PERFECTLY CLEAN: Only local menu-tier tables stay inside this sandbox!
from .models import Category, CustomerFeedback, RestaurantProfile, Tenant, FoodItem


def get_tenant_or_paywall(restaurant_slug=None, tenant_slug_token=None):
    """
    🛡️ SAAS GATEKEEPER HELPER
    🟢 UPDATED: Dynamically accepts restaurant_slug OR tenant_slug_token
    to make subdomains work flawlessly without breaking existing routes!
    """
    # Use whichever parameter variable token was injected by the system layout
    active_slug = restaurant_slug or tenant_slug_token

    # Query your exact model column 'slug' safely
    tenant = get_object_or_404(Tenant, slug=active_slug)
    return tenant


def online_menu(request, restaurant_slug=None, tenant_slug_token=None):
    """
    🍔 RESTAURANT HOME FRONTPAGE
    🟢 UPDATED: Injects both parameter keys to allow seamless routing.
    """
    active_slug = restaurant_slug or tenant_slug_token or getattr(request, 'tenant_slug_token', None)
    tenant = get_tenant_or_paywall(restaurant_slug=active_slug)

    # 🛑 Paywall Gatekeeper: Check if they have paid their monthly ₦10k subscription
    if not tenant.is_active:
        return HttpResponse(
            f"<body style='background:#121212;color:#a1a1aa;font-family:sans-serif;text-align:center;padding:50px 20px;'> "
            f"<h2 style='color:#dc2626;'>🔒 SERVICE SUSPENDED</h2>"
            f"<p>The digital profile for <b>{tenant.business_name}</b> is currently inactive.</p>"
            f"<small style='color:#52525b;'>Please contact the platform administrator to renew your hosting access loop track.</small>"
            f"</body>",
            status=403
        )

    # 🔒 Filter items strictly owned by this specific tenant
    categories = Category.objects.filter(tenant=tenant).prefetch_related('items')

    # Safely fetch or build fallback settings configurations
    profile = getattr(tenant, 'profile', None)
    if not profile:
        profile = RestaurantProfile(
            restaurant_name=tenant.business_name,
            phone_number="2349020425819",
            whatsapp_number="2349020425819",
            primary_color="#dc2626",
            outer_bg_color="#0c0c0d",
            inner_bg_color="#121212"
        )

    context = {
        'categories': categories,
        'profile': profile,
        'tenant': tenant,
    }

    # 🎯 100% AUTOMATED DATABASE ARCHETYPE ROUTER
    if tenant.business_type == 'GROCERY':
        return render(request, 'menu/grocery_catalog.html', context)
    elif tenant.business_type == 'FASHION':
        return render(request, 'menu/fashion.html', context)

    # Default fallback matrix grid row blueprint for standard food / bar clients
    return render(request, 'menu/index.html', context)


@csrf_exempt
def submit_feedback(request, restaurant_slug):
    """
    🗳️ ISOLATED ANONYMOUS REVIEW HANDLING VIEW
    """
    tenant = get_object_or_404(Tenant, slug=restaurant_slug)

    if not tenant.is_active:
        return JsonResponse({'success': False, 'error': 'Account inactive.'}, status=403)

    if request.method == 'POST':
        table_number = request.POST.get('table_number', '')
        rating = request.POST.get('rating', 5)
        comment = request.POST.get('comment', '')

        if not comment:
            return JsonResponse({'success': False, 'error': 'Please drop a short note before sending!'}, status=400)

        CustomerFeedback.objects.create(
            tenant=tenant,
            table_number=table_number,
            rating=int(rating),
            comment=comment
        )
        return JsonResponse({'success': True, 'message': 'Thank you! Your anonymous review was logged.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)


def checkout_summary(request, restaurant_slug):
    """
    🛒 ISOLATED CHECKOUT SUMMARY MINI-PAGE VIEW
    """
    tenant = get_tenant_or_paywall(restaurant_slug)

    if not tenant.is_active:
        return HttpResponse("Account suspended.", status=403)

    profile = getattr(tenant, 'profile', None)
    active_phone = profile.whatsapp_number if profile else "2349020425819"

    context = {
        'whatsapp_number': active_phone,
        'profile': profile,
        'tenant': tenant,
    }
    return render(request, 'menu/checkout.html', context)


# 🎯 Find your product details view function inside menu/views.py and update its return section to this:

def product_detail(request, restaurant_slug, product_id):
    """
    📸 MORE DETAILS CORE ROUTER
    Preserves all your current variable lookups, but swaps the HTML template
    dynamically depending on the registered SaaS business industry archetype!
    """
    tenant = get_tenant_or_paywall(restaurant_slug)

    # 🛑 Paywall Gatekeeper check (Preserves your existing security layer logic)
    if not tenant.is_active:
        return HttpResponse("🔒 SERVICE SUSPENDED", status=403)

    # Fetch the product being inspected
    product = get_object_or_404(FoodItem, id=product_id, category__tenant=tenant)
    categories = Category.objects.filter(tenant=tenant).prefetch_related('items')
    profile = getattr(tenant, 'profile', None)

    # Fetch up to 4 similar items from the same category aisle for recommendations
    similar_products = FoodItem.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'categories': categories,
        'profile': profile,
        'tenant': tenant,
        'similar_products': similar_products,
    }

    # 🎯 THE CRITICAL ROUTING GATEKEEPER SWITCH:
    if tenant.business_type == 'GROCERY':
        # Forces Django to drop the fashion layout and load your premium light supermarket page!
        return render(request, 'menu/grocery_detail.html', context)

    elif tenant.business_type == 'FASHION':
        return render(request, 'menu/product_detail.html', context)  # (Your original clothes details view)

    # Fallback default layout template sheet for restaurant dining plates
    return render(request, 'menu/detail.html', context)


