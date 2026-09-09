# Foundry360 API Guide

Base URL in local development:

```text
http://localhost:8000/api
```

Base URL in the hosted environment:

```text
https://<render-service>.onrender.com/api
```

All JSON requests should send:

```http
Accept: application/json
Content-Type: application/json
```

## Health

### `GET /health/`

Public service health check.

Response:

```json
{"service":"foundry360-api","status":"ok"}
```

## Public endpoints

These endpoints do not require staff authentication. They must be rate-limited before production use.

### `GET /public/organizations/`

Returns organizations and their active receiving points.

Response shape:

```json
[
  {
    "id": 1,
    "name": "Example School",
    "slug": "example-school",
    "receiving_points": [
      {
        "id": 4,
        "name": "Main reception",
        "kind": "RECEPTION",
        "address": "Main gate",
        "opening_hours": "08:00-17:00",
        "contact_phone": "0700000000"
      }
    ]
  }
]
```

Do not add public endpoints that expose item lists, private descriptions, photos, claimant names, phone numbers, storage bins, or audit events.

### `POST /public/lost-reports/`

Creates a lost report and generates the reference server-side.

Request:

```json
{
  "organization": 1,
  "claimant_name": "Example Claimant",
  "claimant_phone": "0712345678",
  "category": "Electronics",
  "description": "Black phone with a cracked corner and a blue case",
  "last_seen_location": "Library entrance"
}
```

The backend assigns `lost_at` when omitted and generates a reference such as `LR-20260909-0001`.

Production requirements still needed:

- Normalize Kenyan phone numbers.
- Rate-limit by IP and phone number.
- Send OTP before exposing status.
- Validate consent and retention notice.
- Do not return unnecessary claimant PII in the response.

### `POST /public/found-items/`

Creates a found-item record for an active receiving point.

Request:

```json
{
  "organization": 1,
  "location": 4,
  "category": "Bags",
  "title": "Blue backpack",
  "private_description": "Small tear on the right strap; red key tag inside"
}
```

The backend checks that the location belongs to the organization, is active, and is configured as a receiving point. It assigns `found_at` when omitted and generates a reference such as `LP-20260909-0001`.

The public endpoint should eventually create a preliminary report rather than treating the item as fully received until an officer confirms physical handover.

## Staff endpoints

Staff endpoints are nested by organization:

```text
/organizations/<organization_id>/
```

A valid authenticated membership is required.

### Dashboard

```http
GET /organizations/1/dashboard/
```

Response:

```json
{
  "open_cases": 24,
  "possible_matches": 7,
  "pending_claims": 4,
  "recovery_rate": 72,
  "category_breakdown": [
    {"category": "Electronics", "total": 14}
  ]
}
```

### CRUD resources

The DRF router currently exposes:

```text
GET    /organizations/1/locations/
POST   /organizations/1/locations/
GET    /organizations/1/locations/<id>/
PATCH  /organizations/1/locations/<id>/
DELETE /organizations/1/locations/<id>/

GET    /organizations/1/bins/
POST   /organizations/1/bins/
GET    /organizations/1/found-items/
POST   /organizations/1/found-items/
GET    /organizations/1/lost-reports/
POST   /organizations/1/lost-reports/
GET    /organizations/1/matches/
POST   /organizations/1/matches/
GET    /organizations/1/claims/
POST   /organizations/1/claims/
```

Available filters include:

```text
found-items?status=STORED
found-items?category=Electronics
found-items?restricted=true
lost-reports?status=OPEN
lost-reports?category=Bags
claims?status=SUBMITTED
```

## Authentication status

The current API foundation uses DRF session and Basic authentication. This is suitable for development and internal checks, but the production application needs a deliberate staff authentication flow, such as secure cookie sessions or short-lived access tokens with refresh rotation.

Do not put service credentials in browser JavaScript. Public browser variables such as `NEXT_PUBLIC_API_URL` are not secrets.

## Error shape

Expected DRF validation response:

```json
{
  "location": ["Choose an active receiving point for this institution."]
}
```

Expected authorization response:

```json
{"detail":"Authentication credentials were not provided."}
```

## API implementation rules

- Resolve organization access from the authenticated membership, not a client-provided organization claim.
- Scope every queryset by organization.
- Validate all organization-owned foreign keys against the active organization.
- Use opaque references for public users.
- Never serialize private descriptions or photos in public endpoints.
- Create audit records for state transitions and sensitive reads.
- Make notification callbacks and payment callbacks idempotent.
