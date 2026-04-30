import Link from 'next/link';

export default function Page() {
  return (
    <>
      <div className="subnav">
        <Link href="/reference/">← Reference</Link>
      </div>
      <span className="kicker">Reference</span>
      <h1>Glossary</h1>
      <p>Every term you\</p>
      <div className="empty">
        Drilldown content lands here. The fleet is filling this in from the legacy walkthrough.
      </div>
    </>
  );
}
