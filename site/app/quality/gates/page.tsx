import Link from 'next/link';

export default function Page() {
  return (
    <>
      <div className="subnav">
        <Link href="/quality/">← Quality</Link>
      </div>
      <span className="kicker">Quality</span>
      <h1>Gates</h1>
      <p>Nothing ships without clearing every gate.</p>
      <div className="empty">
        Drilldown content lands here. The fleet is filling this in from the legacy walkthrough.
      </div>
    </>
  );
}
