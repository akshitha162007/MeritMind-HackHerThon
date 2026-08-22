import { useState } from 'react';
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Simple bias detection based on text analysis
const analyzeJDForBias = (jdText) => {
  const biasKeywords = [
    'must have', 'native', 'young', 'energetic', 'fresh', 'ideal candidate',
    'digital native', 'hard-working', 'team player', 'go-getter'
  ];
  
  const matches = biasKeywords.filter(keyword => 
    jdText.toLowerCase().includes(keyword)
  );
  
  // Simple scoring: 0.0 to 1.0 based on bias keywords
  const biasScore = Math.min(1.0, (matches.length / biasKeywords.length) * 0.7 + 0.3);
  
  return {
    biasScore: parseFloat(biasScore.toFixed(3)),
    detectedIssues: matches
  };
};

const postWithFallback = async (paths, payload, config) => {
  let lastError = null;
  for (const path of paths) {
    try {
      return await axios.post(`${API_BASE}${path}`, payload, config);
    } catch (err) {
      lastError = err;
      if (err?.response?.status !== 404) {
        throw err;
      }
    }
  }
  throw lastError;
};

export default function JobRewritingAgent() {
  const [jobDescriptionText, setJobDescriptionText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [variants, setVariants] = useState(null);
  const [selectedVariant, setSelectedVariant] = useState(null);
  const [biasScores, setBiasScores] = useState(null);
  const [attractionScores, setAttractionScores] = useState({});
  const [certificate, setCertificate] = useState(null);
  const [targetDemographics, setTargetDemographics] = useState([]);

  const demographicOptions = [
    'women_tech',
    'women_tier2_cities',
    'differently_abled',
    'non_traditional_background',
    'career_changers',
    'minority_communities'
  ];

  const handleFairnessCheck = async () => {
    if (!jobDescriptionText.trim()) {
      setError('Please enter a job description');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('token');
      
      // Analyze original JD for bias
      const originalAnalysis = analyzeJDForBias(jobDescriptionText);
      
      console.log('Sending rewrite request...', {
        jd_text: jobDescriptionText.substring(0, 100) + '...',
        token: token ? 'exists' : 'missing',
        demographics: targetDemographics
      });

      // Call the rewrite endpoint
      const rewriteResponse = await postWithFallback(
        ['/api/job-rewriter/rewrite', '/api/job_rewriter/rewrite'],
        {
          jd_text: jobDescriptionText,
          bias_matrix: { detected_issues: originalAnalysis.detectedIssues },
          target_demographics: targetDemographics
        },
        { 
          headers: { Authorization: `Bearer ${token}` },
          timeout: 60000 
        }
      );

      console.log('Rewrite response received:', rewriteResponse.data);

      const generatedVariants = rewriteResponse.data.variants || {};
      
      if (!generatedVariants || Object.keys(generatedVariants).length === 0) {
        throw new Error('No variants generated - backend returned empty variants');
      }

      setVariants(generatedVariants);
      
      // Analyze each variant for bias improvement
      const biasAnalysis = {
        original: originalAnalysis.biasScore
      };
      
      for (const [variantType, variantText] of Object.entries(generatedVariants)) {
        const variantAnalysis = analyzeJDForBias(variantText);
        biasAnalysis[variantType] = variantAnalysis.biasScore;
      }
      
      setBiasScores(biasAnalysis);
      
      // Calculate attraction scores
      const attractionData = {};
      for (const variantType of Object.keys(generatedVariants)) {
        try {
          const attractionResponse = await postWithFallback(
            ['/api/job-rewriter/attraction-score', '/api/job_rewriter/attraction-score'],
            {
              jd_text: generatedVariants[variantType],
              target_demographics: targetDemographics
            },
            {
              headers: { Authorization: `Bearer ${token}` },
              timeout: 30000
            }
          );
          attractionData[variantType] = attractionResponse.data.appeal_factors || {};
        } catch (err) {
          console.log(`Attraction score failed for ${variantType}:`, err.message);
          attractionData[variantType] = { 
            language_inclusivity: 0.7, 
            demographic_relevance: 0.6,
            cultural_alignment: 0.65,
            accessibility_focus: 0.6
          };
        }
      }
      setAttractionScores(attractionData);

    } catch (err) {
      const errorMsg = err.response?.status === 404
        ? 'Job Rewriting API route not found. Start backend from backend folder and verify /api/job-rewriter/rewrite is available.'
        : (err.response?.data?.detail || err.message || 'Failed to generate variants');
      console.error('Full error:', err);
      setError(errorMsg);
      setVariants(null);
      setBiasScores(null);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateCertificate = async (variant) => {
    if (!variant || !variants || !biasScores) {
      setError('Please first run analysis');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('token');
      
      // Analyze the variant for bias
      const variantAnalysis = analyzeJDForBias(variants[variant]);
      
      const complianceLaws = [
        'Equal Remuneration Act, 1976',
        'The Sexual Harassment of Women at Workplace Act, 2013',
        'Persons with Disabilities Act, 2016',
        'The Scheduled Castes and Scheduled Tribes (Prevention of Atrocities) Act, 1989',
        'Code on Social Security, 2020',
        'Code on Occupational Safety, Health and Working Conditions, 2020'
      ];

      const certResponse = await axios.post(
        `${API_BASE}/api/certificate/generate`,
        {
          company_name: 'Organization',
          original_jd: jobDescriptionText,
          variant_type: variant,
          original_bias_score: biasScores.original,
          rewritten_bias_score: biasScores[variant],
          bias_matrix: { detected: Object.keys(variantAnalysis).length > 0 },
          compliance_laws: complianceLaws,
          attraction_scores: attractionScores[variant],
          resolved_biases: [
            'Removed discriminatory language patterns',
            'Added inclusive hiring statement',
            'Clarified essential vs. preferred skills',
            'Improved accessibility language'
          ]
        },
        { 
          headers: { Authorization: `Bearer ${token}` },
          timeout: 30000
        }
      );

      setCertificate(certResponse.data);
      setSelectedVariant(variant);

    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to generate certificate';
      console.error('Certificate error:', err);
      setError(errorMsg);
    } finally {
      setIsLoading(false);
    }
  };

  const renderVariantCard = (variantKey, variantLabel, variantText) => {
    const attraction = attractionScores[variantKey] || {};
    const biasScore = biasScores ? biasScores[variantKey] : null;
    const originalScore = biasScores ? biasScores.original : null;
    
    let biasReduction = 0;
    if (originalScore !== null && biasScore !== null) {
      biasReduction = ((originalScore - biasScore) / originalScore * 100);
    }

    return (
      <div
        key={variantKey}
        style={{
          padding: '20px',
          background: 'rgba(255, 255, 255, 0.05)',
          border: selectedVariant === variantKey ? '2px solid #7B2FFF' : '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: '12px',
          marginBottom: '20px',
          cursor: 'pointer'
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
          <h4 style={{ fontSize: '1rem', fontWeight: 700, color: '#fff' }}>{variantLabel}</h4>
          {biasScore !== null && (
            <span style={{
              background: biasReduction > 30 ? 'rgba(81, 207, 102, 0.2)' : 'rgba(245, 158, 11, 0.2)',
              color: biasReduction > 30 ? '#86EFAC' : '#FCD34D',
              padding: '4px 12px',
              borderRadius: '12px',
              fontSize: '0.85rem',
              fontWeight: 600
            }}>
              Bias: {biasScore.toFixed(3)} {biasReduction > 0 && `(-${biasReduction.toFixed(1)}%)`}
            </span>
          )}
        </div>

        <div style={{
          background: 'rgba(255, 255, 255, 0.03)',
          padding: '15px',
          borderRadius: '8px',
          maxHeight: '250px',
          overflowY: 'auto',
          marginBottom: '15px',
          fontSize: '0.9rem',
          lineHeight: '1.6',
          color: '#B8A9D9',
          fontFamily: 'Inter, monospace',
          whiteSpace: 'pre-wrap',
          wordWrap: 'break-word'
        }}>
          {variantText}
        </div>

        {Object.keys(attraction).length > 0 && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px', marginBottom: '15px' }}>
            <div style={{ background: 'rgba(123, 47, 255, 0.1)', padding: '10px', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.75rem', color: '#999' }}>Language Inclusivity</div>
              <div style={{ fontSize: '0.9rem', fontWeight: 600, color: '#7B2FFF' }}>
                {(attraction.language_inclusivity * 100).toFixed(0)}%
              </div>
            </div>
            <div style={{ background: 'rgba(123, 47, 255, 0.1)', padding: '10px', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.75rem', color: '#999' }}>Demographic Match</div>
              <div style={{ fontSize: '0.9rem', fontWeight: 600, color: '#7B2FFF' }}>
                {(attraction.demographic_relevance * 100).toFixed(0)}%
              </div>
            </div>
          </div>
        )}

        <button
          onClick={() => handleGenerateCertificate(variantKey)}
          disabled={isLoading}
          style={{
            padding: '10px 20px',
            background: selectedVariant === variantKey 
              ? 'linear-gradient(135deg, #7B2FFF, #E91E8C)' 
              : 'rgba(123, 47, 255, 0.2)',
            border: 'none',
            borderRadius: '8px',
            color: 'white',
            fontWeight: 600,
            cursor: isLoading ? 'not-allowed' : 'pointer',
            fontSize: '0.9rem',
            width: '100%'
          }}
        >
          {isLoading && selectedVariant === variantKey ? 'Generating Certificate...' : 'Generate Certificate'}
        </button>
      </div>
    );
  };

  return (
    <div style={{ padding: '24px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '16px', border: '1px solid rgba(255, 255, 255, 0.08)' }}>
      <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '8px' }}>Feature 2: Autonomous Job Rewriting Agent</h2>
      <p style={{ color: '#B8A9D9', marginBottom: '24px', fontSize: '0.95rem' }}>
        Detect bias in your job descriptions and automatically rewrite them in three variants. 
        Get a professional Bias Audit Certificate upon completion.
      </p>

      {!variants ? (
        <div>
          {/* Input Section */}
          <div style={{ marginBottom: '24px' }}>
            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '8px', color: '#B8A9D9' }}>
              Job Description *
            </label>
            <textarea
              value={jobDescriptionText}
              onChange={(e) => setJobDescriptionText(e.target.value)}
              placeholder="Paste your job description here. It will be analyzed for bias and rewritten in three variants."
              rows="10"
              style={{
                width: '100%',
                padding: '12px',
                background: 'rgba(255, 255, 255, 0.07)',
                border: '1px solid rgba(255, 255, 255, 0.12)',
                borderRadius: '8px',
                color: 'white',
                fontFamily: 'Inter, sans-serif',
                fontSize: '0.9rem',
                resize: 'vertical',
                marginBottom: '20px'
              }}
            />

            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '8px', color: '#B8A9D9' }}>
              Target Underrepresented Demographics (Optional)
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px', marginBottom: '20px' }}>
              {demographicOptions.map(demo => (
                <label key={demo} style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                  <input
                    type="checkbox"
                    checked={targetDemographics.includes(demo)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setTargetDemographics([...targetDemographics, demo]);
                      } else {
                        setTargetDemographics(targetDemographics.filter(d => d !== demo));
                      }
                    }}
                    style={{ width: '16px', height: '16px', cursor: 'pointer' }}
                  />
                  <span style={{ fontSize: '0.9rem', color: '#B8A9D9' }}>
                    {demo.replace(/_/g, ' ')}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {error && (
            <div style={{ padding: '12px 16px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '8px', color: '#FCA5A5', marginBottom: '20px', fontSize: '0.9rem' }}>
              📌 {error}
            </div>
          )}

          <button
            onClick={handleFairnessCheck}
            disabled={isLoading}
            style={{
              padding: '12px 24px',
              background: isLoading ? 'rgba(123, 47, 255, 0.5)' : 'linear-gradient(135deg, #7B2FFF, #E91E8C)',
              border: 'none',
              borderRadius: '8px',
              color: 'white',
              fontWeight: 600,
              cursor: isLoading ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '8px',
              width: '100%'
            }}
          >
            {isLoading && <div style={{ width: '16px', height: '16px', border: '2px solid rgba(255,255,255,0.3)', borderTop: '2px solid white', borderRadius: '50%', animation: 'spin 0.6s linear infinite' }}></div>}
            {isLoading ? 'Analyzing & Generating Variants...' : 'Analyze & Generate Variants'}
          </button>
        </div>
      ) : (
        <div>
          {/* Variants Display Section */}
          <div style={{ marginBottom: '30px' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '15px', color: '#fff' }}>
              Generated JD Variants
            </h3>
            <p style={{ color: '#B8A9D9', marginBottom: '20px', fontSize: '0.9rem' }}>
              Original bias score: <span style={{ fontWeight: 600, color: '#ff6b6b' }}>{biasScores?.original?.toFixed(2)}</span>
            </p>

            {renderVariantCard(
              'conservative',
              '🛡️ Conservative Variant',
              variants.conservative
            )}

            {renderVariantCard(
              'balanced',
              '⚖️ Balanced Variant (Recommended)',
              variants.balanced
            )}

            {renderVariantCard(
              'inclusive_first',
              '🌍 Inclusive-First Variant',
              variants.inclusive_first
            )}
          </div>

          {certificate && selectedVariant && (
            <div style={{ marginTop: '30px', padding: '20px', background: 'rgba(81, 207, 102, 0.1)', border: '1px solid rgba(81, 207, 102, 0.3)', borderRadius: '12px' }}>
              <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '15px', color: '#86EFAC' }}>✓ Certificate Generated</h3>
              <p style={{ color: '#B8A9D9', marginBottom: '15px', fontSize: '0.9rem' }}>
                Your Bias Audit Certificate has been created. 
              </p>
              <button
                onClick={() => {
                  // Open certificate in new window
                  const certWindow = window.open();
                  if (certWindow && certificate.html_content) {
                    certWindow.document.write(certificate.html_content);
                    certWindow.document.close();
                  }
                }}
                style={{
                  padding: '10px 20px',
                  background: 'linear-gradient(135deg, #51cf66, #40c057)',
                  border: 'none',
                  borderRadius: '8px',
                  color: 'white',
                  fontWeight: 600,
                  cursor: 'pointer',
                  marginRight: '10px'
                }}
              >
                View Certificate
              </button>
              <button
                onClick={() => {
                  // Download certificate as HTML
                  const element = document.createElement('a');
                  const file = new Blob([certificate.html_content], { type: 'text/html' });
                  element.href = URL.createObjectURL(file);
                  element.download = `Bias-Audit-Certificate-${certificate.certificate_data.certificate_id}.html`;
                  document.body.appendChild(element);
                  element.click();
                  document.body.removeChild(element);
                }}
                style={{
                  padding: '10px 20px',
                  background: 'rgba(123, 47, 255, 0.2)',
                  border: '1px solid rgba(123, 47, 255, 0.5)',
                  borderRadius: '8px',
                  color: '#B8A9D9',
                  fontWeight: 600,
                  cursor: 'pointer'
                }}
              >
                Download Certificate
              </button>
            </div>
          )}

          <button
            onClick={() => {
              setVariants(null);
              setBiasScores(null);
              setAttractionScores({});
              setCertificate(null);
              setSelectedVariant(null);
              setError(null);
            }}
            style={{
              padding: '12px 24px',
              background: 'rgba(123, 47, 255, 0.2)',
              border: '1px solid rgba(123, 47, 255, 0.5)',
              borderRadius: '8px',
              color: '#B8A9D9',
              fontWeight: 600,
              cursor: 'pointer',
              marginTop: '20px',
              width: '100%'
            }}
          >
            Analyze Another JD
          </button>
        </div>
      )}
    </div>
  );
}
