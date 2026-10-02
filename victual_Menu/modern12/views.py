from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import (
    modern12SalonTenant,
    modern12SalonStoreFront,
    modern12SalonStylist,
    modern12SalonService,
    modern12PortfolioWork,
    modern12SalonBlogArticle,
    modern12SalonProduct  # 🟢 IMPORTED: Connected the new beauty retail inventory table model!
)


# =========================================================================
# 🔒 SHARED HELPER LAYER: GETS COMMON BEAUTY SALON CONTEXT AUTOMATICALLY
# =========================================================================
def get_salon_store_context(request, slug=None):
    """🔒 HELPER: Safely extracts tenant salon records uniformly for all sub-views"""
    tenant_slug = slug
    if not tenant_slug:
        tenant_slug = 'modern12'

    active_slug_record = get_object_or_404(modern12SalonTenant, slug_name__iexact=tenant_slug)
    platform_config = get_object_or_404(modern12SalonStoreFront, tenant_identity=active_slug_record)

    # Gather relative dynamic child rows stamped for custom layout modules
    salon_services = modern12SalonService.objects.filter(store=platform_config)
    salon_stylists = modern12SalonStylist.objects.filter(store=platform_config)
    portfolio_works = modern12PortfolioWork.objects.filter(store=platform_config)
    salon_articles = modern12SalonBlogArticle.objects.filter(store=platform_config)

    # 🟢 NEW: Integrated dynamic e-commerce retail products catalogue tracker
    salon_products = modern12SalonProduct.objects.filter(store=platform_config, is_in_stock=True)

    return {
        'active_tenant': active_slug_record,
        'platform_config': platform_config,
        'salon_services': salon_services,
        'salon_stylists': salon_stylists,
        'portfolio_works': portfolio_works,
        'salon_articles': salon_articles,
        'salon_products': salon_products,
    }


# =========================================================================
# 💇‍♀️ PART 1: DYNAMIC SALON LANDING DASHBOARD CONTROLLER VIEW
# =========================================================================
def modern12_index_view(request, slug=None):
    """🏡 Renders your dynamic index.html home storefront layout with featured product sliders"""
    if not slug:
        slug = 'modern12'
    context = get_salon_store_context(request, slug)

    # 🟢 HOME DISPLAY SELECTION LAYER: Pulls ONLY those retail products explicitly toggled by user!
    context['featured_home_products'] = context['salon_products'].filter(is_featured_on_home=True)[:4]

    return render(request, 'modern12/index.html', context)


# =========================================================================
# 💄 PART 2: MULTI-PAGE BEAUTY SALON ROUTERS
# These match your clicked frontend layout menu targets flawlessly!
# =========================================================================

def modern12_services_view(request, slug=None):
    """🛠️ Renders your dynamic services.html grooming menu cards"""
    if not slug:
        slug = 'modern12'
    context = get_salon_store_context(request, slug)
    return render(request, 'modern12/services.html', context)


def modern12_about_view(request, slug=None):
    """🏢 Renders your dynamic about.html corporate welcome story matrix"""
    if not slug:
        slug = 'modern12'
    context = get_salon_store_context(request, slug)
    return render(request, 'modern12/about.html', context)


def modern12_work_view(request, slug=None):
    """📸 Renders your dynamic work.html portfolio lookbook with dynamic query filter arrays"""
    if not slug:
        slug = 'modern12'
    context = get_salon_store_context(request, slug)

    # 🕵️‍♂️ Advanced Classification Query Interceptor (Filter by tag parameter lookups)
    category_param = request.GET.get('category', 'all').strip().upper()

    if category_param and category_param != 'ALL':
        context['portfolio_works'] = context['portfolio_works'].filter(work_category=category_param)

    return render(request, 'modern12/work.html', context)


def modern12_blog_view(request, slug=None):
    """📰 Renders your dynamic blog.html media article boards with text-expansion datasets"""
    if not slug:
        slug = 'modern12'
    context = get_salon_store_context(request, slug)
    return render(request, 'modern12/blog.html', context)


def modern12_contact_view(request, slug=None):
    """📞 Renders your dynamic contact.html coordinate desk grid with WhatsApp action hooks"""
    if not slug:
        slug = 'modern12'
    context = get_salon_store_context(request, slug)
    return render(request, 'modern12/contact.html', context)


# =========================================================================
# 🛍️ PART 3: PREMIUM MULTI-TENANT COSMETICS RETAIL SHOP CONTROLLER VIEW
# =========================================================================
def modern12_shop_view(request, slug=None):
    """🛍️ Renders your dynamic shop.html digital beauty store catalogue with interactive sorting"""
    if not slug:
        slug = 'modern12'
    context = get_salon_store_context(request, slug)

    # 🕵️‍♂️ Advanced Category Query Sorter Interceptor
    shop_category_param = request.GET.get('item_group', 'all').strip().upper()
    if shop_category_param and shop_category_param != 'ALL':
        context['salon_products'] = context['salon_products'].filter(product_category=shop_category_param)

    return render(request, 'modern12/shop.html', context)
