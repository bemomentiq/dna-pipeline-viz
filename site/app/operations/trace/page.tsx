import Link from 'next/link';

export default function Page() {
  return (
    <>
      <div className="subnav">
        <Link href="/operations/">← Operations</Link>
      </div>
      <span className="kicker">Operations</span>
      <h1>Trace</h1>
      <p>Every primary attribute, end-to-end.</p>
      <div className="empty">
        Drilldown content lands here. The fleet is filling this in from the legacy walkthrough.
      </div>
    </>
  );
}
