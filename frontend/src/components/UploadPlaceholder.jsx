import React, { useState } from 'react';

export default function UploadPlaceholder() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0]);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
  };

  return (
    <section className="upload-section">
      <div className="upload-card">
        <div
          className={`dropzone ${isDragging ? 'dragging' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="dropzone-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="17 8 12 3 7 8" />
              <line x1="12" y1="3" x2="12" y2="15" />
            </svg>
          </div>

          <h3 className="dropzone-title">Upload your complex document</h3>
          <p className="dropzone-subtitle">
            Drag and drop your file here, or click to browse
          </p>

          <label className="browse-button" htmlFor="file-input">
            Select Document
            <input
              id="file-input"
              type="file"
              accept=".pdf,.txt,.png,.jpg,.jpeg"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
          </label>

          <div className="supported-formats">
            <span className="format-tag">.PDF</span>
            <span className="format-tag">.TXT</span>
            <span className="format-tag">.PNG</span>
            <span className="format-tag">.JPG</span>
            <span className="format-note">Max 10 MB</span>
          </div>
        </div>

        {selectedFile && (
          <div className="file-preview-card">
            <div className="file-meta">
              <div className="file-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                </svg>
              </div>
              <div className="file-details">
                <span className="file-name">{selectedFile.name}</span>
                <span className="file-size">
                  {(selectedFile.size / 1024).toFixed(1)} KB • Ready for extraction
                </span>
              </div>
            </div>
            <div className="file-actions">
              <span className="phase-pill">Phase 0 Preview</span>
              <button onClick={handleClear} className="remove-btn" title="Remove file">
                ✕
              </button>
            </div>
          </div>
        )}

        <div className="upload-note">
          <p>
            ℹ️ <strong>Phase 0 Foundation Active:</strong> Text extraction (PyMuPDF & Tesseract OCR)
            will be activated in Phase 1, followed by Gemini AI simplification in Phase 2.
          </p>
        </div>
      </div>
    </section>
  );
}
