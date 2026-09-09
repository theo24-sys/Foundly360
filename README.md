# Foundry360

Foundry360 is a multi-tenant lost-property operations platform for Kenyan institutions. It connects the public user who lost or found an item with the institution responsible for receiving, storing, verifying, transferring, and returning it.

The institution remains the physical custodian. Foundry360 provides the accountable digital trail.

## Product shape

Foundry360 supports three connected experiences:

- **Public users** report lost items, report found items, choose an institution and receiving point, receive a private reference, and check case status.
- **Institution teams** intake property, manage receiving points and storage bins, review matches and claims, record custody events, and complete verified handovers.
- **Platform administrators** onboard institutions, manage support and subscriptions, and monitor system health.

The platform is designed for schools, universities, hotels, hospitals, offices, malls, estates, churches, airports, bus terminals, and other organizations with a physical lost-property desk.

## Current status

### Implemented foundation

- Next.js public landing page and responsive route shell.
- Public routes for lost reports, found reports, and case status.
- Institution workspace route at `/app`.
- Platform administration route at `/admin`.
- Institution team and role route at `/app/team`.
- Staff found-item intake route at `/app/found-items/new`.
- Public organization and receiving-point discovery API.
- Public lost-report and found-item submission API.
- Server-generated case references.
- Multi-tenant Django domain models.
- Organization membership roles.
- Receiving points with type, opening hours, address, and contact phone.
- Found items, lost reports, claims, match suggestions, transfers, disposal, notifications, payments, audit, retention, and preventative-tag models.
- Tenant-scoped staff API foundation.
- PostgreSQL, Redis, Celery, Cloudflare R2, Render, Vercel, and Supabase configuration.
- Docker and Docker Compose foundations.

### Still required before handling real institutional records

- Production staff authentication and role-specific authorization.
- OTP delivery and public case verification.
- Live match-scoring workflow.
- Collection PIN generation, verification, and handover receipts.
- Private R2 upload and presigned-download endpoints.
- Audit events throughout every sensitive state transition.
- Africa's Talking, WhatsApp Cloud API, and Daraja adapters.
- Retention and PII anonymization jobs.
- Automated backend, frontend, and browser tests.
- Backups, restore testing, monitoring, rate limiting, and production privacy review.

Use fake data until these controls are complete.

## Repository structure

```text
.
├── backend/                 Django REST API and domain models
│   ├── apps/core/           Organizations, reports, claims, custody, API
│   ├── config/              Settings, WSGI, Celery, provider configuration
│   ├── manage.py
│   └── requirements.txt
├── frontend/                Next.js 15 and React 19 application
│   ├── src/app/             Public, staff, institution, and admin routes
│   └── src/lib/api.ts       Browser API client
├── docs/                    Product, API, operations, and security guides
├── infra/                   Nginx configuration
├── ARCHITECTURE.md          Runtime topology and security boundaries
├── DEPLOYMENT.md            Render, Supabase, Redis, Vercel, and R2 setup
├── docker-compose.yml       Local PostgreSQL, Redis, API, web, and Nginx
├── Dockerfile               Root Render Docker image for the Django API
├── render.yaml              Render API and worker blueprint
├── vercel.json              Vercel project configuration
└── LICENSE                  Apache License 2.0
```

## Technology

### Frontend

- Next.js 15.5
- React 19.1
- TypeScript
- App Router
- Tailwind CSS 4
- Responsive public and staff experiences

### Backend

- Python 3.12
- Django 5.1
- Django REST Framework
- PostgreSQL 16 through `DATABASE_URL`
- Redis and Celery
- Gunicorn
- WhiteNoise
- `boto3` for Cloudflare R2-compatible storage

### Hosting path

- Vercel for the Next.js frontend
- Render for the Django API
- Supabase PostgreSQL pooler for hosted database access
- Redis-compatible Key Value service for Celery and cache
- Cloudflare R2 for private media
- GitHub for source control

## Local development

### Prerequisites

- Node.js 22 or newer
- npm
- Python 3.12
- Docker or Podman with Compose support

### Frontend

```bash
cd frontend
npm ci
npm run dev
```

Open `http://localhost:3000`.

Validation:

```bash
npm run lint
npm run build
```

### Backend

Create the isolated environment once:

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Copy the environment template from the repository root and configure local values:

```bash
cd ..
cp .env.example .env
```

Run checks and migrations:

