# Foundry360 Free-Tier Deployment

This deployment uses:

- Render web service for Django API
- Render/Upstash Redis-compatible Key Value for Redis
- Supabase PostgreSQL
- Vercel for Next.js
- Cloudflare R2 for private media
- GitHub as the source repository

Do not place provider keys in Git. Add them through each platform's environment-variable dashboard.

## 1. Supabase

1. Create a Supabase project.
2. Open **Connect** and choose the **Session pooler** connection, not the direct connection.
3. Use the pooler connection string as `DATABASE_URL` on Render.
4. Keep the Supabase database password private.

Do not use the direct `db.<project-ref>.supabase.co:5432` connection on Render. It can resolve to IPv6, which may produce `Network is unreachable`. Use the Supabase pooler host instead. Session pooler is the safer default for Django migrations and persistent connections; transaction pooler can be used when Supabase only exposes that option.

The URL should look similar to one of these:

```text
postgresql://postgres.<project-ref>:<password>@aws-0-<region>.pooler.supabase.com:5432/postgres
postgresql://postgres.<project-ref>:<password>@aws-0-<region>.pooler.supabase.com:6543/postgres
```

## 2. Redis

Create a Redis-compatible Key Value instance and copy its TLS URL. Set it as:

```text
REDIS_URL=rediss://default:password@host:port
```

Use the same `REDIS_URL` on both the Render web service and worker. Do not commit the URL.

## 3. Render API

Import the repository and use the included `render.yaml`, or create a Web Service manually:

If you create a **Docker** Web Service manually, keep the repository root as the service root. The root `Dockerfile` now builds the Django API from `backend/`.

If you create a **Python** Web Service manually, set the root directory to `backend` and use the Python commands below.

- Root directory: `backend`
- Runtime: Python
- Build command: `pip install -r requirements.txt`
- Start command: `python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --access-logfile -`
- Health check: `/api/health/`

Add:

```text
DJANGO_DEBUG=0
DJANGO_SECRET_KEY=<long-random-secret>
DJANGO_ALLOWED_HOSTS=foundry360-api.onrender.com
CORS_ALLOWED_ORIGINS=https://your-vercel-app.vercel.app
CSRF_TRUSTED_ORIGINS=https://your-vercel-app.vercel.app
DATABASE_URL=<Supabase pooled URL>
REDIS_URL=<Redis TLS URL>
```

Use no trailing slash for the browser origins. `DJANGO_ALLOWED_HOSTS` is hostname-only and must not include `https://`:

```text
DJANGO_ALLOWED_HOSTS=foundly360-1.onrender.com
CORS_ALLOWED_ORIGINS=https://lost-found-jet.vercel.app
CSRF_TRUSTED_ORIGINS=https://lost-found-jet.vercel.app
```

`DATABASE_URL` is required when `DJANGO_DEBUG=0`. If it is missing, the service will stop with a clear configuration error instead of attempting to connect to `localhost:5432`.

For Supabase, copy the complete pooled connection string, including its username, password, pooler host, port, and database name. Do not enter only the Supabase project URL or the direct `db...supabase.co` host.

After deployment, test:

```text
https://foundry360-api.onrender.com/api/health/
```

The expected response is:

```json
{"service":"foundry360-api","status":"ok"}
```

### Celery worker

The `render.yaml` includes a worker. Free plans may not include an always-on background worker. If Render requires a paid worker, deploy the API first and postpone Celery-dependent features, or run the worker locally during development. Notifications, retention jobs, and media processing should not be treated as reliable until a worker is running continuously.

## 4. Cloudflare R2

1. Create an R2 bucket with a non-public default policy.
2. Create an R2 API token limited to that bucket.
3. Copy the S3-compatible endpoint.
4. Add these Render variables:

```text
R2_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com
R2_BUCKET_NAME=foundry360-media
R2_ACCESS_KEY_ID=<access-key>
R2_SECRET_ACCESS_KEY=<secret-key>
```

Keep the bucket private. Files must be served through short-lived signed URLs after Django authorization. Do not use public bucket URLs for claimant or ID-document photos.

## 5. Vercel frontend

1. Import the same GitHub repository into Vercel.
2. Set **Root Directory** to `frontend` and enable **Include files outside the root directory** only if Vercel asks for it.
3. Framework preset: Next.js.
4. Add this environment variable:

```text
NEXT_PUBLIC_API_URL=https://foundry360-api.onrender.com/api
```

Deploy. Copy the resulting Vercel URL back into Render:

The Vercel root-directory setting is required. It makes Vercel run `npm ci` inside `frontend/`, where `package.json` and `package-lock.json` exist. Do not deploy the repository root as a Next.js project.

```text
CORS_ALLOWED_ORIGINS=https://your-project.vercel.app
CSRF_TRUSTED_ORIGINS=https://your-project.vercel.app
```

Redeploy the API after changing those values.

## 6. First admin user

Render's free plan may not provide Shell access. The Docker entrypoint can create the first admin automatically during deployment when all three variables are present. Add these as Render environment variables:

```text
FOUNDRY_ADMIN_USERNAME=ops-<unique-word>-<random-digits>
FOUNDRY_ADMIN_EMAIL=your-private-admin-email@example.com
FOUNDRY_ADMIN_PASSWORD=<unique-20-plus-character-password>
```

Mark all three as secret/private. Do not use `admin`, `administrator`, `root`, `foundry360`, a name, a phone number, or a password reused anywhere else. Generate the password with a password manager. The command sets `is_staff` and `is_superuser`, and can safely be rerun to rotate the password for that administrator. After the first successful deployment, remove `FOUNDRY_ADMIN_PASSWORD` and redeploy; the account remains available.

The next application step is an organization onboarding command that creates an `Organization` and `Membership` for that user.

## Free-tier safety

Use fake data until backups, access controls, and private media flows are complete. Do not upload national IDs, phone numbers, passports, or real claimant records to a free-tier deployment before reviewing retention, backups, and provider data-processing terms.

Free services may sleep, restart, limit connections, or remove inactive resources. This setup is appropriate for development and a demo, not yet for production institutional records.
