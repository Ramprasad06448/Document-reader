import React, { useState } from 'react';
import { extractDocument, simplifyText, simplifyDocument } from '../services/api';
import DualPaneViewer from './DualPaneViewer';

const ALLOWED_EXTENSIONS = ['pdf', 'txt', 'png', 'jpg', 'jpeg'];
const MAX_SIZE_MB = 10;

export default function DocumentProcessor() {
  const [activeTab, setActiveTab] = useState('upload'); // 'upload' | 'text'
  const [file, setFile] = useState(null);
  const [rawText, setRawText] = useState('');
  const [level, setLevel] = useState('plain_language');
  const [isDragging, setIsDragging] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStage, setProcessingStage] = useState('');
  const [error, setError] = useState(null);

  // Results state
  const [simplifiedResult, setSimplifiedResult] = useState(null);
  const [extractOnlyResult, setExtractOnlyResult] = useState(null);
  const [copiedExtract, setCopiedExtract] = useState(false);

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
      setExtractOnlyResult(null);
      setSimplifiedResult(null);
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
      setExtractOnlyResult(null);
      setSimplifiedResult(null);
    }
  };

  // Phase 1 Extract Only
  const handleExtractOnly = async () => {
    if (!file) return;

    setIsProcessing(true);
    setProcessingStage('Extracting text via PyMuPDF / Tesseract OCR...');
    setError(null);

    try {
      const data = await extractDocument(file);
      if (data.status === 'success') {
        setExtractOnlyResult(data);
      } else {
        setError(data.message || 'Failed to extract text.');
      }
    } catch (err) {
      const msg = err.response?.data?.message || err.message || 'Network error occurred.';
      setError(`Extraction failed: ${msg}`);
    } finally {
      setIsProcessing(false);
      setProcessingStage('');
    }
  };

  // Phase 2 Full Simplification
  const handleSimplify = async () => {
    setIsProcessing(true);
    setError(null);
    setExtractOnlyResult(null);

    try {
      if (activeTab === 'upload') {
        if (!file) {
          setError('Please select or drop a file to simplify.');
          setIsProcessing(false);
          return;
        }
        setProcessingStage('Ingesting document & extracting text layers...');
        const res = await simplifyDocument(file, level);
        if (res.status === 'success') {
          setSimplifiedResult(res);
        } else {
          setError(res.message || 'Simplification failed.');
        }
      } else {
        if (!rawText.trim()) {
          setError('Please paste or type the text you wish to simplify.');
          setIsProcessing(false);
          return;
        }
        setProcessingStage('Analyzing document structure with AI Simplification Engine...');
        const res = await simplifyText(rawText.trim(), level);
        if (res.status === 'success') {
          setSimplifiedResult(res);
        } else {
          setError(res.message || 'Simplification failed.');
        }
      }
    } catch (err) {
      const msg = err.response?.data?.message || err.message || 'Network error.';
      setError(`Simplification failed: ${msg}`);
    } finally {
      setIsProcessing(false);
      setProcessingStage('');
    }
  };

  const handleSimplifyExtracted = async () => {
    if (!extractOnlyResult?.extracted_text) return;
    setIsProcessing(true);
    setProcessingStage('Simplifying extracted text with AI Plain-Language Engine...');
    setError(null);

    try {
      const res = await simplifyText(extractOnlyResult.extracted_text, level);
      if (res.status === 'success') {
        res.document_metadata = {
          filename: extractOnlyResult.filename,
          page_count: extractOnlyResult.page_count,
          file_extension: extractOnlyResult.file_extension,
        };
        setSimplifiedResult(res);
        setExtractOnlyResult(null);
      } else {
        setError(res.message || 'Simplification failed.');
      }
    } catch (err) {
      setError(`Simplification failed: ${err.message}`);
    } finally {
      setIsProcessing(false);
      setProcessingStage('');
    }
  };

  const handleReset = () => {
    setFile(null);
    setRawText('');
    setSimplifiedResult(null);
    setExtractOnlyResult(null);
    setError(null);
  };

  // If simplified result exists, display DualPaneViewer
  if (simplifiedResult) {
    return <DualPaneViewer data={simplifiedResult} onReset={handleReset} />;
  }

  return (
    <section className="processor-section">
      {error && (
        <div className="alert-banner alert-error">
          <span className="alert-icon">⚠️</span>
          <span className="alert-text">{error}</span>
          <button className="alert-close" onClick={() => setError(null)}>✕</button>
        </div>
      )}

      {/* Input Mode Navigation Tabs */}
      <div className="tab-bar">
        <button
          className={`tab-btn ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
          disabled={isProcessing}
        >
          📁 Upload Document (PDF, TXT, PNG, JPG)
        </button>
        <button
          className={`tab-btn ${activeTab === 'text' ? 'active' : ''}`}
          onClick={() => setActiveTab('text')}
          disabled={isProcessing}
        >
          ✍️ Direct Text Paste
        </button>
      </div>

      <div className="upload-card">
        {/* Simplification Level Bar */}
        <div className="level-bar">
          <span className="level-label">Simplification Level:</span>
          <div className="level-options">
            <button
              className={`level-pill ${level === 'plain_language' ? 'active' : ''}`}
              onClick={() => setLevel('plain_language')}
            >
              Everyday Plain English
            </button>
            <button
              className={`level-pill ${level === 'executive_summary' ? 'active' : ''}`}
              onClick={() => setLevel('executive_summary')}
            >
              Executive Summary
            </button>
            <button
              className={`level-pill ${level === 'middle_school' ? 'active' : ''}`}
              onClick={() => setLevel('middle_school')}
            >
              Elementary / ESL
            </button>
          </div>
        </div>

        {activeTab === 'upload' ? (
          <>
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

              <h3 className="dropzone-title">Upload Complex Document</h3>
              <p className="dropzone-subtitle">
                Drag and drop your file here, or click to browse
              </p>

              <label className="browse-button" htmlFor="doc-input">
                Select File
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
                      {(file.size / 1024).toFixed(1)} KB • Ready for processing
                    </span>
                  </div>
                </div>

                <div className="file-actions">
                  <button
                    className="simplify-btn-primary"
                    onClick={handleSimplify}
                    disabled={isProcessing}
                  >
                    {isProcessing ? (
                      <>
                        <span className="btn-spinner"></span>
                        {processingStage || 'Processing...'}
                      </>
                    ) : (
                      <>
                        <span>✨</span> Simplify with AI
                      </>
                    )}
                  </button>

                  <button
                    className="extract-btn-secondary"
                    onClick={handleExtractOnly}
                    disabled={isProcessing}
                  >
                    Extract Text Only
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
          </>
        ) : (
          /* Text Paste Tab */
          <div className="text-paste-zone">
            <textarea
              className="text-input-area"
              rows="8"
              placeholder="Paste contract clauses, medical records, policy terms, or technical text here..."
              value={rawText}
              onChange={(e) => setRawText(e.target.value)}
              disabled={isProcessing}
            ></textarea>
            <div className="paste-actions">
              <span className="char-counter">
                {rawText.trim().split(/\s+/).filter(Boolean).length} words • {rawText.length} characters
              </span>
              <button
                className="simplify-btn-primary"
                onClick={handleSimplify}
                disabled={isProcessing || !rawText.trim()}
              >
                {isProcessing ? (
                  <>
                    <span className="btn-spinner"></span>
                    {processingStage || 'Simplifying...'}
                  </>
                ) : (
                  <>
                    <span>✨</span> Simplify Text with AI
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {/* Phase 1 Extract Only Results View */}
        {extractOnlyResult && (
          <div className="extract-only-container">
            <div className="extract-header">
              <div className="extract-meta">
                <h4>Extracted Text ({extractOnlyResult.word_count} words)</h4>
                <span className="method-pill">{extractOnlyResult.extraction_method}</span>
              </div>
              <div className="extract-actions">
                <button
                  className="simplify-btn-primary small"
                  onClick={handleSimplifyExtracted}
                  disabled={isProcessing}
                >
                  ✨ Simplify This Extracted Text
                </button>
                <button
                  className="copy-btn small"
                  onClick={() => {
                    navigator.clipboard.writeText(extractOnlyResult.extracted_text);
                    setCopiedExtract(true);
                    setTimeout(() => setCopiedExtract(false), 2000);
                  }}
                >
                  {copiedExtract ? '✓ Copied' : '📋 Copy Text'}
                </button>
              </div>
            </div>
            <pre className="extracted-text-body">{extractOnlyResult.extracted_text}</pre>
          </div>
        )}

        <div className="upload-note">
          <p>
            ✨ <strong>Full Pipeline Active:</strong> Ingest native PDFs (PyMuPDF), scanned files/images (Tesseract OCR),
            and simplify with Google Gemini plain-language AI synthesis with synchronized dual-pane comparison.
          </p>
        </div>
      </div>
    </section>
  );
}
