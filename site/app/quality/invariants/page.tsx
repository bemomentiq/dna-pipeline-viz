import Link from 'next/link';

export default function Page() {
  return (
    <>
      <div className="subnav">
        <Link href="/quality/">← Quality</Link>
      </div>
      <span className="kicker">Quality</span>
      <h1>Invariants</h1>
      <p>Non-negotiable rules the pipeline enforces.</p>
      <div className="empty">
        Drilldown content lands here. The fleet is filling this in from the legacy walkthrough.
      </div>
    </>
  );
}
