import Link from 'next/link';

export default function Page() {
  return (
    <>
      <div className="subnav">
        <Link href="/overview/">← Overview</Link>
      </div>
      <span className="kicker">Overview</span>
      <h1>Phase walkthrough</h1>
      <p>What actually happens at each node.</p>
      <div className="empty">
        Drilldown content lands here. The fleet is filling this in from the legacy walkthrough.
      </div>
    </>
  );
}
