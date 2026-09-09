"use client";

import { FormEvent, useEffect, useState } from "react";
import { getPublicOrganizations, PublicOrganization, submitLostReport } from "@/lib/api";

export default function ReportLostPage() {
  const [organizations, setOrganizations] = useState<PublicOrganization[]>([]);
  const [organizationId, setOrganizationId] = useState("");
  const [submittedReference, setSubmittedReference] = useState("");
  const [error, setError] = useState("");
  useEffect(() => { getPublicOrganizations().then(setOrganizations).catch(() => setError("Institutions are temporarily unavailable. Please try again shortly.")); }, []);
  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError("");
    const form = new FormData(event.currentTarget);
    try {
      const result = await submitLostReport({ organization: Number(organizationId), claimant_name: String(form.get("name")), claimant_phone: String(form.get("phone")), category: String(form.get("category")), description: String(form.get("description")), last_seen_location: String(form.get("location")) });
      setSubmittedReference(result.reference);
    } catch (submitError) { setError(submitError instanceof Error ? submitError.message : "We could not submit your report."); }
  }
  return <main className="form-shell"><a className="brand" href="/"><span className="brand-mark">+</span>foundry360</a><section className="public-form"><a className="back-link" href="/">← Back to Foundry360</a><p className="eyebrow">Public report</p><h1>Report something lost</h1><p className="muted">Choose the institution responsible for the place where you lost it.</p>{submittedReference ? <div className="confirmation"><span className="confirm-mark">✓</span><h2>Report received</h2><p>Your private case reference is <strong>{submittedReference}</strong>. Keep it to check updates.</p><a className="primary" href="/claim-status">Check case status</a></div> : <form onSubmit={handleSubmit}><div className="form-grid"><label>Institution<select name="organization" required value={organizationId} onChange={(event) => setOrganizationId(event.target.value)}><option value="">Choose an institution</option>{organizations.map((organization) => <option value={organization.id} key={organization.id}>{organization.name}</option>)}</select></label><label>Phone number<input name="phone" required type="tel" placeholder="07XX XXX XXX" /></label><label>What was lost?<select name="category"><option>Phone or electronics</option><option>Bag or wallet</option><option>Document or ID</option><option>Keys</option><option>Other</option></select></label><label>Last seen location<input name="location" required placeholder="Library, gate, residence..." /></label><label className="wide">Describe it<textarea name="description" required placeholder="Include details that can help the desk verify ownership." /></label></div>{error && <p className="api-notice">{error}</p>}<button className="primary" type="submit" disabled={!organizationId}>Submit lost report</button><p className="form-note">The institution will contact you through the phone number provided.</p></form>}</section></main>;
}
