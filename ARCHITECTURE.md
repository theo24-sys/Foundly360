# Foundry360 Production Architecture

## Product boundary

Foundry360 is a multi-tenant lost-property operations platform for Kenyan institutions. Institutions remain the custodians of physical property; Foundry360 manages reporting, matching, verification, custody, communication, transfer, and disposal records.

## Runtime topology

```text
Claimant / security desk
        |
        v
Nginx + Certbot SSL
        |
        +--> Next.js 15 / React 19 PWA
        |
        +--> Django REST Framework API
                 |
                 +--> PostgreSQL 16
                 +--> Redis 7 + Celery
                 +--> Cloudflare R2 private media
                 +--> Africa's Talking SMS
                 +--> Meta WhatsApp Cloud API
                 +--> Safaricom Daraja 2.0
```

## Application layers

| Layer | Technology | Responsibility |
| --- | --- | --- |
| Client | Next.js 15, React 19, TypeScript | App Router, claimant reporting, staff workspace, PWA shell |
| UI | Tailwind CSS, shadcn/ui | Accessible responsive controls and mobile-first layouts |
| Data fetching | TanStack Query | Cache, background refresh, mutation state, offline retry queue |
| API | Django REST Framework on Python 3.12 | Authentication, tenant authorization, workflows, admin API |
| Data | PostgreSQL 16 | Relational records, custody events, JSONB item attributes |
| Jobs | Redis 7 and Celery | OTPs, notifications, media processing, retention purges, reports |
| Media | Cloudflare R2 | Private item photos and documents with 15-minute presigned URLs |
| Deployment | Docker Compose, Gunicorn, Nginx, Certbot | Single VPS deployment with a clear path to separate workers/services |

## Tenant and access model

Every organization-owned record carries `organization_id`. The API resolves the active organization from the authenticated staff membership and applies tenant filtering at the service/query boundary before serialization. Never accept an organization identifier from an untrusted client as the authorization source.

Recommended roles:

- `ORG_ADMIN`: organization settings, staff, reports, retention policy
- `SUPERVISOR`: approvals, transfers, disposal, audit review
- `OFFICER`: intake, storage scans, claimant evidence, collection handover
- `VIEWER`: read-only operational reports
- `PLATFORM_ADMIN`: support and billing across tenants, with explicit audited access

Public claimant flows use opaque case references and OTP verification. They must never expose a tenant-wide search endpoint or raw item identifiers.

## Core domain records

- `Organization`, `Location`, `Membership`
- `FoundItem`, `LostReport`, `MatchSuggestion`, `Claim`
- `StorageBin`, `CustodyEvent`, `Transfer`
- `Notification`, `Payment`, `DisposalEvent`
- `AuditLog`, `RetentionJob`, `PreventativeTag`

`CustodyEvent` is append-only. Status fields provide the current projection, while the event log records who registered, stored, matched, approved, transferred, disposed of, or released an item.

## Security and privacy requirements

- Keep item photos private in R2; issue short-lived presigned URLs only after authorization.
- Store phone numbers and sensitive document details separately from public case metadata where practical.
- Treat national IDs, passports, bank cards, keys, medication, firearms, and official documents as restricted categories with additional approval rules.
- Mask or redact document numbers before staff previews are stored or displayed.
- Use OTPs for claimant access; do not require a claimant account for the initial report.
- Apply organization-level authorization to every read, write, file URL, background task, and admin action.
- Record audit events for sensitive reads, approval decisions, transfers, collection PIN use, and data exports.
- Run retention jobs after return or disposal to anonymize claimant PII while retaining aggregate metrics.
- Keep secrets in environment variables or a secrets manager; never commit provider tokens, Daraja credentials, or R2 keys.

## External integrations

### Africa's Talking

Use for OTP and fallback transactional SMS. Queue sends through Celery, persist provider message IDs, and make delivery callbacks idempotent.

### WhatsApp Cloud API

Use for utility notifications such as claim updates, collection PINs, transfer status, and disposal notices. Store template names and delivery status; do not put sensitive item details in message text.

### Daraja 2.0

Use STK Push for organization subscriptions and optional delivery fees. Keep payment intent, checkout request ID, receipt number, and reconciliation status in a separate payment record. Never treat a client-side success response as payment confirmation.

### Cloudflare R2

Upload through short-lived presigned URLs where possible. Validate content type and size server-side, generate redacted previews asynchronously, and reject public bucket access.

## Deployment baseline

A first production deployment can run on a 4 GB / 2 vCPU Hetzner or DigitalOcean VPS:

- Nginx and Certbot
- Next.js server
- Django/Gunicorn API
- Celery worker and scheduler
- Redis
- PostgreSQL, with encrypted backups and restore checks

Use Docker Compose for the initial deployment. Keep the API, worker, scheduler, and web processes independently scalable even if they share one host at first.

## Delivery sequence

1. Keep the Next.js public journey and institution staff shell aligned with Foundry360 workflows.
2. Implement Django models, tenant-scoped query services, custody events, and staff authentication.
3. Add public claimant reporting with OTP access and private R2 uploads.
4. Add Celery-backed SMS/WhatsApp notifications, retention jobs, and document redaction.
5. Add QR bin tags, transfers, disposal notices, and audit exports.
6. Add Daraja billing and optional delivery only after institutional workflows are stable.

The production application is scaffolded in `frontend/` and `backend/`. External messaging, payments, and object storage adapters will be added behind the API service boundaries. Detailed behavior is documented in `docs/PRODUCT.md`, `docs/API.md`, `docs/OPERATIONS.md`, and `docs/SECURITY.md`.
