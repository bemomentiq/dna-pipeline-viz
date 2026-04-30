import Link from 'next/link';

export default function Page() {
  return (
    <>
      <div className="subnav">
        <Link href="/overview/">← Overview</Link>
      </div>
      <span className="kicker">Overview</span>
      <h1>Pipeline hub</h1>
      <p>Where to start. Top-level navigation across the engine.</p>
      <div className="empty">
        Drilldown content lands here. The fleet is filling this in from the legacy walkthrough.
      </div>
    </>
  );
}
