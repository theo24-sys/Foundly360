from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api_views import ClaimViewSet, FoundItemViewSet, LocationViewSet, LostReportViewSet, MatchSuggestionViewSet, StorageBinViewSet, dashboard

router = DefaultRouter()
router.register("locations", LocationViewSet)
router.register("bins", StorageBinViewSet)
router.register("found-items", FoundItemViewSet)
router.register("lost-reports", LostReportViewSet)
router.register("matches", MatchSuggestionViewSet)
router.register("claims", ClaimViewSet)

urlpatterns = [path("dashboard/", dashboard, name="dashboard"), path("", include(router.urls))]
