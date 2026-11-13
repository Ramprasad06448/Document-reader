import axios from 'axios';

// Base Axios instance pointing to the backend API
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
  timeout: 45000, // 45 seconds for OCR of large pages
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

export default api;
