import { RoadmapDashboard } from '@/components/RoadmapDashboard';
import { SectionGrid } from '@/components/SectionGrid';
import { LAYERS } from '@/lib/ia';
import { loadRoadmap } from '@/lib/roadmap';

export default function HomePage() {
  const roadmap = loadRoadmap();
  return (
    <>
      <RoadmapDashboard data={roadmap} />

      <h2 style={{ marginTop: 48 }}>Explore the engine</h2>
      <p>Seven layers, drill all the way down. Pulled from the original 33-section walkthrough.</p>
      <SectionGrid
        items={LAYERS.map((l) => ({
          href: `/${l.slug}/`,
          title: l.title,
          blurb: l.blurb,
        }))}
      />
    </>
  );
}
