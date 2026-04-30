import type { Metadata } from 'next';
import Link from 'next/link';
import './globals.css';

export const metadata: Metadata = {
  title: 'DNA Pipeline · MomentIQ',
  description:
    'Kalodata → AI Content Platform training pipeline — closed-loop, category-aware, bandit-driven.',
};

const NAV: { href: string; label: string }[] = [
  { href: '/', label: 'Home' },
  { href: '/overview/', label: 'Overview' },
  { href: '/architecture/', label: 'Architecture' },
  { href: '/bandits/', label: 'Bandits & Reward' },
  { href: '/quality/', label: 'Quality & Gates' },
  { href: '/operations/', label: 'Operations' },
  { href: '/reference/', label: 'Reference' },
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="topbar">
          <div className="topbar-inner">
            <Link href="/" className="brand" aria-label="Home">
              <span className="brand-mark" aria-hidden>◆</span>
              <span>DNA Pipeline</span>
              <span className="brand-org">MomentIQ</span>
            </Link>
            <nav className="primary-nav">
              {NAV.map((item) => (
                <Link key={item.href} href={item.href}>
                  {item.label}
                </Link>
              ))}
            </nav>
          </div>
        </header>
        <main className="page">{children}</main>
        <footer className="site-footer">
          <div className="site-footer-inner">
            <span>MomentIQ · DNA Pipeline</span>
            <span>
              Source ·{' '}
              <a
                href="https://github.com/bemomentiq/dna-pipeline-site"
                target="_blank"
                rel="noreferrer"
              >
                bemomentiq/dna-pipeline-site
              </a>
            </span>
          </div>
        </footer>
      </body>
    </html>
  );
}
