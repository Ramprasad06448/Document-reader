import axios from 'axios';

// Create base Axios instance pointing to the backend API
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Checks the health status of the DocuEase backend.
 * @returns {Promise<{status: string, message: string}>}
 */
export const checkHealth = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

export default api;
