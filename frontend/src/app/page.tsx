"use client";

import { useEffect, useState } from "react";
import { getDashboardMetrics, type DashboardMetrics } from "@/lib/api";

const cases = [
  ["Black leather wallet", "#LP-1048", "Possible match", "Student Centre"],
  ["iPhone 13 · Midnight", "#LP-1047", "Claim pending", "Library Block"],
  ["Blue Nike backpack", "#LP-1046", "Stored", "Gate 2"],
  ["Keys with red tag", "#LP-1045", "Returned", "Main Reception"],
];

export default function Home() {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [apiError, setApiError] = useState(false);

  useEffect(() => {
    const controller = new AbortController();
    getDashboardMetrics(1, controller.signal).then(setMetrics).catch((error: unknown) => {
      if (error instanceof DOMException && error.name === "AbortError") return;
      setApiError(true);
    });
    return () => controller.abort();
  }, []);

  const metricCards = [
    ["Open cases", metrics?.open_cases ?? "—", "Live API metric"],
    ["Possible matches", metrics?.possible_matches ?? "—", "Live API metric"],
    ["Pending claims", metrics?.pending_claims ?? "—", "Live API metric"],
    ["Recovery rate", metrics ? `${metrics.recovery_rate}%` : "—", "Live API metric"],
  ];

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><span className="brand-mark">+</span>foundry360</div>
        <div className="tenant"><span className="tenant-mark">S</span><span><b>Strathmore University</b><small>Security &amp; Registry</small></span><span>⌄</span></div>
        <p className="nav-label">Workspace</p>
        {['Overview', 'All cases 24', 'Matches 7', 'Claims 4'].map((item, index) => <button className={`nav-item ${index === 0 ? 'active' : ''}`} key={item}>{item}</button>)}
        <p className="nav-label">Manage</p>
        {['Locations', 'Team', 'Reports'].map((item) => <button className="nav-item" key={item}>{item}</button>)}
        <div className="sidebar-foot"><button className="nav-item">Settings</button><div className="user"><span>AM</span><b>Angela Mwangi<small>Administrator</small></b></div></div>
      </aside>
      <main className="main-content">
        <header className="topbar"><span>Workspace / <b>Overview</b></span><span>Tuesday, 08 September 2026 · Nairobi, KE</span></header>
        <div className="page-wrap">
          <section className="heading"><div><p className="eyebrow">Operations centre</p><h1>Good morning, Angela</h1><p className="muted">Here is what is happening across your lost-property desk.</p></div><button className="primary">＋ Register found item</button></section>
          {apiError && <div className="api-notice" role="status">Dashboard data is unavailable. Start the API or check your staff session.</div>}
          <section className="metrics">{metricCards.map(([label, value, note]) => <article className="metric" key={label}><span>{label}</span><strong>{value}</strong><small>{note}</small></article>)}</section>
          <section className="work-grid"><article className="panel cases"><div className="panel-head"><div><h2>Recent activity</h2><p className="muted">New items, matches and claims.</p></div><button className="link">View all cases →</button></div><div className="table-head"><span>Case</span><span>Status</span><span>Location</span></div>{cases.map(([item, reference, status, location]) => <div className="case-row" key={reference}><div><b>{item}</b><small>{reference}</small></div><span className={`status ${status.toLowerCase().replace(' ', '-')}`}>{status}</span><span>{location}</span></div>)}</article>
            <aside className="panel attention"><h2>Needs your attention</h2><p className="muted">4 items waiting for a decision</p><button className="attention-item"><b>Claim #CL-1042</b><small>iPhone 13 · submitted 18m ago</small><span>›</span></button><button className="attention-item"><b>Match suggestion</b><small>Black backpack · 86% match</small><span>›</span></button><button className="attention-item"><b>Collection due today</b><small>Samsung A54 · #LP-0931</small><span>›</span></button><button className="outline">Open attention queue</button></aside>
          </section>
          <section className="operations"><div className="panel-head"><div><p className="eyebrow">High-volume tools</p><h2>Keep the desk moving</h2></div><span className="badge">ODPC ready</span></div><div className="ops-grid"><article><span className="ops-icon">＋</span><h3>Event intake mode</h3><p>Log one item every 5 seconds after large campus events.</p><button className="link">Start rapid intake →</button></article><article><span className="ops-icon">⌗</span><h3>Storage &amp; QR bins</h3><p>Scan a box tag to see its complete custody contents.</p><button className="link">Manage bin tags →</button></article><article><span className="ops-icon">⌛</span><h3>Disposal watch</h3><p>Prepare notices and preserve an audit trail for unclaimed property.</p><button className="link">Review queue →</button></article></div></section>
        </div>
      </main>
    </div>
  );
}
