from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import PlatformSetting, ShowcaseTemplate, InfrastructureMailLog



def platform_landing_home_view(request):
    """
    👑 MASTER SAAS PLATFORM HOMEPAGE ROUTER
    Queries global configuration settings and displays your beautiful landing.html template!
    """
    platform_config = PlatformSetting.objects.first()
    showcase_cards = ShowcaseTemplate.objects.all()

    context = {
        'platform_config': platform_config,
        'showcase_cards': showcase_cards,
    }

    # 🎯 FIXED: Renders your custom 'landing.html' filename from the super_admin path!
    return render(request, 'super_admin/landing.html', context)


def platform_landing_images_subs_view(request):
    """
    🖼️ LANDING IMAGE SUPPORTING VIEW ROUTER
    Loads your secondary ambient 'landing_image.html' viewport seamlessly.
    """
    platform_config = PlatformSetting.objects.first()

    context = {
        'platform_config': platform_config,
    }

    # 🎯 FIXED: Renders your custom 'landing_image.html' template file!
    return render(request, 'super_admin/landing_images.html', context)


def platform_explore_templates_view(request):
    """
    📁 EXPLORE LAYOUTS MOUNT ENGINE CONTROLLER
    🎯 FIXED: Captures requests for the template layout slider page and passes
    your newly added admin database cards straight into the bubble scroller rows loop!
    """
    # Pulls your 'DINER MENU' and 'Menu' upload image records from your new super_admin table!
    showcase_cards = ShowcaseTemplate.objects.all()

    context = {
        'showcase_cards': showcase_cards,  # 🎯 KEY MATCH: Feeds your {% for node in showcase_cards %} loop perfectly!
    }

    # Renders your template preview gallery template file
    return render(request, 'super_admin/landing_images.html', context)


def dispatch_console_mail(request):
    """
    📥 TERMINAL PACKET INTERCEPTOR
    Captures message submissions from the main landing page header drawer.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            InfrastructureMailLog.objects.create(
                sender_name=name,
                sender_email=email,
                message_body=message
            )
            messages.success(request, "Secure message transmitted successfully to main infrastructure logs!",
                             extra_tags='terminal_mail')

    return redirect('/')


# ==========================================================================
# 🔒 NEW SECURITY INTERCEPTORS & MULTI-TIERED PORTAL DASHBOARDS
# ==========================================================================

def console_portal_login_view(request):
    """
    🎛️ PORTAL MATRIX LOGIN GATEWAY
    Validates credentials directly against Django's auth database table.
    """
    if request.method == 'POST':
        user_identity = request.POST.get('username', '').strip()
        user_passkey = request.POST.get('password', '')

        user_node = authenticate(request, username=user_identity, password=user_passkey)

        if user_node is not None:
            login(request, user_node)
            messages.success(request, f"Access Authorized. Identity Confirmed: {user_node.username}")

            # 🛡️ ROLE MATRIX PATH ROUTER: Checks who logged in and directs them to their station
            if user_node.is_superuser:
                return redirect('/admin/')
            elif user_node.is_staff or user_node.groups.filter(name='Agents').exists():
                return redirect('super_admin:agent_dashboard')
            else:
                return redirect('super_admin:merchant_dashboard')
        else:
            messages.error(request, "CRITICAL ERROR: Invalid authentication credentials match.",
                           extra_tags='portal_auth')

    return redirect('super_admin:landing_home')


def console_portal_logout_view(request):
    """
    🔌 CONSOLE LOGOUT INTERCEPTOR
    Kills active web sessions cleanly and returns safely to the base terminal display.
    """
    logout(request)
    messages.success(request, "Secure terminal session terminated successfully.")
    return redirect('super_admin:landing_home')


@login_required(login_url='super_admin:landing_home')
def agent_control_deck_view(request):
    """
    🏗️ AGENT COMMAND BRIDGE
    Secure view layer where agents deploy fresh merchant vendor profiles.
    """
    if not (request.user.is_superuser or request.user.is_staff or request.user.groups.filter(name='Agents').exists()):
        return redirect('super_admin:landing_home')

    return render(request, 'super_admin/agent_deck.html')


from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect


def portal_login_view(request):
    """
    🔐 SECURE PORTAL CONTROLLER
    Validates account credentials and sends agents/merchants straight into the native admin dashboard.
    """
    if request.method == 'POST':
        user_ident = request.POST.get('username')
        passkey = request.POST.get('password')

        user = authenticate(request, username=user_ident, password=passkey)

        if user is not None:
            login(request, user)
            request.session.modified = True

            # 🚀 SUCCESS RAIL: Drops them straight into the stable admin tables matrix
            return redirect('/admin/')
        else:
            messages.error(request, "Encryption mismatch: Invalid Username or Security Passkey.")
            return redirect('/')

    return redirect('/')
