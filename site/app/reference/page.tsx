import { SectionGrid } from '@/components/SectionGrid';
import { findLayer } from '@/lib/ia';

export default function ReferenceIndexPage() {
  const layer = findLayer('reference')!;
  return (
    <>
      <span className="kicker">Layer</span>
      <h1>{layer.title}</h1>
      <p>{layer.blurb}</p>
      <SectionGrid items={layer.sections} />
    </>
  );
}
