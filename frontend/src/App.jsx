import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import DocumentProcessor from './components/DocumentProcessor';
import FeaturesOverview from './components/FeaturesOverview';
import { checkHealth } from './services/api';

export default function App() {
  const [backendStatus, setBackendStatus] = useState({
    state: 'loading', // 'connected' | 'disconnected' | 'loading'
    message: 'Connecting to backend...',
  });

  useEffect(() => {
    const verifyBackend = async () => {
      try {
        const data = await checkHealth();
        if (data.status === 'success') {
          setBackendStatus({
            state: 'connected',
            message: data.message || 'DocuEase backend is running',
          });
        } else {
          setBackendStatus({
            state: 'disconnected',
            message: 'Unexpected backend response',
          });
        }
      } catch (err) {
        setBackendStatus({
          state: 'disconnected',
          message: 'Unable to reach backend API',
        });
      }
    };

    verifyBackend();
    const interval = setInterval(verifyBackend, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app-container">
      <Navbar backendStatus={backendStatus} />

      <main className="main-content">
        {/* Hero Section */}
        <section className="hero-section">
          <div className="container hero-container">
            <div className="badge-pill">
              <span className="badge-sparkle">✦</span>
              <span>AI-Powered Document Simplification</span>
            </div>

            <h1 className="hero-title">
              Make Any Complex Document <br />
              <span className="gradient-text">Instantly Understandable</span>
            </h1>

            <p className="hero-subtitle">
              DocuEase translates dense contracts, medical charts, financial statements, and technical research
              into plain, accessible language without losing critical meaning or legal nuances.
            </p>

            <div className="hero-stats">
              <div className="stat-item">
                <span className="stat-number">4+</span>
                <span className="stat-label">Formats Supported</span>
              </div>
              <div className="stat-divider"></div>
              <div className="stat-item">
                <span className="stat-number">Tesseract</span>
                <span className="stat-label">Integrated OCR</span>
              </div>
              <div className="stat-divider"></div>
              <div className="stat-item">
                <span className="stat-number">Gemini AI</span>
                <span className="stat-label">Plain-Language Engine</span>
              </div>
            </div>
          </div>
        </section>

        {/* Document Ingestion & Extraction */}
        <div className="container">
          <DocumentProcessor />
        </div>

        {/* Platform Capabilities */}
        <div className="container">
          <FeaturesOverview />
        </div>
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="container footer-container">
          <div className="footer-left">
            <span className="footer-brand">DocuEase</span>
            <span className="footer-copy">© 2026 DocuEase. Built with React, Flask & Tesseract OCR.</span>
          </div>
          <div className="footer-right">
            <span className="footer-phase">Phase 2: AI Simplification & Dual-Pane Viewer Active</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
