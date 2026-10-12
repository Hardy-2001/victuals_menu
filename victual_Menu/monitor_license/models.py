from django.db import models


class MonitorLicense(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]

    company_name = models.CharField(max_length=150)

    subscription = models.ForeignKey(
        'CompanySubscription',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='device_licenses',
        help_text="Company subscription this device license belongs to."
    )

    email = models.EmailField()

    product_name = models.CharField(
        max_length=150,
        default='FOCUS NOC MONITOR'
    )

    installation_id = models.CharField(
        max_length=150,
        unique=True
    )

    license_key = models.CharField(
        max_length=255,
        unique=True
    )

    issued_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.company_name} - {self.product_name}"



class LicenseRequest(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    company_name = models.CharField(max_length=150)

    email = models.EmailField()

    product_name = models.CharField(
        max_length=150,
        default='FOCUS NOC MONITOR'
    )

    installation_id = models.CharField(max_length=150)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    requested_at = models.DateTimeField(auto_now_add=True)

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    license_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Choose when the approved license should expire."
    )

    plan = models.ForeignKey(
        'SubscriptionPlan',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='license_requests',
        help_text="Subscription plan selected by the customer."
    )

    def __str__(self):
        return f"{self.company_name} - {self.installation_id}"


class SubscriptionPlan(models.Model):

    name = models.CharField(
        max_length=50,
        unique=True
    )

    device_limit = models.PositiveIntegerField(
        default=5,
        help_text="Maximum number of computers allowed under this plan."
    )

    duration_days = models.PositiveIntegerField(
        default=30,
        help_text="Default subscription duration in days."
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.device_limit} devices"



class CompanySubscription(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]

    company_name = models.CharField(max_length=150)

    email = models.EmailField()

    product_name = models.CharField(
        max_length=150,
        default='FOCUS NOC MONITOR'
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    starts_at = models.DateTimeField(
        null=True,
        blank=True
    )

    expires_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} - {self.plan.name}"
