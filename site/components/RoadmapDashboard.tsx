import type { RoadmapSnapshot } from '@/lib/roadmap';

export function RoadmapDashboard({ data }: { data: RoadmapSnapshot }) {
  const { totals } = data;
  const pct = (n: number) => (totals.total ? Math.round((n / totals.total) * 1000) / 10 : 0);
  const sourceLabel =
    [data.source.repo, data.source.pr, data.source.commit].filter(Boolean).join(' · ');

  return (
    <section aria-labelledby="roadmap-heading">
      <span className="kicker">Roadmap snapshot</span>
      <h1 id="roadmap-heading">DNA Pipeline — Status</h1>
      <p>
        Audit refresh {data.capturedAt}. Source: {sourceLabel}.{' '}
        {data.source.doc ? (
          <>
            See <code>{data.source.doc}</code>.
          </>
        ) : null}
      </p>

      <div className="snapshot-stats">
        <div className="stat shipped">
          <div className="num">{pct(totals.shipped)}%</div>
          <div className="label">Shipped ({totals.shipped})</div>
        </div>
        <div className="stat wiring">
          <div className="num">{pct(totals.wiring)}%</div>
          <div className="label">Wiring incomplete ({totals.wiring})</div>
        </div>
        <div className="stat notstarted">
          <div className="num">{pct(totals.notstarted)}%</div>
          <div className="label">Not started ({totals.notstarted})</div>
        </div>
        <div className="stat total">
          <div className="num">{totals.total}</div>
          <div className="label">Total claims</div>
        </div>
      </div>

      <div className="legend">
        <span className="l-shipped">Shipped</span>
        <span className="l-wiring">Wiring incomplete</span>
        <span className="l-notstarted">Not started</span>
      </div>
      <div className="bar" aria-hidden>
        <span className="b-shipped" style={{ width: `${pct(totals.shipped)}%` }} />
        <span className="b-wiring" style={{ width: `${pct(totals.wiring)}%` }} />
        <span className="b-notstarted" style={{ width: `${pct(totals.notstarted)}%` }} />
      </div>

      {data.phases.length > 0 ? (
        <>
          <h2>Phases</h2>
          <div className="phase-list">
            {data.phases.map((p) => (
              <article key={p.id} className="phase">
                <div className="phase-head">
                  <span className="phase-title">{p.title}</span>
                  <span className={`badge ${p.status}`}>{labelFor(p.status)}</span>
                  {p.meta ? <span className="phase-meta">{p.meta}</span> : null}
                </div>
                {p.items.length ? (
                  <ul>
                    {p.items.map((item, i) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                ) : null}
              </article>
            ))}
          </div>
        </>
      ) : null}

      {data.topGaps.length > 0 ? (
        <>
          <h2>Top remaining wiring gaps</h2>
          <div className="gap-list card">
            <ol>
              {data.topGaps.map((g, i) => (
                <li key={i}>
                  <b>{g.title}</b>
                  {g.detail}
                </li>
              ))}
            </ol>
          </div>
        </>
      ) : null}
    </section>
  );
}

function labelFor(status: string) {
  switch (status) {
    case 'shipped':
      return 'Shipped';
    case 'wiring':
      return 'Wiring';
    case 'notstarted':
      return 'Not started';
    case 'inprog':
      return 'In progress';
    default:
      return status;
  }
}
