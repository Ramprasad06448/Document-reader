import axios from 'axios';

// Base Axios instance pointing to the backend API
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
  timeout: 60000, // 60 seconds for OCR and AI pipelines
});

/**
 * Checks the health status of the DocuEase backend.
 * @returns {Promise<{status: string, message: string}>}
 */
export const checkHealth = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

/**
 * Uploads a document to the backend for text extraction (TXT, PDF, JPG, PNG).
 * @param {File} file - The file to upload and extract
 * @returns {Promise<object>} Extracted document metadata and text
 */
export const extractDocument = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/api/extract', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

/**
 * Simplifies raw text using the Gemini AI simplification engine.
 * @param {string} text - The input text to simplify
 * @param {string} level - Simplification level
 * @returns {Promise<object>} Structured simplification result
 */
export const simplifyText = async (text, level = 'plain_language') => {
  const response = await api.post('/api/simplify', {
    text,
    level,
  });
  return response.data;
};

/**
 * Uploads a file and simplifies it in one step.
 * @param {File} file - Document file (PDF, TXT, PNG, JPG)
 * @param {string} level - Simplification level
 * @returns {Promise<object>} Extracted metadata and simplified result
 */
export const simplifyDocument = async (file, level = 'plain_language') => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post(`/api/simplify?level=${encodeURIComponent(level)}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export default api;
