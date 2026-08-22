 import { useEffect, useState } from 'react';
import SkillIntelligence from '../components/SkillIntelligence';

export default function SkillEvaluationPage() {
  const [candidateId, setCandidateId] = useState('');
  const [jobId, setJobId] = useState('');
  const [jobs, setJobs] = useState([]);
  const apiBaseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  useEffect(() => {
    const normalizeJobs = (rawJobs) => (
      (Array.isArray(rawJobs) ? rawJobs : [])
        .map((job) => {
          const id = job?.id ?? job?.jd_id ?? job?.job_id ?? job?.jobId ?? job?.uuid;
          const title = job?.title ?? job?.job_title ?? job?.jd_title ?? job?.name;
          return id ? { id: String(id), title: title || `Job ${id}` } : null;
        })
        .filter(Boolean)
    );

    const loadJobs = async () => {
      try {
        const token = localStorage.getItem('token');
        const res = await fetch(`${apiBaseUrl}/api/skills/jobs`, {
          headers: token ? { Authorization: `Bearer ${token}` } : {}
        });
        if (!res.ok) return;
        const data = await res.json();
        const normalizedJobs = normalizeJobs(data);
        setJobs(normalizedJobs);
        if (!jobId && normalizedJobs.length > 0) {
          setJobId(normalizedJobs[0].id);
        }
      } catch {
        setJobs([]);
      }
    };

    loadJobs();
  }, [apiBaseUrl, jobId]);

  return (
    <div style={{ minHeight: '100vh', background: '#0D0B1E', padding: '32px' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, color: 'white', marginBottom: '32px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Skill Graph Intelligence
        </h1>
        
        <div className="glass-card" style={{ padding: '24px', marginBottom: '24px' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'white', marginBottom: '16px' }}>
            Evaluation Parameters
          </h2>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px', marginBottom: '24px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 600, color: '#B8A9D9', marginBottom: '8px' }}>
                Candidate ID
              </label>
              <input
                type="text"
                value={candidateId}
                onChange={(e) => setCandidateId(e.target.value)}
                placeholder="Enter candidate UUID"
                style={{ width: '100%', padding: '12px 16px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '0.875rem' }}
              />
            </div>
            
            <div>
              <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: 600, color: '#B8A9D9', marginBottom: '8px' }}>
                Job ID
              </label>
              <select
                value={jobId}
                onChange={(e) => setJobId(e.target.value)}
                style={{ width: '100%', padding: '12px 16px', background: 'rgba(255, 255, 255, 0.05)', border: '1px solid rgba(255, 255, 255, 0.1)', borderRadius: '8px', color: 'white', fontSize: '0.875rem' }}
              >
                {jobs.length === 0 && <option value="">No jobs available</option>}
                {jobs.map((job) => (
                  <option key={job.id} value={job.id}>
                    {job.title}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div style={{ padding: '16px', background: 'rgba(123, 47, 255, 0.1)', borderRadius: '8px', border: '1px solid rgba(123, 47, 255, 0.3)' }}>
            <h3 style={{ fontSize: '0.875rem', fontWeight: 700, color: 'white', marginBottom: '12px' }}>Example Scenario</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px', fontSize: '0.875rem' }}>
              <div>
                <p className="text-secondary" style={{ marginBottom: '8px' }}>Job Requirements:</p>
                <ul style={{ color: '#B8A9D9', paddingLeft: '20px' }}>
                  <li>Data Analysis</li>
                  <li>SQL</li>
                  <li>Python</li>
                </ul>
              </div>
              <div>
                <p className="text-secondary" style={{ marginBottom: '8px' }}>Candidate Skills:</p>
                <ul style={{ color: '#B8A9D9', paddingLeft: '20px' }}>
                  <li>Business Analytics</li>
                  <li>SQL</li>
                  <li>Excel</li>
                  <li>Python</li>
                </ul>
              </div>
            </div>
            <p style={{ marginTop: '12px', fontSize: '0.75rem', color: '#7B2FFF', fontWeight: 600 }}>
              → System detects: Business Analytics ≈ Data Analysis (85% similarity)
            </p>
          </div>
        </div>

        {candidateId && jobId && <SkillIntelligence candidateId={candidateId} jobId={jobId} />}
        
        {(!candidateId || !jobId) && (
          <div className="glass-card" style={{ padding: '32px', textAlign: 'center' }}>
            <div style={{ width: '64px', height: '64px', background: 'linear-gradient(135deg, #7B2FFF, #E91E8C)', borderRadius: '12px', margin: '0 auto 16px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '2rem' }}>
              🧠
            </div>
            <p className="text-secondary">Enter both Candidate ID and Job ID to evaluate skill match</p>
          </div>
        )}
      </div>
    </div>
  );
}
