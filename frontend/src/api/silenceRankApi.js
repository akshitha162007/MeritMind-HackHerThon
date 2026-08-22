import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const runSilenceRank = async (jd_id, application_ids) => {
  try {
    const token = localStorage.getItem('token');
    const response = await api.post('/api/silence-rank/run', {
      jd_id,
      application_ids
    }, {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to run SilenceRank analysis');
  }
};

export const getSilenceRankResults = async (jd_id) => {
  try {
    const token = localStorage.getItem('token');
    const response = await api.get(`/api/silence-rank/results/${jd_id}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch SilenceRank results');
  }
};
