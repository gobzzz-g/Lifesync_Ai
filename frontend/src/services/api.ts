import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // If backend 401 occurs, don't immediately kick user out if user is stored locally
    if (error.response && error.response.status === 401) {
      if (error.config?.url?.includes('/api/auth/me')) {
        const savedUser = localStorage.getItem('user');
        if (!savedUser) {
          localStorage.removeItem('token');
          if (!window.location.pathname.includes('/login') && !window.location.pathname.includes('/register')) {
            window.location.href = '/login';
          }
        }
      }
    }
    return Promise.reject(error);
  }
);
export default api;
