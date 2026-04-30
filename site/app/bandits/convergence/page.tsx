import Link from 'next/link';

export default function Page() {
  return (
    <>
      <div className="subnav">
        <Link href="/bandits/">← Bandits</Link>
      </div>
      <span className="kicker">Bandits</span>
      <h1>Convergence loop</h1>
      <p>Closed loop that converges on indistinguishability.</p>
      <div className="empty">
        Drilldown content lands here. The fleet is filling this in from the legacy walkthrough.
      </div>
    </>
  );
}
