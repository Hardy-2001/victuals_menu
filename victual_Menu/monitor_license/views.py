from django.shortcuts import render, get_object_or_404
from .models import MonitorLicense
from django.http import JsonResponse
from django.utils import timezone
from .models import MonitorLicense


import json
from django.views.decorators.csrf import csrf_exempt
from .models import MonitorLicense, LicenseRequest, SubscriptionPlan

def license_portal(request, installation_id=None, slug=None):
    license_record = None

    if installation_id:
        license_record = get_object_or_404(
            MonitorLicense,
            installation_id=installation_id
        )

    subscription_plans = SubscriptionPlan.objects.filter(
        is_active=True
    ).order_by('price', 'device_limit')

    return render(
        request,
        'monitor_license/license.html',
        {
            'license': license_record,
            'subscription_plans': subscription_plans,
        }
    )

#==========================stage two===============================

def license_status_api(request, installation_id):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Only GET requests are allowed."},
            status=405
        )

    try:
        license_record = MonitorLicense.objects.get(
            installation_id=installation_id
        )
    except MonitorLicense.DoesNotExist:
        return JsonResponse(
            {
                "installation_id": installation_id,
                "status": "not_found",
                "licensed": False,
                "message": "No license found for this installation."
            },
            status=404
        )

    is_expired = license_record.expires_at <= timezone.now()

    if license_record.status == "revoked":
        effective_status = "revoked"
    elif is_expired:
        effective_status = "expired"
    else:
        effective_status = license_record.status

    licensed = effective_status == "active"

    return JsonResponse({
        "installation_id": license_record.installation_id,
        "company_name": license_record.company_name,
        "product_name": license_record.product_name,
        "status": effective_status,
        "licensed": licensed,
        "expires_at": license_record.expires_at.isoformat(),
    })


@csrf_exempt
def activation_request_api(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed."},
            status=405
        )

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Invalid JSON request body."},
            status=400
        )

    company_name = data.get("company_name", "").strip()
    email = data.get("email", "").strip()
    installation_id = data.get("installation_id", "").strip()
    product_name = data.get(
        "product_name", "FOCUS NOC MONITOR"
    ).strip()
    plan_id = data.get("plan_id")

    if not all([
        company_name,
        email,
        installation_id,
        product_name,
        plan_id,
    ]):
        return JsonResponse(
            {"error": "All fields are required, including a subscription plan."},
            status=400
        )

    if len(company_name) > 150 or len(installation_id) > 150:
        return JsonResponse(
            {"error": "A field exceeds the maximum length."},
            status=400
        )

    if len(product_name) > 150:
        return JsonResponse(
            {"error": "Product name is too long."},
            status=400
        )

    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    from .models import SubscriptionPlan

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse(
            {"error": "Enter a valid email address."},
            status=400
        )

    try:
        selected_plan = SubscriptionPlan.objects.get(
            id=plan_id,
            is_active=True
        )
    except (SubscriptionPlan.DoesNotExist, ValueError, TypeError):
        return JsonResponse(
            {"error": "Please select a valid active subscription plan."},
            status=400
        )

    existing = LicenseRequest.objects.filter(
        installation_id=installation_id,
        status="pending"
    ).first()

    if existing:
        return JsonResponse({
            "message": "A request is already awaiting review.",
            "status": "pending",
            "installation_id": installation_id,
        }, status=200)

    license_request = LicenseRequest.objects.create(
        company_name=company_name,
        email=email,
        installation_id=installation_id,
        product_name=product_name,
        plan=selected_plan,
        status="pending",
    )

    return JsonResponse({
        "message": (
            f"Your request for the {selected_plan.name} plan "
            "has been submitted successfully. Please wait for administrator approval."
        ),
        "request_id": license_request.id,
        "installation_id": license_request.installation_id,
        "plan": selected_plan.name,
        "status": license_request.status,
    }, status=201)
