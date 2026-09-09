# Foundry360 Operations Runbook

## Institution onboarding

1. Create the organization.
2. Add locations and mark only real handover desks as receiving points.
3. Add opening hours, address, phone, and escalation contact.
4. Create storage bins with stable codes such as `BOX-A12`.
5. Create the institution admin membership.
6. Add supervisors and officers with the least privilege needed.
7. Print QR codes for public reporting and physical bins.
8. Agree on retention and disposal policy before intake begins.
9. Run a staff orientation using fake records.
10. Start with one campus or branch before enabling all locations.

## Receiving-point procedure

At each desk:

1. Accept the physical item.
2. Ask the finder not to publish sensitive identifiers.
3. Create or confirm the found-item record.
4. Photograph the item only when institution policy allows it.
5. Mark restricted documents and sensitive property.
6. Attach a storage-bin code.
7. Record who received it and when.
8. Place it in secure storage.
9. Confirm the public description contains no hidden ownership evidence.
10. Tell the finder or claimant the correct reference and next step.

Receiving points should display:

- Desk name
- Opening hours
- Contact number
- QR report code
- Instructions for sensitive documents
- Emergency or security escalation instructions

## Claim review

Officers should compare the claimant's evidence against information that was not published publicly.

Good hidden evidence includes:

- Exact damage or sticker placement
- Contents inside a bag
- Wallpaper or lock-screen detail
- Keychain shape
- Unique marking
- Approximate purchase or loss context

Avoid asking claimants to disclose full passwords, banking PINs, national ID PINs, or unnecessary sensitive information.

Supervisors should approve restricted categories such as:

- National IDs and passports
- Bank and ATM cards
- Keys
- Medication
- Firearms
- Official documents
- Confidential workplace documents

## Collection procedure

1. Confirm the claim is approved.
2. Verify claimant identity according to institution policy.
3. Send or read the collection instructions through an approved channel.
4. Ask the claimant for the collection PIN or other controlled proof.
5. Compare the item to the hidden evidence.
6. Record the officer and receiving location.
7. Record the collection time.
8. Update the item to `RETURNED` and claim to `COLLECTED`.
9. Record an append-only custody event.
10. Give the claimant a receipt where institution policy requires it.

Never mark an item returned based only on a web form submission.

## Bulk and event intake

For graduations, sports days, concerts, examinations, and conferences:

- Preselect the event and receiving location.
- Keep reference numbers server-generated.
- Use a separate queue for items waiting for physical confirmation.
- Photograph one item at a time.
- Attach a bin or bag code before moving to the next item.
- Reconcile the digital count with the physical count at the end of the shift.
- Have a supervisor review restricted or high-value items.

## Transfer between locations

For campus or branch transfers:

1. Create a transfer request.
2. Confirm the sending and receiving locations belong to the same organization.
3. Record the item and physical container.
4. Mark the transfer `IN_TRANSIT` only when it leaves the first desk.
5. Receiving staff scan or verify the item.
6. Mark it `RECEIVED` and record the receiving officer.
7. Append custody events at both handovers.

Do not use a transfer to move an item between unrelated tenants.

## Disposal and unclaimed property

Disposal rules vary by institution and item category. The software should support policy configuration, but staff must follow the institution's legal and governance process.

Before disposal:

- Confirm the retention period has elapsed.
- Check for active claims or unresolved matches.
- Issue the required notice.
- Obtain the required supervisor or committee approval.
- Record the disposal method.
- Keep the notice and approval evidence.
- Create a `DisposalEvent` and custody event.
- Anonymize claimant PII according to the approved retention schedule.

Never automatically auction, destroy, or donate restricted documents without the correct authority procedure.

## Service operations

### Health check

```bash
curl https://<render-service>.onrender.com/api/health/
```

### Deployments

- Render web service runs migrations and starts Gunicorn.
- Render worker runs Celery when a worker plan is available.
- Vercel builds the frontend from the `frontend` root.
- Supabase stores PostgreSQL data.
- Redis stores Celery broker and cache data.
- R2 stores private media.

### Deployment rollback

1. Stop accepting new operational work if data integrity is at risk.
2. Identify the failing commit in Render or Vercel.
3. Roll back the application image or redeploy the previous known-good commit.
4. Do not roll back migrations blindly.
5. Check whether a forward migration is required.
6. Confirm `/api/health/`.
7. Test one authenticated staff request and one public request.

## Free-tier limitations

- Render services may sleep or restart.
- A continuously running Celery worker may not be available on a free plan.
- Supabase connection limits and pooler behavior must be monitored.
- Redis free tiers may have memory and eviction limits.
- Free-tier backups may be limited or absent.
- Do not use free-tier infrastructure as the final repository for sensitive institutional records without a reviewed backup and retention plan.
