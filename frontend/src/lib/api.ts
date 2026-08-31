import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error caught in interceptor:", error.message);
    // Return a graceful fallback response to prevent frontend crashes on 503 / 500
    // Components will receive { data: null } and should handle it gracefully
    return Promise.resolve({ data: null });
  }
);

export default api;
