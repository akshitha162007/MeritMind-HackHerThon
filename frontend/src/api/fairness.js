const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const fairnessAPI = {
  checkFairness: async (candidateId) => {
    const token = localStorage.getItem('token');
    const response = await fetch(`${API_BASE_URL}/api/fairness/check`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ candidate_id: candidateId })
    });
    
    if (!response.ok) {
      throw new Error('Failed to check fairness');
    }
    
    return response.json();
  }
};
