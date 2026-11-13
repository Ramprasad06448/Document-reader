import React from 'react';

const features = [
  {
    title: 'Multi-Format Ingestion',
    desc: 'Upload native digital PDFs, scanned documents, PNG/JPG images, and plain text files with automated format detection.',
    icon: '📄',
    phase: 'Phase 1',
  },
  {
    title: 'Tesseract OCR Pipeline',
    desc: 'High-precision optical character recognition extracts readable text from scanned forms, receipts, and images.',
    icon: '🔍',
    phase: 'Phase 1',
  },
  {
    title: 'Gemini AI Simplification',
    desc: 'Transforms complex legal, medical, and technical jargon into plain, accessible language while preserving exact meaning.',
    icon: '✨',
    phase: 'Phase 2',
  },
  {
    title: 'Dual-Pane Comparison',
    desc: 'Side-by-side synchronized comparison highlights corresponding sections between original and simplified text.',
    icon: '⚖️',
    phase: 'Phase 2',
  },
  {
    title: 'Terminology Glossary',
    desc: 'Automatically extracts dense domain terms and builds an interactive glossary explaining what they mean.',
    icon: '📚',
    phase: 'Phase 2',
  },
  {
    title: 'One-Click Export',
    desc: 'Copy simplified text and executive summaries directly to your clipboard or download for offline review.',
    icon: '📋',
    phase: 'Phase 2',
  },
];

export default function FeaturesOverview() {
  return (
    <section className="features-section">
      <div className="section-header">
        <h2 className="section-title">Designed for Clarity & Comprehension</h2>
        <p className="section-desc">
          DocuEase bridges the comprehension gap for contracts, academic papers, medical records, and official filings.
        </p>
      </div>

      <div className="features-grid">
        {features.map((feature, idx) => (
          <div key={idx} className="feature-card">
            <div className="feature-top">
              <span className="feature-icon">{feature.icon}</span>
              <span className="feature-phase-tag">{feature.phase}</span>
            </div>
            <h3 className="feature-title">{feature.title}</h3>
            <p className="feature-text">{feature.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
