# Foundry360

Foundry360 is an institutional lost-property operations platform for Kenyan organizations. It manages reporting, matching, verification, custody, transfers, notifications, and disposal records while the institution remains the physical custodian.

## Workspace

- `frontend/`: Next.js 15, React 19, TypeScript, App Router, Tailwind
- `backend/`: Django REST foundation and tenant-aware domain models
- `infra/`: deployment assets to be added as services are productionized
- `ARCHITECTURE.md`: production boundaries and security decisions
- `DEPLOYMENT.md`: Render, Supabase, Vercel, Redis, and Cloudflare R2 setup
- `docker-compose.yml`: local PostgreSQL 16 and Redis 7 services

## Development foundations

Frontend:

```bash
cd frontend
npm run lint
npm run build
```

Backend:

```bash
cd backend
python3 -m pip install -r requirements.txt
python3 manage.py check
python3 manage.py makemigrations
python3 manage.py migrate
```

The application is not wired to external messaging, payments, or object storage yet. Those integrations should be added behind queued service adapters after authentication and tenant authorization are in place.

## Deployment

The free-tier deployment path is documented in [DEPLOYMENT.md](DEPLOYMENT.md). It uses Render for Django, Supabase for PostgreSQL, a Redis-compatible Key Value service, Vercel for Next.js, and Cloudflare R2 for private media.
