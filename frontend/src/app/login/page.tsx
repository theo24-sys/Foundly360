"use client";

import { useState } from "react";

export default function LoginPage() {
  const [submitted, setSubmitted] = useState(false);
  return <main className="auth-shell"><a className="brand" href="/"><span className="brand-mark">+</span>foundry360</a><section className="auth-card"><p className="eyebrow">Institution access</p><h1>Welcome back</h1><p className="muted">Sign in to your institution workspace.</p><form onSubmit={(event) => { event.preventDefault(); setSubmitted(true); }}><label>Work email<input type="email" placeholder="you@institution.ac.ke" required /></label><label>Password<input type="password" placeholder="Your password" required /></label><div className="form-row"><label className="checkbox"><input type="checkbox" /> Remember me</label><a href="/login/reset">Forgot password?</a></div><button className="primary full-width" type="submit">Sign in to workspace</button></form>{submitted && <p className="form-success">Sign-in will connect to the staff authentication service once configured.</p>}<p className="auth-foot">Are you looking for an item? <a href="/claim-status">Check a public case</a></p></section></main>;
}