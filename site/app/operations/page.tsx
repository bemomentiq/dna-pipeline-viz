import { SectionGrid } from '@/components/SectionGrid';
import { findLayer } from '@/lib/ia';

export default function OperationsIndexPage() {
  const layer = findLayer('operations')!;
  return (
    <>
      <span className="kicker">Layer</span>
      <h1>{layer.title}</h1>
      <p>{layer.blurb}</p>
      <SectionGrid items={layer.sections} />
    </>
  );
}
