from django.urls import include, path
from .views import health
from .public_views import PublicFoundItemCreateView, PublicLostReportCreateView, PublicOrganizationListView

urlpatterns = [
	path("health/", health, name="health"),
	path("public/organizations/", PublicOrganizationListView.as_view(), name="public-organizations"),
	path("public/lost-reports/", PublicLostReportCreateView.as_view(), name="public-lost-report"),
	path("public/found-items/", PublicFoundItemCreateView.as_view(), name="public-found-item"),
	path("organizations/<int:organization_id>/", include("apps.core.api_urls")),
]
