import Link from 'next/link';

export type SectionLink = {
  href: string;
  title: string;
  blurb: string;
  status?: 'shipped' | 'wiring' | 'notstarted';
};

export function SectionGrid({ items }: { items: SectionLink[] }) {
  return (
    <div className="section-grid">
      {items.map((s) => (
        <Link key={s.href} href={s.href} className="section-card">
          <h3>
            {s.title}
            {s.status ? <span className={`badge ${s.status}`} style={{ marginLeft: 8 }}>{s.status}</span> : null}
          </h3>
          <p>{s.blurb}</p>
        </Link>
      ))}
    </div>
  );
}
