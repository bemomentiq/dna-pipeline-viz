import Link from 'next/link';

export default function Page() {
  return (
    <>
      <div className="subnav">
        <Link href="/quality/">← Quality</Link>
      </div>
      <span className="kicker">Quality</span>
      <h1>Rollout</h1>
      <p>From 0% canary to steady-state — the 5 promotion ramps.</p>
      <div className="empty">
        Drilldown content lands here. The fleet is filling this in from the legacy walkthrough.
      </div>
    </>
  );
}
