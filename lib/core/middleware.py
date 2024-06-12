
from django.core.exceptions import DisallowedHost
from django.db import connection
from django_tenants.middleware.main import TenantMainMiddleware
from django_tenants.utils import get_tenant_model


class ExemptedUrlException(ValueError): ...


class UnauthenticatedRequestException(ValueError): ...


class TenantNotFoundException(ValueError): ...


class TenantMiddleware(TenantMainMiddleware):
    """
    This is simplified tenant middleware which selects the tenant based on authenticated user,
    rather than, selecting tenant from the 'domain'.
    """

    def get_tenant(self, request):
        token = request.headers.get("Authorization", "").replace("Bearer", "").strip()

        print(f"INFO: token: {token} url: [{request.path}]")
        if "/auth/" in request.path or request.path in ["/"]:
            raise ExemptedUrlException("Url don't require tenant!")
        elif not token:
            raise UnauthenticatedRequestException("Unauthenticated request.")

        model = get_tenant_model()
        if hasattr(model, "from_auth_token") and callable(model.from_auth_token):
            try:
                return model.from_auth_token(token)
            except Exception as e:
                raise TenantNotFoundException(f"Tenant Not Found: {e}")
        else:
            raise ValueError(f"ERROR: Unknown tenant model: {model}")

    def process_request(self, request):

        connection.set_schema_to_public()
        try:
            hostname = request.get_host()
        except DisallowedHost:
            from django.http import HttpResponseNotFound

            return HttpResponseNotFound()

        try:
            tenant = self.get_tenant(request)
        except UnauthenticatedRequestException as e:
            print(f"EXCEPTION: {e}")
        except ExemptedUrlException as e:
            print(f"EXCEPTION: {e}")
        except TenantNotFoundException:
            self.no_tenant_found(request, hostname)
        else:
            tenant.domain_url = hostname
            request.tenant = tenant
            connection.set_tenant(request.tenant)
            self.setup_url_routing(request)
