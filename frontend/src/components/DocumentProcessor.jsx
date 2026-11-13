import React, { useState } from 'react';
import { extractDocument } from '../services/api';

const ALLOWED_EXTENSIONS = ['pdf', 'txt', 'png', 'jpg', 'jpeg'];
const MAX_SIZE_MB = 10;

export default function DocumentProcessor() {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [copied, setCopied] = useState(false);

  const validateFile = (selectedFile) => {
    if (!selectedFile) return false;

    const ext = selectedFile.name.split('.').pop().toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(ext)) {
      setError(`Unsupported file type (.${ext}). Supported formats: ${ALLOWED_EXTENSIONS.map(e => '.' + e).join(', ')}`);
      return false;
    }

    if (selectedFile.size > MAX_SIZE_MB * 1024 * 1024) {
      setError(`File size (${(selectedFile.size / (1024 * 1024)).toFixed(1)} MB) exceeds the ${MAX_SIZE_MB} MB limit.`);
      return false;
    }

    setError(null);
    return true;
  };

  const handleFileChange = (e) => {
    const selected = e.target.files && e.target.files[0];
    if (selected && validateFile(selected)) {
      setFile(selected);
      setResult(null);
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
    const dropped = e.dataTransfer.files && e.dataTransfer.files[0];
    if (dropped && validateFile(dropped)) {
      setFile(dropped);
      setResult(null);
    }
  };

  const handleExtract = async () => {
    if (!file) return;

    setIsProcessing(true);
    setError(null);

    try {
      const data = await extractDocument(file);
      if (data.status === 'success') {
        setResult(data);
      } else {
        setError(data.message || 'Failed to extract document.');
      }
    } catch (err) {
      const msg = err.response?.data?.message || err.message || 'Network error occurred while communicating with the server.';
      setError(`Extraction failed: ${msg}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleCopy = () => {
    if (!result?.extracted_text) return;
    navigator.clipboard.writeText(result.extracted_text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  const handleReset = () => {
    setFile(null);
    setResult(null);
    setError(null);
  };

  const getMethodBadge = (method) => {
    switch (method) {
      case 'ocr_image':
        return { label: 'Tesseract OCR', color: 'badge-ocr' };
      case 'digital_pdf':
        return { label: 'PyMuPDF Digital', color: 'badge-digital' };
      case 'hybrid_pdf_ocr':
        return { label: 'Hybrid PyMuPDF + OCR', color: 'badge-hybrid' };
      case 'plain_text':
        return { label: 'Plain Text Stream', color: 'badge-plain' };
      default:
        return { label: method || 'Standard', color: 'badge-plain' };
    }
  };

  return (
    <section className="processor-section">
      {error && (
        <div className="alert-banner alert-error">
          <span className="alert-icon">⚠️</span>
          <span className="alert-text">{error}</span>
          <button className="alert-close" onClick={() => setError(null)}>✕</button>
        </div>
      )}

      {!result ? (
        <div className="upload-card">
          <div
            className={`dropzone ${isDragging ? 'dragging' : ''} ${isProcessing ? 'disabled' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <div className="dropzone-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="17 8 12 3 7 8" />
                <line x1="12" y1="3" x2="12" y2="15" />
              </svg>
            </div>

            <h3 className="dropzone-title">Upload Document for Text Extraction</h3>
            <p className="dropzone-subtitle">
              Drag and drop your file here, or browse from your device
            </p>

            <label className="browse-button" htmlFor="doc-input">
              Choose Document
              <input
                id="doc-input"
                type="file"
                accept=".pdf,.txt,.png,.jpg,.jpeg"
                onChange={handleFileChange}
                disabled={isProcessing}
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

          {file && (
            <div className="file-preview-card">
              <div className="file-meta">
                <div className="file-icon">
                  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                    <polyline points="14 2 14 8 20 8" />
                  </svg>
                </div>
                <div className="file-details">
                  <span className="file-name">{file.name}</span>
                  <span className="file-size">
                    {(file.size / 1024).toFixed(1)} KB • Ready for extraction
                  </span>
                </div>
              </div>

              <div className="file-actions">
                <button
                  className="extract-btn"
                  onClick={handleExtract}
                  disabled={isProcessing}
                >
                  {isProcessing ? (
                    <>
                      <span className="btn-spinner"></span>
                      Extracting Text...
                    </>
                  ) : (
                    <>
                      <span>⚡</span> Extract Document Text
                    </>
                  )}
                </button>
                <button
                  className="remove-btn"
                  onClick={handleReset}
                  disabled={isProcessing}
                  title="Remove selected file"
                >
                  ✕
                </button>
              </div>
            </div>
          )}

          <div className="upload-note">
            <p>
              🔍 <strong>Phase 1 Text Extraction Active:</strong> Utilizing PyMuPDF for native PDF text layers
              and official Tesseract OCR for scanned documents and PNG/JPG images.
            </p>
          </div>
        </div>
      ) : (
        /* Results View */
        <div className="results-card">
          <div className="results-header">
            <div className="results-header-left">
              <h3 className="results-title">Extracted Document Content</h3>
              <div className="meta-pills">
                <span className="meta-pill">📄 {result.filename}</span>
                <span className="meta-pill">💾 {result.file_size_formatted}</span>
                <span className="meta-pill">📑 {result.page_count} page{result.page_count !== 1 ? 's' : ''}</span>
                <span className="meta-pill">🔤 {result.char_count.toLocaleString()} characters</span>
                <span className="meta-pill">📝 {result.word_count.toLocaleString()} words</span>
                <span className={`method-badge ${getMethodBadge(result.extraction_method).color}`}>
                  {getMethodBadge(result.extraction_method).label}
                </span>
              </div>
            </div>

            <div className="results-header-actions">
              <button className={`action-btn copy-btn ${copied ? 'copied' : ''}`} onClick={handleCopy}>
                {copied ? '✓ Copied!' : '📋 Copy Text'}
              </button>
              <button className="action-btn secondary-btn" onClick={handleReset}>
                🔄 Extract Another
              </button>
            </div>
          </div>

          <div className="extracted-content-box">
            {result.extracted_text ? (
              <pre className="extracted-text-body">{result.extracted_text}</pre>
            ) : (
              <div className="empty-text-notice">
                <p>⚠️ No readable text was detected in this document.</p>
              </div>
            )}
          </div>

          <div className="phase2-teaser">
            <div className="teaser-content">
              <span className="teaser-badge">Phase 2 Next</span>
              <p className="teaser-text">
                <strong>Ready for AI Simplification:</strong> In Phase 2, this extracted text will be simplified
                into plain language with executive summaries and a terminology glossary powered by Google Gemini.
              </p>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
