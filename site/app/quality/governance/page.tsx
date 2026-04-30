import Link from 'next/link';

export default function Page() {
  return (
    <>
      <div className="subnav">
        <Link href="/quality/">← Quality</Link>
      </div>
      <span className="kicker">Quality</span>
      <h1>Governance</h1>
      <p>Roles, on-call, change control.</p>
      <div className="empty">
        Drilldown content lands here. The fleet is filling this in from the legacy walkthrough.
      </div>
    </>
  );
}
