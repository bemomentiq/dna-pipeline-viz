import Link from 'next/link';

export default function Page() {
  return (
    <>
      <div className="subnav">
        <Link href="/architecture/">← Architecture</Link>
      </div>
      <span className="kicker">Architecture</span>
      <h1>Schema</h1>
      <p>Net-new database surface in Neon.</p>
      <div className="empty">
        Drilldown content lands here. The fleet is filling this in from the legacy walkthrough.
      </div>
    </>
  );
}
