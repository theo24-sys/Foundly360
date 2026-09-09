from django.urls import include, path
from .views import health

urlpatterns = [
	path("health/", health, name="health"),
	path("organizations/<int:organization_id>/", include("apps.core.api_urls")),
]
