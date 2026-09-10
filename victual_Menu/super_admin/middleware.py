from django.http import HttpResponse
from django.apps import apps

class MultiTenantSubdomainRouterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. CRITICAL ASSET ENGINE GUARD (Your exact working asset fix kept completely intact!)
        if request.path_info.startswith('/static/') or request.path_info.startswith('/media/'):
            return self.get_response(request)

        # 2. Grab the clean host string header from the browser request (e.g., "foodco.corex.ng")
        raw_host = request.get_host().lower()

        # SAFE PORT SPLIT: Drops the port suffix ":8000" if it exists, leaves a pure domain string
        host_domain = raw_host.split(':')[0]

        # THE MASTER DOMAIN WIRE ALIGNMENT MAP:
        production_domain = "corex.ng"
        local_testing_domain = "localhost"
        ngrok_testing_domain = "ngrok-free.dev"

        subdomain_token = None

        # 3. Extract the subdomain token based on the active link tunnel channel
        if local_testing_domain in host_domain and host_domain != local_testing_domain:
            subdomain_token = host_domain.split('.')[0]

        elif production_domain in host_domain and host_domain != production_domain:
            subdomain_token = host_domain.split('.')[0]

        elif ngrok_testing_domain in host_domain and host_domain != ngrok_testing_domain:
            subdomain_token = host_domain.split('.')[0]

        # 4. If a valid merchant slug is detected, route dynamically using the Domain Engine table rows
        ignored_subdomains = ['www', 'admin', 'portal', 'api', 'superadmin', 'extrude-chlorine-cycle']

        if subdomain_token and subdomain_token not in ignored_subdomains:
            # Clean and force everything to lowercase universally
            formatted_slug = subdomain_token.strip().lower()

            # Unified session parameter injection variables (Matches all your applications)
            request.tenant_slug_token = formatted_slug
            request.custom_slug = formatted_slug
            request.restaurant_slug = formatted_slug

            # Set default fallbacks so the variable always exists
            slugs = 'modern5'

            try:
                # Dynamically fetch the model mapping from your super_admin app setup
                DomainEngineModel = apps.get_model(app_label='super_admin', model_name='DomainEngine')
                router_record = DomainEngineModel.objects.filter(slug_name__iexact=formatted_slug).first()

                if router_record:
                    slugs = router_record.app_target  # Inject 'store', 'modern', etc.

            except Exception:
                # Safe fallback if database queries fail entirely
                slugs = 'modern5'

            # DYNAMIC PATH ROUTING TRANSFORMATION RAIL:
            # FIXED: Checks if the path already contains the slug prefix to prevent doubling!
            prefix_check = f"/{slugs}/{formatted_slug}/"
            if not request.path_info.startswith(prefix_check):
                request.path_info = f"/{slugs}/{formatted_slug}{request.path_info}"

        # 🟢 FIX: Moved out of the IF block so standard root domain requests complete successfully!
        return self.get_response(request)
