import Link from 'next/link';

export default function Page() {
  return (
    <>
      <div className="subnav">
        <Link href="/reference/">← Reference</Link>
      </div>
      <span className="kicker">Reference</span>
      <h1>Build plan</h1>
      <p>Sprint-by-sprint plan to feature-complete.</p>
      <div className="empty">
        Drilldown content lands here. The fleet is filling this in from the legacy walkthrough.
      </div>
    </>
  );
}
