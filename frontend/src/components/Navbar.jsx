import React from 'react';

export default function Navbar({ backendStatus }) {
  return (
    <header className="navbar">
      <div className="container nav-container">
        <div className="brand">
          <div className="logo-badge">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
              <polyline points="14 2 14 8 20 8" />
              <path d="m9 15 2 2 4-4" />
            </svg>
          </div>
          <div className="brand-text">
            <h1 className="brand-name">DocuEase</h1>
            <span className="brand-tagline">AI Document Simplification</span>
          </div>
        </div>

        <div className="nav-actions">
          <div className={`status-pill ${backendStatus.state}`}>
            <span className="status-dot"></span>
            <span className="status-text">
              {backendStatus.state === 'connected' && 'Backend Connected'}
              {backendStatus.state === 'loading' && 'Checking Backend...'}
              {backendStatus.state === 'disconnected' && 'Backend Offline'}
            </span>
          </div>
          <a
            href="https://github.com/tesseract-ocr/tesseract"
            target="_blank"
            rel="noreferrer"
            className="nav-link"
          >
            Tesseract OCR
          </a>
        </div>
      </div>
    </header>
  );
}
