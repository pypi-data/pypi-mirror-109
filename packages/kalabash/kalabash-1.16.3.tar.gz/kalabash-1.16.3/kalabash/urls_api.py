"""External API urls."""

from django.urls import include, path

from kalabash.core.extensions import exts_pool

app_name = "api"

urlpatterns = [
    path('', include("kalabash.admin.urls_api")),
    path('', include("kalabash.limits.urls_api")),
    path('', include("kalabash.relaydomains.urls_api")),
] + exts_pool.get_urls(category="api")
