import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { loginUser } from '../api/auth';

export default function LoginPage({ onLoginSuccess }) {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!email || !password) {
      setError('Please fill in all fields');
      return;
    }

    setLoading(true);
    try {
      const data = await loginUser({ email, password });
      
      if (data && data.token) {
        onLoginSuccess(data);
        navigate('/');
      } else {
        setError('Invalid response from server');
      }
    } catch (err) {
      setError(err.message || 'Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: '#0D0B1E', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '24px' }}>
      <div className="glass-card" style={{ width: '100%', maxWidth: '420px', padding: '48px' }}>
        <h1 style={{ fontSize: '2rem', marginBottom: '8px', textAlign: 'center', color: 'white' }}>Sign In</h1>
        <p className="text-secondary" style={{ textAlign: 'center', marginBottom: '32px', fontSize: '0.95rem' }}>
          Welcome back to Merit Mind
        </p>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', fontWeight: 500, color: 'white' }}>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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

          <div style={{ marginBottom: '24px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', fontWeight: 500, color: 'white' }}>Password</label>
            <div style={{ position: 'relative' }}>
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
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
            {loading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>

        <p style={{ textAlign: 'center', fontSize: '0.9rem', color: '#B8A9D9' }}>
          Don't have an account?{' '}
          <Link to="/register" style={{ color: '#E91E8C', textDecoration: 'none', fontWeight: 600 }}>
            Sign Up
          </Link>
        </p>
      </div>
    </div>
  );
}
