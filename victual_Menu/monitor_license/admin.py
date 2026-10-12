
import secrets
from datetime import timedelta

from django.contrib import admin, messages
from django.utils import timezone
from django.db import transaction

from .models import (
    MonitorLicense,
    LicenseRequest,
    SubscriptionPlan,
    CompanySubscription,
)


def find_company_subscription(company_name, email, product_name):
    return CompanySubscription.objects.filter(
        company_name__iexact=company_name.strip(),
        email__iexact=email.strip(),
        product_name__iexact=product_name.strip(),
        status='active',
    ).select_related('plan').order_by('-created_at').first()



def validate_company_subscription(subscription):
    now = timezone.now()

    if subscription is None:
        return False, (
            "No active company subscription matches these company details."
        )

    if subscription.expires_at <= now:
        return False, "The company subscription has expired."

    if subscription.starts_at and subscription.starts_at > now:
        return False, "The company subscription has not started yet."

    if not subscription.plan.is_active:
        return False, "The subscription plan is inactive."

    if subscription.plan.device_limit <= 0:
        return False, "The subscription plan has no available device capacity."

    registered_count = subscription.device_licenses.filter(
        status='active',
        expires_at__gt=now,
    ).count()

    if registered_count >= subscription.plan.device_limit:
        return False, (
            f"This company has reached its device limit of "
            f"{subscription.plan.device_limit}."
        )

    return True, "Subscription is valid and has device capacity."



@admin.register(MonitorLicense)
class MonitorLicenseAdmin(admin.ModelAdmin):
    list_display = [
        'company_name',
        'email',
        'product_name',
        'installation_id',
        'status',
        'expires_at',
    ]

    search_fields = [
        'company_name',
        'email',
        'installation_id',
        'license_key',
    ]

    list_filter = [
        'status',
        'product_name',
    ]


@admin.register(LicenseRequest)
class LicenseRequestAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'email',
        'product_name',
        'installation_id',
        'plan',
        'status',
        'requested_at',
    )

    search_fields = [
        'company_name',
        'email',
        'installation_id',
    ]

    list_filter = [
        'status',
        'product_name',
    ]

    readonly_fields = [
        'requested_at',
        'reviewed_at',
    ]

    actions = ['approve_license_requests']



    @admin.action(
        description='Approve requests and activate company subscription'
    )
    def approve_license_requests(self, request, queryset):
        issued = 0
        skipped = 0

        for request_id in queryset.values_list('id', flat=True):
            try:
                with transaction.atomic():
                    license_request = (
                        LicenseRequest.objects
                        .select_for_update(of=('self',))
                        .select_related('plan')
                        .get(pk=request_id)
                    )

                    if license_request.status != 'pending':
                        skipped += 1
                        continue

                    now = timezone.now()

                    # Prevent duplicate licenses for this installation.
                    if MonitorLicense.objects.filter(
                        installation_id=license_request.installation_id
                    ).exists():
                        self.message_user(
                            request,
                            f'{license_request.installation_id} already '
                            'has a license. No new license was issued.',
                            level=messages.WARNING,
                        )
                        skipped += 1
                        continue

                    plan = license_request.plan

                    if not plan or not plan.is_active:
                        self.message_user(
                            request,
                            f'{license_request.company_name}: '
                            'The selected subscription plan is missing '
                            'or inactive.',
                            level=messages.ERROR,
                        )
                        skipped += 1
                        continue

                    # Reuse an active subscription for this company.
                    subscription = find_company_subscription(
                        license_request.company_name,
                        license_request.email,
                        license_request.product_name,
                    )

                    if subscription:
                        # Do not silently switch an existing customer
                        # to a different plan.
                        if subscription.plan_id != plan.id:
                            self.message_user(
                                request,
                                f'{license_request.company_name}: '
                                'This company already has a subscription '
                                'on a different plan. Review it first.',
                                level=messages.ERROR,
                            )
                            skipped += 1
                            continue

                        valid, reason = validate_company_subscription(
                            subscription
                        )

                        if not valid:
                            self.message_user(
                                request,
                                f'{license_request.company_name}: {reason}',
                                level=messages.ERROR,
                            )
                            skipped += 1
                            continue

                    else:
                        # Create a yearly subscription from the selected plan.
                        subscription = CompanySubscription.objects.create(
                            company_name=license_request.company_name,
                            email=license_request.email,
                            product_name=license_request.product_name,
                            plan=plan,
                            status='active',
                            starts_at=now,
                            expires_at=now + timedelta(
                                days=plan.duration_days
                            ),
                        )

                    valid, reason = validate_company_subscription(
                        subscription
                    )

                    if not valid:
                        self.message_user(
                            request,
                            f'{license_request.company_name}: {reason}',
                            level=messages.ERROR,
                        )
                        skipped += 1
                        continue

                    device_expiry = subscription.expires_at

                    # Issue the license under the company subscription.
                    MonitorLicense.objects.create(
                        company_name=subscription.company_name,
                        email=subscription.email,
                        product_name=subscription.product_name,
                        installation_id=license_request.installation_id,
                        license_key=(
                            f'FNM-{secrets.token_hex(16).upper()}'
                        ),
                        expires_at=device_expiry,
                        status='active',
                        subscription=subscription,
                    )

                    license_request.status = 'approved'
                    license_request.reviewed_at = now
                    license_request.save(
                        update_fields=['status', 'reviewed_at']
                    )

                    issued += 1

            except Exception as exc:
                # Roll back the current request and report the failure.
                self.message_user(
                    request,
                    f'Request {request_id} failed: {exc}',
                    level=messages.ERROR,
                )
                skipped += 1

        if issued:
            self.message_user(
                request,
                f'{issued} device license(s) issued successfully.',
                level=messages.SUCCESS,
            )

        if skipped:
            self.message_user(
                request,
                f'{skipped} request(s) skipped. Review the messages above.',
                level=messages.WARNING,
            )

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'device_limit',
        'duration_days',
        'price',
        'is_active',
    ]

    search_fields = ['name']

    list_filter = ['is_active']



@admin.register(CompanySubscription)
class CompanySubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'company_name',
        'email',
        'plan',
        'device_limit',
        'registered_devices',
        'status',
        'starts_at',
        'expires_at',
    ]

    search_fields = [
        'company_name',
        'email',
    ]

    list_filter = [
        'plan',
        'status',
    ]

    @admin.display(description='Device limit')
    def device_limit(self, obj):
        return obj.plan.device_limit

    @admin.display(description='Registered devices')
    def registered_devices(self, obj):
        return obj.device_licenses.count()
