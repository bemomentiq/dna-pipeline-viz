import Link from 'next/link';

export default function Page() {
  return (
    <>
      <div className="subnav">
        <Link href="/operations/">← Operations</Link>
      </div>
      <span className="kicker">Operations</span>
      <h1>Failure modes</h1>
      <p>What breaks, how it surfaces, who fixes it.</p>
      <div className="empty">
        Drilldown content lands here. The fleet is filling this in from the legacy walkthrough.
      </div>
    </>
  );
}
