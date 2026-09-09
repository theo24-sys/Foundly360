# Foundry360 Product Guide

## Purpose

Foundry360 is institutional lost-property software for schools, universities, hotels, hospitals, offices, malls, transport hubs, estates, churches, and public venues.

The institution remains the physical custodian. Foundry360 provides the digital record from reporting through verified return.

It is not a public marketplace where people publish detailed descriptions of valuable items. Public users submit a report; authorized institution staff control matching, hidden evidence, approval, storage, and handover.

## User types

### Public user

A claimant or finder who does not need an account to begin.

Public users can:

- Report an item they lost.
- Report an item they found.
- Choose the responsible institution.
- Choose or receive instructions for a receiving point.
- Receive a case reference.
- Check case progress with a reference and phone verification.

Public users must not see private item photos, phone numbers belonging to other users, hidden evidence, storage details, or the full institution case list.

### Officer

An institution staff member who handles daily intake and handover.

Officers can:

- Register found items.
- Assign a receiving location and storage bin.
- Record custody events.
- Review claimant evidence.
- Complete a verified collection.

### Supervisor

A staff member who handles decisions and exceptions.

Supervisors can:

- Approve or reject claims.
- Review restricted items.
- Authorize transfers.
- Review disposal queues.
- Inspect audit history.

### Organization admin

The institution's administrator.

Organization admins can:

- Manage locations and receiving points.
- Manage bins and storage rules.
- Invite and deactivate staff.
- Assign roles.
- Configure operating hours and contact details.
- Review institution reports.

### Platform admin

Foundry360 staff responsible for the SaaS platform.

Platform admins can:

- Onboard organizations.
- Manage platform-level support.
- Review subscriptions and payments.
- Investigate system health.
- Access tenant data only through explicit, audited support workflows.

## Main journeys

### Lost item

1. User opens the public report page.
2. User selects an institution.
3. User enters a phone number, category, last-seen location, and description.
4. API creates a private `LostReport` reference.
5. Matching services compare the report to stored found items.
6. Staff review suggestions using hidden identifying evidence.
7. Staff request more evidence, approve, or reject the claim.
8. Approved claimant receives collection instructions.
9. Staff verify the collection PIN and record a custody event.
10. Case becomes resolved and later enters the retention policy.

### Found item

1. Finder selects the responsible institution.
2. Finder selects a receiving point such as security, reception, registry, or property store.
3. Finder describes the item without publishing sensitive identifiers.
4. API creates a private `FoundItem` reference.
5. Staff physically receive and inspect the item.
6. Staff assign a storage bin and record the first custody event.
7. Item becomes available for matching.
8. Staff approve a verified claim or retain it for the institution's policy period.

### Receiving point

Each institution can have multiple places where items are accepted or collected:

- Main reception
- Security desk
- Registry office
- Student affairs office
- Library property desk
- Hotel front desk
- Hospital security office
- Property store
- Branch or campus desk

Each receiving point has a name, type, address, opening hours, phone number, and active/inactive state. Public forms should only offer active receiving points.

### School operating model

A school or university should configure at least:

- Main gate security desk
- Main reception
- Student affairs or registry desk
- Boarding/residence desk where applicable
- Library or student centre desk
- Central property store
- One supervisor responsible for approvals

The institution should publish QR codes at gates, noticeboards, libraries, hostels, halls, and event venues. QR codes should open the public report flow and identify the institution or receiving point without exposing private cases.

## Status concepts

### Found item status

- `STORED`: physically held and assigned to a custody location.
- `MATCHED`: a possible lost-report match exists.
- `CLAIM_PENDING`: a claimant is awaiting staff review.
- `RETURNED`: verified handover completed.
- `DISPOSED`: handled under the institution's policy.

### Lost report status

- `OPEN`: report is awaiting a match.
- `MATCHED`: one or more possible found items were associated.
- `RESOLVED`: item returned or another resolution recorded.
- `CLOSED`: administrative case closure.

### Claim status

- `SUBMITTED`: claimant has submitted evidence.
- `EVIDENCE_REQUIRED`: staff need more information.
- `APPROVED`: collection can be scheduled.
- `REJECTED`: evidence did not establish ownership.
- `COLLECTED`: handover completed.

## Product boundaries

### Included in the current foundation

- Multi-tenant organization model.
- Staff membership roles.
- Found items, lost reports, claims, matches, transfers, bins, locations, disposal, notifications, payments, audit, retention, and preventative-tag models.
- Tenant-scoped staff API routes.
- Public organization discovery.
- Public lost and found submission endpoints.
- Next.js public, staff, institution-admin, and platform-admin route shells.
- Render, Vercel, Supabase, Redis, and R2 deployment configuration.

### Still required before production use

- Real staff authentication UI and session/token lifecycle.
- API-backed organization onboarding.
- OTP delivery and case verification.
- Real matching service and scoring rules.
- R2 presigned upload and download endpoints.
- Collection PIN generation, hashing, and verification.
- Role-specific server permissions beyond membership existence.
- Audit event creation in every sensitive workflow.
- Real SMS, WhatsApp, payment, and retention adapters.
- Automated tests and browser acceptance tests.

The current frontend route forms provide the interaction shape, but every critical workflow must be connected to the backend before real institutional data is accepted.
