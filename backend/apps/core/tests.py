from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Membership, Organization


class TenantApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="officer", password="test-pass")
        self.organization = Organization.objects.create(name="Test University", slug="test-university")
        Membership.objects.create(user=self.user, organization=self.organization, role=Membership.Role.OFFICER)
        self.client.force_authenticate(self.user)

    def test_dashboard_requires_membership(self):
        response = self.client.get(f"/api/organizations/{self.organization.pk}/dashboard/")
        self.assertEqual(response.status_code, 200)

    def test_unknown_tenant_is_forbidden(self):
        response = self.client.get("/api/organizations/9999/dashboard/")
        self.assertEqual(response.status_code, 403)
