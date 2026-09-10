from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import (
    Modern5PortfolioTenant,
    Modern5VisualDeck,
    Modern5DeveloperSkill,
    Modern5ProjectBentoGrid,
    Modern5ContractMailbox
)


# ==============================================================================
# 🪐 PART 1: HIGH-TECH TERMINAL STOREFRONT DISPLAY ENGINE VIEW
# ==============================================================================

def modern5_portfolio_storefront_view(request, slug=None):
    """
    💻 DYNAMIC PORTFOLIO STOREFRONT ROUTER FOR MODERN5
    Intercepts the user text slug, fetches isolated profiles, and pumps data to terminal layout.
    """
    # 🧬 1. Extract the active tenant slug token parameter from the route link tracking loops
    tenant_slug = getattr(request, 'tenant_slug_token', slug)

    # Safety Check fallback if no slug token is parsed on local dev environments
    if not tenant_slug:
        tenant_slug = 'ismail'

    # 🧬 2. Look up the matching isolated identity rows from your private modern5 tenant registry
    active_slug_record = get_object_or_404(Modern5PortfolioTenant, portfolio_slug__iexact=tenant_slug)

    # 🧬 3. Query the single visual deck control panel assigned exclusively to this developer ID
    platform_config = Modern5VisualDeck.objects.filter(tenant_identity=active_slug_record).first()

    # Auto-fabricate setting row baseline shell parameters safely if database field row is blank
    if not platform_config:
        platform_config = Modern5VisualDeck.objects.create(tenant_identity=active_slug_record)

    # 🧬 4. Gather repeating child data arrays matching this visual store deck node context
    developer_skills = Modern5DeveloperSkill.objects.filter(store=platform_config)
    bento_projects = Modern5ProjectBentoGrid.objects.filter(store=platform_config)

    # Bundle entries into your template context engines cleanly for frontend mapping attributes
    context = {
        'active_tenant': active_slug_record,
        'platform_config': platform_config,
        'developer_skills': developer_skills,
        'bento_projects': bento_projects,
    }

    return render(request, 'modern5/index.html', context)


# ==============================================================================
# 📥 PART 2: SECURE CLIENT PROJECT BRIEF INTAKE TRANSACTION VIEW
# ==============================================================================

def modern5_submit_contract_brief(request, slug=None):
    """
    🔒 INBOUND CLIENT WORK DESK MAILBOX RECEIVER
    Extracts text tokens from user web submissions and archives requests safely.
    """
    if request.method == "POST":
        tenant_slug = getattr(request, 'tenant_slug_token', slug)

        # 🛸 Fallback constraint anchor tracking
        if not tenant_slug:
            tenant_slug = 'ismail'

        # Look up the matching isolated visual profile deck table nodes
        active_slug_record = get_object_or_404(Modern5PortfolioTenant, portfolio_slug__iexact=tenant_slug)
        platform_config = get_object_or_404(Modern5VisualDeck, tenant_identity=active_slug_record)

        # 📥 Read raw form inputs parameters
        client_name = request.POST.get('name')
        client_email = request.POST.get('email')
        project_budget = request.POST.get('budget', '₦500,000 - ₦1,000,000')
        project_brief = request.POST.get('brief')

        # 🚀 Write input metrics into your custom modern5 mailbox transaction table row
        Modern5ContractMailbox.objects.create(
            store=platform_config,
            client_name=client_name,
            client_email=client_email,
            project_budget_estimate=project_budget,
            project_brief_body=project_brief
        )

        # Trigger an elegant web confirmation alert response banner
        messages.success(request, f"System Node Alert: Project submission from {client_name} logged safely.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect('/')
