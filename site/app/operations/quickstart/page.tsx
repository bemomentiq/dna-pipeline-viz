import Link from 'next/link';

export default function Page() {
  return (
    <>
      <div className="subnav">
        <Link href="/operations/">← Operations</Link>
      </div>
      <span className="kicker">Operations</span>
      <h1>Quickstart</h1>
      <p>If something breaks — this card first.</p>
      <div className="empty">
        Drilldown content lands here. The fleet is filling this in from the legacy walkthrough.
      </div>
    </>
  );
}
