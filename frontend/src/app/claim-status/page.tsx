"use client";

import { useState } from "react";

export default function ClaimStatusPage() {
  const [checked, setChecked] = useState(false);
  return <main className="form-shell"><a className="brand" href="/"><span className="brand-mark">+</span>foundry360</a><section className="public-form narrow"><a className="back-link" href="/">← Back to Foundry360</a><p className="eyebrow">Private case access</p><h1>Check your case</h1><p className="muted">Enter the reference from your SMS or WhatsApp update. We never publish item details publicly.</p>{checked ? <div className="status-result"><span className="status-dot"/><div><small>LR-2026-1049</small><h2>Report under review</h2><p>Security staff are checking new found items at Strathmore University.</p></div><a className="secondary" href="/">Done</a></div> : <form onSubmit={(event) => { event.preventDefault(); setChecked(true); }}><label>Case reference<input required placeholder="LR-2026-1049" /></label><label>Phone number<input required type="tel" placeholder="07XX XXX XXX" /></label><button className="primary full-width" type="submit">Send me a secure code</button></form>}</section></main>;
}