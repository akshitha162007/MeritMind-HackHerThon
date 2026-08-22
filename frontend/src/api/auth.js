import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 45000,
  headers: {
    'Content-Type': 'application/json'
  }
});

const isTransientNetworkError = (error) => {
  return error.code === 'ECONNABORTED' || !error.response;
};

const withOneRetry = async (requestFn) => {
  try {
    return await requestFn();
  } catch (error) {
    if (!isTransientNetworkError(error)) {
      throw error;
    }
    return await requestFn();
  }
};

api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message,
      url: error.config?.url
    });
    return Promise.reject(error);
  }
);

export const registerUser = async ({ name, email, password, role }) => {
  try {
    const payload = {
      name: (name || '').trim(),
      email: (email || '').trim().toLowerCase(),
      password,
      role: role || 'recruiter'
    };
    
    const response = await withOneRetry(() => api.post('/api/auth/register', payload));
    return response.data;
  } catch (error) {
    const errorMsg = error.response?.data?.detail || error.message || 'Registration failed';
    throw new Error(errorMsg);
  }
};

export const loginUser = async ({ email, password }) => {
  try {
    const payload = {
      email: (email || '').trim().toLowerCase(),
      password
    };
    
    const response = await withOneRetry(() => api.post('/api/auth/login', payload));
    return response.data;
  } catch (error) {
    const errorMsg = error.response?.data?.detail || error.message || 'Login failed';
    throw new Error(errorMsg);
  }
};

export const logoutUser = async (token) => {
  try {
    const response = await api.post(
      '/api/auth/logout',
      { token },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    return response.data;
  } catch (error) {
    return { ok: true };
  }
};