```bash
cd backend
PYTHONPATH=. .venv/bin/python manage.py check
PYTHONPATH=. .venv/bin/python manage.py makemigrations
PYTHONPATH=. .venv/bin/python manage.py migrate
```

Run the API locally:

```bash
PYTHONPATH=. .venv/bin/python manage.py runserver
```

The API health endpoint is `http://localhost:8000/api/health/`.

### Docker Compose

The Compose file starts PostgreSQL, Redis, the Django API, the Next.js app, and Nginx:

```bash
cp .env.example .env
docker compose up --build
```

Use Docker Compose for local integration only. Do not expose PostgreSQL or Redis publicly in production.

## API entry points

Local base URL:

```text
http://localhost:8000/api
```

Public endpoints:

```text
GET  /public/organizations/
POST /public/lost-reports/
POST /public/found-items/
GET  /health/
```

Tenant-scoped staff endpoints:

```text
GET    /organizations/<organization_id>/dashboard/
GET    /organizations/<organization_id>/locations/
GET    /organizations/<organization_id>/bins/
GET    /organizations/<organization_id>/found-items/
GET    /organizations/<organization_id>/lost-reports/
GET    /organizations/<organization_id>/matches/
GET    /organizations/<organization_id>/claims/
```

Full payloads, response examples, filters, and authorization rules are in [docs/API.md](docs/API.md).

## Environment variables

Never commit a real `.env` file. Use `.env.example` as a names-only template.

Core deployment variables:

```text
DJANGO_DEBUG=0
DJANGO_SECRET_KEY=<secret>
DJANGO_ALLOWED_HOSTS=<render-hostname>
CORS_ALLOWED_ORIGINS=https://<vercel-domain>
CSRF_TRUSTED_ORIGINS=https://<vercel-domain>
DATABASE_URL=<Supabase pooler URL>
REDIS_URL=<Redis TLS URL>
```

Cloudflare R2 variables:

```text
R2_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com
R2_BUCKET_NAME=<private-bucket>
R2_ACCESS_KEY_ID=<bucket-scoped-access-key>
R2_SECRET_ACCESS_KEY=<bucket-scoped-secret>
```

Admin bootstrap variables are temporary deployment secrets:

```text
FOUNDRY_ADMIN_USERNAME=<non-obvious-username>
FOUNDRY_ADMIN_EMAIL=<private-email>
FOUNDRY_ADMIN_PASSWORD=<password-at-least-6-characters>
```

Remove `FOUNDRY_ADMIN_PASSWORD` after the first successful deployment. See [DEPLOYMENT.md](DEPLOYMENT.md) for provider-specific configuration.

## Deployment

The supported free-tier path is:

```text
GitHub
  ├── Vercel       Next.js frontend
  └── Render       Django API
        ├── Supabase PostgreSQL
        ├── Redis-compatible Key Value
        └── Cloudflare R2 private media
```

Important platform settings:

- Vercel Root Directory: `frontend`
- Vercel Install Command: `npm ci`
- Vercel Build Command: `npm run build`
- Render Docker context: repository root when using the root `Dockerfile`
- Render `DATABASE_URL`: Supabase Session Pooler or compatible pooler URL, not the direct IPv6 database host
- `DJANGO_ALLOWED_HOSTS`: hostnames only, without `https://` or trailing slash
- CORS and CSRF origins: full `https://` origins without trailing slash

Follow [DEPLOYMENT.md](DEPLOYMENT.md) step by step. Do not accept real IDs, claimant phone numbers, or sensitive photos on free infrastructure until backups, privacy controls, and retention policies have been reviewed.

## Documentation

- [Product guide](docs/PRODUCT.md): roles, journeys, receiving points, and product boundaries
- [API guide](docs/API.md): endpoints, payloads, filters, and security rules
- [Operations runbook](docs/OPERATIONS.md): desk procedures, claims, transfers, disposal, and rollback
- [Security guide](docs/SECURITY.md): tenant isolation, privacy, secrets, retention, and production checklist
- [Architecture](ARCHITECTURE.md): system topology and design decisions
- [Deployment](DEPLOYMENT.md): hosted setup and troubleshooting

## License

Foundry360 is licensed under the [Apache License 2.0](LICENSE).

The license permits use, reproduction, modification, and distribution subject to its terms. Review the complete [LICENSE](LICENSE) file before redistributing the project or creating a commercial derivative.
