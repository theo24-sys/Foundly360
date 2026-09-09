# Foundry360 Security and Privacy Guide

## Threat model

Foundry360 handles names, phone numbers, location information, photos, item descriptions, identity documents, claim evidence, and institutional custody history.

Primary risks:

- One institution viewing another institution's cases.
- A stranger learning enough about an item to make a false claim.
- Public photos exposing IDs or contact details.
- A compromised staff account approving or releasing property.
- Lost or leaked provider credentials.
- Unverified payment callbacks.
- Data retained after the approved purpose has ended.
- Background jobs sending sensitive information to the wrong recipient.

## Tenant isolation

Every organization-owned object must contain an organization relationship. Staff access must be derived from an active `Membership`.

Required rules:

- Filter every staff queryset by the active organization.
- Validate foreign keys such as locations, bins, items, and claims against the same organization.
- Do not trust an organization ID supplied by the browser as authorization.
- Use explicit platform-admin support access with audit records.
- Add tests for cross-tenant reads, creates, updates, deletes, and file URLs.

## Public privacy

Public routes may expose:

- Institution name and public receiving points.
- Public operating hours and contact instructions.
- The submitting user's own opaque reference after submission.

Public routes must not expose:

- Other claimant names or phone numbers.
- Full item lists.
- Private descriptions.
- Storage bins.
- Unredacted document photos.
- Hidden match signals.
- Internal officer names or audit records.

## Authentication

Staff authentication must eventually include:

- Strong password or institution-managed authentication.
- Secure, HttpOnly, SameSite cookies or a carefully designed token flow.
- Session expiration and logout.
- Login throttling.
- Password reset with single-use expiring links.
- Optional MFA for organization and platform admins.
- Audit records for sign-in, failed sign-in, sensitive reads, exports, and role changes.

Public claimant access should use OTP or another expiring verification flow. Do not make a public claimant create a permanent password to submit a first report.

## Files and R2

- Keep the R2 bucket private.
- Use presigned URLs with short expiration.
- Authorize the user before generating a URL.
- Validate MIME type, extension, size, and image dimensions.
- Re-encode images to remove hidden metadata where appropriate.
- Generate redacted previews for identity documents.
- Store objects under tenant-scoped keys.
- Do not put phone numbers or national ID numbers in object names.
- Plan malware scanning before accepting arbitrary uploads.

## Sensitive categories

Require additional review for:

- National IDs
- Passports
- Bank cards
- Keys
- Medication
- Firearms
- Government documents
- Confidential business documents

The public description should remain generic. A staff-only description can contain the verification evidence, subject to access controls.

## Secrets

Never commit:

- Django secret key
- Supabase database URL
- Redis URL
- R2 access key
- R2 secret key
- Africa's Talking credentials
- WhatsApp tokens
- Daraja consumer secrets
- Admin passwords

Use Render, Vercel, Supabase, Cloudflare, or a secrets manager. Rotate a credential if it has ever been pasted into Git, a public issue, a browser-visible variable, or an untrusted chat.

## Data retention

Define retention by organization and category. At minimum, document:

- How long open reports are kept.
- How long returned cases are retained.
- How long disposed cases are retained.
- When claimant names and phone numbers are anonymized.
- Which aggregates remain after anonymization.
- Who can export or delete records.
- How legal holds suspend deletion.

Retention jobs must be idempotent and auditable. Do not permanently erase records before confirming the institution's policy and legal requirements.

## Provider callbacks

SMS, WhatsApp, and Daraja callbacks must:

- Verify provider signatures where available.
- Use an idempotency key.
- Store provider event IDs.
- Reject duplicate state transitions.
- Avoid trusting a client-side payment success message.
- Avoid putting sensitive item data into message templates.

## Production checklist

Before real records:

- [ ] Render `DJANGO_DEBUG=0`.
- [ ] `DATABASE_URL` uses the Supabase pooler.
- [ ] `DJANGO_ALLOWED_HOSTS` contains hostnames only.
- [ ] CORS and CSRF origins contain no trailing slash.
- [ ] Admin bootstrap password has been removed after first use.
- [ ] R2 bucket is private.
- [ ] R2 credentials are scoped to the required bucket.
- [ ] Public endpoints are rate-limited.
- [ ] OTP expiry and retry limits exist.
- [ ] Cross-tenant authorization is tested.
- [ ] PostgreSQL backups are enabled and restore-tested.
- [ ] Error logs do not contain secrets or full claimant data.
- [ ] Institution data-processing agreements are reviewed.
- [ ] ODPC obligations and retention policy are reviewed.
