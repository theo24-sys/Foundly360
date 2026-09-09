"use client";

import { FormEvent, useEffect, useState } from "react";
import { getPublicOrganizations, PublicOrganization, submitFoundItem } from "@/lib/api";

export default function ReportFoundPage() {
  const [organizations, setOrganizations] = useState<PublicOrganization[]>([]);
  const [organizationId, setOrganizationId] = useState("");
  const [submittedReference, setSubmittedReference] = useState("");
  const [error, setError] = useState("");
  const receivingPoints = organizations.find((organization) => String(organization.id) === organizationId)?.receiving_points ?? [];
  useEffect(() => { getPublicOrganizations().then(setOrganizations).catch(() => setError("Institutions are temporarily unavailable. Please try again shortly.")); }, []);
  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError("");
    const form = new FormData(event.currentTarget);
    try {
      const result = await submitFoundItem({ organization: Number(organizationId), location: Number(form.get("location")), category: String(form.get("category")), title: String(form.get("title")), private_description: String(form.get("description")) });
      setSubmittedReference(result.reference);
    } catch (submitError) { setError(submitError instanceof Error ? submitError.message : "We could not submit the found item."); }
  }
  return <main className="form-shell"><a className="brand" href="/"><span className="brand-mark">+</span>foundry360</a><section className="public-form"><a className="back-link" href="/">← Back to Foundry360</a><p className="eyebrow">Community handover</p><h1>Report something found</h1><p className="muted">Choose the institution and receiving point where staff can secure the item.</p>{submittedReference ? <div className="confirmation"><span className="confirm-mark">✓</span><h2>Item sent to the desk</h2><p>Reference <strong>{submittedReference}</strong> was created. Please take the item to the selected receiving point.</p><a className="secondary" href="/">Return home</a></div> : <form onSubmit={handleSubmit}><div className="form-grid"><label>Institution<select required value={organizationId} onChange={(event) => setOrganizationId(event.target.value)}><option value="">Choose an institution</option>{organizations.map((organization) => <option value={organization.id} key={organization.id}>{organization.name}</option>)}</select></label><label>Receiving point<select name="location" required disabled={!organizationId}><option value="">Choose a desk</option>{receivingPoints.map((point) => <option value={point.id} key={point.id}>{point.name} · {point.opening_hours}</option>)}</select></label><label>Item title<input name="title" required placeholder="Black backpack" /></label><label>Item category<select name="category"><option>Phone or electronics</option><option>Bag or wallet</option><option>Document or ID</option><option>Keys</option><option>Other</option></select></label><label className="wide">Safe description<textarea name="description" required placeholder="Describe what you found without private owner details." /></label></div>{error && <p className="api-notice">{error}</p>}<button className="primary" type="submit" disabled={!organizationId || receivingPoints.length === 0}>Send to receiving point</button></form>}</section></main>;
}
