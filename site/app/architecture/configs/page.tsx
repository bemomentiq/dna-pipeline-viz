import Link from 'next/link';

export default function Page() {
  return (
    <>
      <div className="subnav">
        <Link href="/architecture/">← Architecture</Link>
      </div>
      <span className="kicker">Architecture</span>
      <h1>Configs</h1>
      <p>Every DNA knob, by content surface.</p>
      <div className="empty">
        Drilldown content lands here. The fleet is filling this in from the legacy walkthrough.
      </div>
    </>
  );
}
