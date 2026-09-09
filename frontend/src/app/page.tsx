const journeys = [
  ["I lost something", "Report an item and receive a private reference number.", "/report-lost", "Start a lost report"],
  ["I found something", "Tell the institution what you found so it can be secured.", "/report-found", "Report a found item"],
  ["Check my case", "Use your reference and phone number to see the latest update.", "/claim-status", "Check case status"],
];

const capabilities = [
  ["01", "One trusted desk", "The institution stays responsible for the physical item while every handover is recorded digitally."],
  ["02", "Private by default", "Public reports never expose identifying details. Staff verify ownership using hidden evidence."],
  ["03", "From found to returned", "Track intake, storage, matching, approval, collection, transfers and disposal in one place."],
];

const guides = [
  ["For people", "How to report a lost item", "The information to include, what happens next, and how to follow your case.", "/report-lost"],
  ["For finders", "Safely hand over found property", "Give an item to the right desk without publishing someone else’s private details.", "/report-found"],
  ["For institutions", "Set up a property desk", "A practical starting guide for security, registry, reception and campus teams.", "/login"],
];

export default function Home() {
  return (
    <main className="public-shell">
      <nav className="public-nav"><a className="brand" href="/"><span className="brand-mark">+</span>foundry360</a><div><a href="#how-it-works">How it works</a><a href="#guides">Guides</a><a href="/claim-status">Check a case</a><a className="nav-login" href="/login">Staff login</a></div></nav>
      <section className="public-hero landing-hero"><div><p className="eyebrow">Lost property, handled properly</p><h1>Less searching. More returning.</h1><p className="hero-copy">Foundry360 gives Kenyan institutions a secure way to manage lost property from the moment it is found to the moment it reaches its owner.</p><div className="hero-actions"><a className="primary" href="/report-lost">Report something lost</a><a className="secondary" href="/login">For institutions <span>→</span></a></div><div className="hero-proof"><span className="signal-dot"/><span>Built for campuses, hotels, hospitals and public venues</span></div></div><div className="hero-signal"><div className="signal-top"><span className="signal-dot"/><small>RECOVERY WORKFLOW</small></div><strong>Found → verified → returned</strong><p>One clear trail for every item, every decision and every handover.</p><div className="signal-steps"><span><b>01</b> Registered</span><span><b>02</b> Matched</span><span><b>03</b> Collected</span></div><small className="signal-caption">Private item details stay with authorized staff.</small></div></section>
      <section className="trust-strip"><span>Designed for real institutional desks</span><b>Universities</b><b>Hotels</b><b>Hospitals</b><b>Malls</b><b>Schools</b><b>Transport hubs</b></section>
      <section className="journeys landing-section"><p className="eyebrow">Start here</p><h2>A simpler next step</h2><p className="section-lede">Whether you lost an item, found one, or run the desk that keeps property safe, there is a clear path forward.</p><div className="journey-grid">{journeys.map(([title, copy, href, action], index) => <a className="journey-card" href={href} key={title}><span className="journey-number">0{index + 1}</span><h3>{title}</h3><p>{copy}</p><b>{action} →</b></a>)}</div></section>
      <section className="how-section" id="how-it-works"><div className="section-intro"><p className="eyebrow">How it works</p><h2>A chain of custody people can trust.</h2><p className="section-lede">Good lost-property management is not a marketplace. It is a calm, accountable process owned by the institution.</p></div><div className="capability-list">{capabilities.map(([number, title, copy]) => <article className="capability" key={number}><span>{number}</span><div><h3>{title}</h3><p>{copy}</p></div></article>)}</div></section>
      <section className="institution-section"><div className="institution-copy"><p className="eyebrow">For institutions</p><h2>Turn a manual logbook into a recovery operation.</h2><p className="section-lede">Give security and registry teams the tools to intake quickly, match carefully and prove what happened to every item.</p><a className="primary" href="/login">Explore the staff workspace <span>→</span></a></div><div className="institution-panel"><div className="institution-panel-head"><span className="mini-label">TODAY AT THE DESK</span><span className="live-pill"><i/>Live</span></div><div className="desk-stat"><strong>72%</strong><span>recovery rate</span></div><div className="desk-row"><span>Possible matches</span><b>07 <em>review</em></b></div><div className="desk-row"><span>Items awaiting collection</span><b>04 <em>today</em></b></div><div className="desk-row"><span>Custody events recorded</span><b>128 <em>this month</em></b></div></div></section>
      <section className="privacy-section"><div className="privacy-mark">◉</div><div><p className="eyebrow">Privacy and trust</p><h2>Reveal only what helps prove ownership.</h2><p className="section-lede">Photos and sensitive details stay private. Claimants use a phone number and case reference, while staff use hidden identifying evidence before approving a return.</p></div><a className="text-arrow" href="/claim-status">See how case access works →</a></section>
      <section className="guides-section landing-section" id="guides"><p className="eyebrow">Guides</p><h2>Useful from the first day.</h2><p className="section-lede">Short, practical guidance for the people who report, find and manage lost property.</p><div className="guide-grid">{guides.map(([audience, title, copy, href]) => <a className="guide-card" href={href} key={title}><span>{audience}</span><h3>{title}</h3><p>{copy}</p><b>Read guide <i>↗</i></b></a>)}</div></section>
      <section className="final-cta"><p className="eyebrow">Ready when you are</p><h2>Make the next lost item easier to return.</h2><p>Start with a report, or bring a better property desk to your institution.</p><div className="hero-actions"><a className="primary" href="/report-lost">Report a lost item</a><a className="secondary" href="/login">Talk to the desk team</a></div></section>
      <footer className="public-footer"><span><span className="brand-mark small-mark">+</span> Foundry360</span><span>Kenya · Privacy-first by design</span><span><a href="/claim-status">Check a case</a> · <a href="/login">Staff login</a></span></footer>
    </main>
  );
}
