import Link from 'next/link';

export default function Page() {
  return (
    <>
      <div className="subnav">
        <Link href="/reference/">← Reference</Link>
      </div>
      <span className="kicker">Reference</span>
      <h1>SOTA gap</h1>
      <p>27-capability delta vs 2024–2026 state-of-the-art.</p>
      <div className="empty">
        Drilldown content lands here. The fleet is filling this in from the legacy walkthrough.
      </div>
    </>
  );
}
