import { useState, useEffect } from 'react';
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const getHeaders = () => ({
  'Content-Type': 'application/json',
  Authorization: `Bearer ${localStorage.getItem('token')}`
});

export default function CandidateBiasView() {
  const [applications, setApplications] = useState([]);
  const [biasViews, setBiasViews] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadApplications();
  }, []);

  const loadApplications = async () => {
    try {
      setLoading(true);
      const response = await axios.get(
        `${BASE_URL}/api/fairness/jobs`,
        { headers: getHeaders() }
      );
      
      if (Array.isArray(response.data)) {
        setApplications(response.data);
        
        for (const app of response.data) {
          try {
            const biasData = await axios.get(
              `${BASE_URL}/api/bias/candidate-view/${app.id}`,
              { headers: getHeaders() }
            );
            setBiasViews(prev => ({
              ...prev,
              [app.id]: biasData.data
            }));
          } catch (err) {
            console.log(`No bias data for ${app.id}`);
          }
        }
      }
    } catch (err) {
      setError('Failed to load applications');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getBiasStatusColor = (score) => {
    if (score === null || score === undefined) return 'bg-slate-100 text-slate-800';
    if (score < 4) return 'bg-green-100 text-green-800';
    if (score < 7) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  const getBiasStatusLabel = (score) => {
    if (score === null || score === undefined) return 'Pending Review';
    if (score < 4) return 'Low Bias';
    if (score < 7) return 'Moderate Bias';
    return 'High Bias — JD being improved';
  };

  const getBiasStatusMessage = (score) => {
    if (score === null || score === undefined) return 'Bias analysis not yet run for this job';
    return 'This job description has been reviewed for bias and inclusivity by Merit Mind AI';
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '40px', color: '#B8A9D9' }}>
        Loading your applications...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '8px', padding: '16px', color: '#FCA5A5' }}>
        {error}
      </div>
    );
  }

  if (applications.length === 0) {
    return (
      <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.07)', borderRadius: '12px', padding: '40px', textAlign: 'center', color: '#B8A9D9' }}>
        <p style={{ fontSize: '1rem', marginBottom: '8px' }}>No applications yet</p>
        <p style={{ fontSize: '0.9rem' }}>Apply to jobs to see their fairness status</p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'white', marginBottom: '8px' }}>Job Description Fairness Check</h2>
        <p style={{ color: '#B8A9D9', fontSize: '0.95rem' }}>
          See if the jobs you applied to have been reviewed for bias and inclusivity
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '16px' }}>
        {applications.map((app) => {
          const biasView = biasViews[app.id];
          const score = biasView?.overall_bias_score;
          const isChecked = biasView?.bias_checked;

          return (
            <div
              key={app.id}
              style={{
                background: 'rgba(255, 255, 255, 0.03)',
                border: '1px solid rgba(255, 255, 255, 0.07)',
                borderRadius: '12px',
                padding: '20px',
                display: 'flex',
                flexDirection: 'column',
                gap: '12px'
              }}
            >
              <div>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'white', marginBottom: '4px' }}>
                  {app.title}
                </h3>
                <p style={{ color: '#B8A9D9', fontSize: '0.9rem' }}>
                  {app.company || 'Unknown Company'}
                </p>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div
                  style={{
                    padding: '6px 12px',
                    borderRadius: '6px',
                    fontSize: '0.85rem',
                    fontWeight: 600
                  }}
                  className={getBiasStatusColor(score)}
                >
                  {isChecked ? 'Bias Reviewed' : 'Pending Review'}
                </div>
                {isChecked && score !== null && (
                  <span style={{ color: '#B8A9D9', fontSize: '0.9rem', fontWeight: 600 }}>
                    Score: {score.toFixed(1)}/10
                  </span>
                )}
              </div>

              {isChecked && score !== null && (
                <div style={{ background: 'rgba(255, 255, 255, 0.02)', borderRadius: '8px', padding: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                    <div
                      style={{
                        width: '100%',
                        height: '6px',
                        background: 'rgba(255, 255, 255, 0.1)',
                        borderRadius: '3px',
                        overflow: 'hidden'
                      }}
                    >
                      <div
                        style={{
                          width: `${(score / 10) * 100}%`,
                          height: '100%',
                          background: score < 4 ? '#22C55E' : score < 7 ? '#EAB308' : '#EF4444',
                          transition: 'width 0.3s ease'
                        }}
                      />
                    </div>
                  </div>
                  <p style={{ color: '#B8A9D9', fontSize: '0.85rem' }}>
                    {getBiasStatusLabel(score)}
                  </p>
                </div>
              )}

              <p style={{ color: '#B8A9D9', fontSize: '0.85rem', lineHeight: '1.5' }}>
                {getBiasStatusMessage(score)}
              </p>

              {biasView?.summary && (
                <div style={{ background: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.3)', borderRadius: '8px', padding: '12px', color: '#93C5FD', fontSize: '0.85rem' }}>
                  {biasView.summary}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
