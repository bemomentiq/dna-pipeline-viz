import Link from 'next/link';

export default function Page() {
  return (
    <>
      <div className="subnav">
        <Link href="/architecture/">← Architecture</Link>
      </div>
      <span className="kicker">Architecture</span>
      <h1>API surface</h1>
      <p>All `/api/v1/dna/*` endpoints.</p>
      <div className="empty">
        Drilldown content lands here. The fleet is filling this in from the legacy walkthrough.
      </div>
    </>
  );
}
