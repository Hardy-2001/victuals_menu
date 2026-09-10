from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import RestaurantProfile

def professional_restaurant_view(request, store_slug):
    """
    🍔 MODERN2 CHOWDECK-STYLE VIEW CONTROLLER
    Queries the professional restaurant profiles and pre-fetches food sections cleanly.
    """
    # 🎯 FIXED: Updated lookup path to query restaurant_slug inside the linked identity vault table!
    store = get_object_or_404(RestaurantProfile, restaurant_identity__restaurant_slug=store_slug)

    # 🛑 Active Account Paywall Gatekeeper
    if not store.is_restaurant_active:
        return HttpResponse(
            "<body style='background:#fcfcfc;color:#4b5563;font-family:sans-serif;text-align:center;padding:80px 20px;'>"
            "<h2 style='color:#dc2626;font-size:26px;font-weight:900;'>🔒 KITCHEN DISPATCH SUSPENDED</h2>"
            f"<p style='font-size:15px;margin-top:10px;'>The food catalog for <b>{store.restaurant_name}</b> is currently inactive.</p>"
            "</body>",
            status=403
        )

    # Fetch menu categories and pre-fetch child items to prevent database loops
    categories = store.food_categories.all().prefetch_related('menu_items')

    context = {
        'store': store,
        'categories': categories,
    }

    return render(request, 'advance2/restaurant_catalog.html', context)
