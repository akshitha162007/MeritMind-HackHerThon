import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { registerUser } from '../api/auth';

export default function RegisterPage({ onSignUpSuccess }) {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    role: 'recruiter'
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!formData.name || !formData.email || !formData.password) {
      setError('Please fill in all fields');
      return;
    }
    
    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    setLoading(true);
    try {
      const data = await registerUser(formData);
      
      if (data && data.token) {
        onSignUpSuccess(data);
        navigate('/');
      } else {
        setError('Invalid response from server');
      }
    } catch (err) {
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: '#0D0B1E', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '24px' }}>
      <div className="glass-card" style={{ width: '100%', maxWidth: '420px', padding: '48px' }}>
        <h1 style={{ fontSize: '2rem', marginBottom: '8px', textAlign: 'center', color: 'white' }}>Create Account</h1>
        <p className="text-secondary" style={{ textAlign: 'center', marginBottom: '32px', fontSize: '0.95rem' }}>
          Join Merit Mind today
        </p>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', fontWeight: 500, color: 'white' }}>Full Name</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="John Doe"
              required
              style={{ 
                width: '100%',
                padding: '10px 12px',
                borderRadius: '8px',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                background: 'rgba(255, 255, 255, 0.05)',
                color: 'white'
              }}
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', fontWeight: 500, color: 'white' }}>Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="you@example.com"
              required
              style={{ 
                width: '100%',
                padding: '10px 12px',
                borderRadius: '8px',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                background: 'rgba(255, 255, 255, 0.05)',
                color: 'white'
              }}
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', fontWeight: 500, color: 'white' }}>Password</label>
            <div style={{ position: 'relative' }}>
              <input
                type={showPassword ? 'text' : 'password'}
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Min 8 characters"
                required
                style={{ 
                  width: '100%',
                  padding: '10px 12px',
                  paddingRight: '40px',
                  borderRadius: '8px',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                  background: 'rgba(255, 255, 255, 0.05)',
                  color: 'white'
                }}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{ position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', color: '#B8A9D9', cursor: 'pointer', fontSize: '1rem' }}
              >
                {showPassword ? '✓' : '○'}
              </button>
            </div>
          </div>

          <div style={{ marginBottom: '24px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', fontWeight: 500, color: 'white' }}>Role</label>
            <select
              name="role"
              value={formData.role}
              onChange={handleChange}
              style={{ 
                width: '100%',
                padding: '10px 12px',
                borderRadius: '8px',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                background: 'rgba(255, 255, 255, 0.05)',
                color: 'white'
              }}
            >
              <option value="recruiter" style={{ background: '#0D0B1E', color: 'white' }}>Recruiter</option>
              <option value="candidate" style={{ background: '#0D0B1E', color: 'white' }}>Candidate</option>
            </select>
          </div>

          {error && (
            <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '8px', padding: '12px', marginBottom: '20px', color: '#FCA5A5', fontSize: '0.9rem' }}>
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%',
              marginBottom: '20px',
              padding: '12px',
              borderRadius: '8px',
              border: 'none',
              background: loading ? 'rgba(123, 47, 255, 0.5)' : 'linear-gradient(135deg, #7B2FFF, #E91E8C)',
              color: 'white',
              fontWeight: 600,
              cursor: loading ? 'not-allowed' : 'pointer',
              transition: 'all 0.3s ease'
            }}
          >
            {loading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        <p style={{ textAlign: 'center', fontSize: '0.9rem', color: '#B8A9D9' }}>
          Already have an account?{' '}
          <Link to="/login" style={{ color: '#E91E8C', textDecoration: 'none', fontWeight: 600 }}>
            Sign In
          </Link>
        </p>
      </div>
    </div>
  );
}
