import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const getHeaders = () => ({
  'Content-Type': 'application/json',
  Authorization: `Bearer ${localStorage.getItem('token')}`
});

export const analyzeJDText = async (jd_text) => {
  const response = await axios.post(
    `${BASE_URL}/api/bias/analyze-text`,
    { jd_text },
    { headers: getHeaders() }
  );
  return response.data;
};

export const runBiasAnalysis = async (jd_id) => {
  const response = await axios.post(
    `${BASE_URL}/api/bias/analyze/${jd_id}`,
    {},
    { headers: getHeaders() }
  );
  return response.data;
};

export const getBiasReport = async (jd_id) => {
  const response = await axios.get(
    `${BASE_URL}/api/bias/report/${jd_id}`,
    { headers: getHeaders() }
  );
  return response.data;
};

export const rewriteJD = async (jd_id, variant = 'balanced') => {
  const response = await axios.post(
    `${BASE_URL}/api/bias/rewrite/${jd_id}`,
    { variant },
    { headers: getHeaders() }
  );
  return response.data;
};

export const getJDList = async () => {
  const response = await axios.get(
    `${BASE_URL}/api/bias/jd-list`,
    { headers: getHeaders() }
  );
  return response.data;
};

export const getCandidateBiasView = async (jd_id) => {
  const response = await axios.get(
    `${BASE_URL}/api/bias/candidate-view/${jd_id}`,
    { headers: getHeaders() }
  );
  return response.data;
};
