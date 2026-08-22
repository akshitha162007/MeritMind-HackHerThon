import { useState } from 'react';
import { analyzeJDText } from '../api/biasApi';

const DEMO_JD = `Software Engineer — TechCorp India

We are looking for a young, energetic male engineer preferably
from IIT or NIT with excellent communication skills.
The ideal candidate should be physically fit, willing to
relocate anywhere in India without family commitments.
Hindi fluency is mandatory for this role.
We prefer candidates from premier institutes with a
strong personality who can lead from the front.
Must be available for frequent travel.`;

// ─── Indian-specific bias taxonomy ───────────────────────────────────────────
const TAXONOMY = [
  {
    id: 'college_tier',
    label: 'College Tier Hierarchy',
    color: '#F59E0B',
    patterns: [
      /\bIIT(s)?\b/gi, /\bNIT(s)?\b/gi, /\bIIM(s)?\b/gi, /\bBITS\b/gi,
      /premier\s*institute/gi, /top[-\s]tier\s*college/gi, /tier.?1\s*college/gi,
    ],
    severity: 8,
    intersects_with: ['socioeconomic'],
    description: 'Preference for elite institutions doubly excludes state-college graduates and first-generation professionals whose families could not afford JEE coaching.',
    harmed: 'State college graduates · First-generation professionals · Rural candidates',
    rewrite: 'strong engineering background from any accredited program',
  },
  {
    id: 'regional_language',
    label: 'Regional Language Discrimination',
    color: '#EF4444',
    patterns: [
      /Hindi\s*(fluency|mandatory|required|proficiency|speaking)/gi,
      /fluent\s*in\s*Hindi/gi,
      /native\s*Hindi/gi,
      /mother\s*tongue\s*Hindi/gi,
      /Hindi[-\s]speaking\s*(preferred|mandatory|required)/gi,
    ],
    severity: 8,
    intersects_with: ['caste'],
    description: 'Requiring Hindi in non-language roles silently closes the door on South Indian, Northeast Indian, and other non-Hindi-speaking engineers.',
    harmed: 'South Indian candidates · Northeast Indian candidates · Non-Hindi professionals',
    rewrite: 'strong written and verbal communication skills in English',
  },
  {
    id: 'gender',
    label: 'Gender Bias',
    color: '#EC4899',
    patterns: [
      /\bmale\s*(engineer|candidate|applicant)/gi,
      /\bhe\s*should\b/gi,
      /\bbrotherhood\b/gi,
      /young.*male/gi,
      /male[-\s]dominated/gi,
    ],
    severity: 9,
    intersects_with: ['age', 'matrimonial'],
    description: 'Explicit or implied gendered language creates an unwelcoming signal that disproportionately drives women away.',
    harmed: 'Women · Non-binary candidates · Gender-diverse applicants',
    rewrite: 'skilled engineer with demonstrated technical ability',
  },
  {
    id: 'age',
    label: 'Age Discrimination',
    color: '#8B5CF6',
    patterns: [
      /\byoung\s*(and\s*dynamic|engineer|professional|candidate)?/gi,
      /digital\s*native/gi,
      /fresh\s*graduate/gi,
      /recent\s*graduate/gi,
      /\benergetic\s*youngster/gi,
    ],
    severity: 7,
    intersects_with: ['gender'],
    description: 'Age-coded words exclude experienced professionals and people returning from career breaks.',
    harmed: 'Experienced professionals · Career returners · Parents re-entering workforce',
    rewrite: 'motivated professional with relevant skills',
  },
  {
    id: 'matrimonial',
    label: 'Matrimonial Status Signal',
    color: '#F97316',
    patterns: [
      /without\s*family\s*commitments/gi,
      /no\s*family\s*obligations/gi,
      /willing\s*to\s*relocate\s*without/gi,
      /bachelor\s*preferred/gi,
      /single\s*preferred/gi,
    ],
    severity: 7,
    intersects_with: ['gender'],
    description: 'Matrimonial proxies disproportionately penalise women with families.',
    harmed: 'Married women · Parents · Candidates with caregiving responsibilities',
    rewrite: 'flexibility for occasional travel as required by the role',
  },
  {
    id: 'socioeconomic',
    label: 'Socioeconomic Class Marker',
    color: '#06B6D4',
    patterns: [
      /excellent\s*English/gi,
      /impeccable\s*English/gi,
      /native[-\s]level\s*English/gi,
      /convent[-\s]educated/gi,
      /foreign[-\s]educated/gi,
      /studied\s*abroad\s*preferred/gi,
    ],
    severity: 6,
    intersects_with: ['college_tier', 'caste'],
    description: '"Excellent English" as a criterion is a proxy for socioeconomic class.',
    harmed: 'Regional-medium graduates · First-generation professionals · Tier-2/3 city candidates',
    rewrite: 'clear and professional communication skills',
  },
  {
    id: 'caste',
    label: 'Caste Signal (Cultural Fit)',
    color: '#10B981',
    patterns: [
      /cultural\s*fit/gi,
      /good\s*family\s*background/gi,
      /from\s*a\s*good\s*family/gi,
      /\bwell[-\s]bred\b/gi,
      /right\s*background/gi,
      /decent\s*background/gi,
    ],
    severity: 9,
    intersects_with: ['socioeconomic', 'regional_language'],
    description: '"Cultural fit" and "good family background" are proxies for caste discrimination in Indian hiring.',
    harmed: 'OBC / SC / ST candidates · First-generation professionals · Minority communities',
    rewrite: 'alignment with our core values of collaboration and integrity',
  },
  {
    id: 'physical',
    label: 'Physical Appearance Bias',
    color: '#64748B',
    patterns: [
      /physically\s*fit/gi,
      /good[-\s]looking/gi,
      /presentable\s*appearance/gi,
      /\bwell[-\s]groomed\b/gi,
      /\battractive\b/gi,
    ],
    severity: 6,
    intersects_with: ['gender'],
    description: 'Physical appearance requirements create barriers for differently-abled candidates.',
    harmed: 'Differently-abled candidates · Candidates with visible disabilities',
    rewrite: 'professional demeanor and strong interpersonal skills',
  },
];

const AXES = ['gender', 'age', 'caste', 'college_tier', 'regional_language', 'socioeconomic', 'matrimonial', 'physical'];
const AXIS_LABELS = {
  gender: 'Gender', age: 'Age', caste: 'Caste', college_tier: 'College', regional_language: 'Regional Lang',
  socioeconomic: 'Socioeconomic', matrimonial: 'Matrimonial', physical: 'Physical',
};

// ─── Local analysis engine ────────────────────────────────────────────────────
const analyzeLocally = (jdText) => {
  const flags = [];

  for (const cat of TAXONOMY) {
    for (const pattern of cat.patterns) {
      const matches = [...jdText.matchAll(new RegExp(pattern.source, pattern.flags))];
      if (matches.length > 0 && !flags.find(f => f.axis === cat.id)) {
        flags.push({
          axis: cat.id,
          label: cat.label,
          color: cat.color,
          intersectional_axes: [cat.id, ...cat.intersects_with],
          trigger_phrase: matches[0][0],
          severity: cat.severity,
          harmed_demographic: cat.harmed,
          explanation: cat.description,
          suggested_rewrite: cat.rewrite,
        });
      }
    }
  }

  const matrix = [];
  for (const f1 of flags) {
    for (const f2 of flags) {
      if (f1.axis < f2.axis && f1.intersectional_axes.includes(f2.axis)) {
        matrix.push({
          axis_row: f1.axis,
          axis_col: f2.axis,
          score: Math.min(1.0, (f1.severity + f2.severity) / 20),
          compound_harm: `Specifically excludes candidates affected by both ${f1.label.toLowerCase()} and ${f2.label.toLowerCase()}`,
        });
      }
    }
  }

  const criticalCount = flags.filter(f => f.severity >= 8).length;
  const overallScore = flags.length === 0
    ? 0
    : parseFloat(Math.min(10, (flags.reduce((s, f) => s + f.severity, 0) / flags.length) * (1 + matrix.length * 0.06)).toFixed(1));

  return {
    overall_bias_score: overallScore,
    bias_flags: flags,
    matrix,
    summary: flags.length === 0
      ? 'No significant bias patterns detected.'
      : `Found ${flags.length} bias pattern(s) with ${matrix.length} intersectional compounds. ${criticalCount} critical bias(es) will narrow your candidate pool.`,
  };
};

export default function BiasDetectionPanel() {
  const [jdText, setJdText] = useState('');
  const [result, setResult] = useState(null);
  const [rewriteResult, setRewriteResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [rewriteLoading, setRewriteLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isDemo, setIsDemo] = useState(false);

  const handleLoadDemo = () => {
    setJdText(DEMO_JD);
    setResult(null);
    setRewriteResult(null);
    setError(null);
    setIsDemo(false);
  };

  const handleAnalyze = async () => {
    if (!jdText.trim()) {
      setError('Please paste a job description to analyze.');
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    setRewriteResult(null);
    setIsDemo(false);

    try {
      const data = await analyzeJDText(jdText);
      setResult(data);
    } catch {
      const localResult = analyzeLocally(jdText);
      setResult(localResult);
      setIsDemo(true);
    } finally {
      setLoading(false);
    }
  };

  const handleRewrite = () => {
    if (!result) return;
    setRewriteLoading(true);

    const rewritten = result.bias_flags.reduce((text, flag) => {
      try {
        const cat = TAXONOMY.find(t => t.id === flag.axis);
        if (!cat) return text;
        for (const pat of cat.patterns) {
          const re = new RegExp(pat.source, pat.flags);
          if (re.test(text)) {
            return text.replace(re, flag.suggested_rewrite);
          }
        }
      } catch { /* skip */ }
      return text;
    }, jdText);

    const newScore = Math.max(0, result.overall_bias_score - result.bias_flags.length * 0.8);

    setRewriteResult({
      rewritten_jd: rewritten,
      original_bias_score: result.overall_bias_score,
      new_bias_score: parseFloat(newScore.toFixed(1)),
      changes: result.bias_flags.map(f => ({
        original: f.trigger_phrase,
        replacement: f.suggested_rewrite,
        reason: f.label,
      })),
    });
    setRewriteLoading(false);
  };

  const severityLabel = (s) => s >= 8 ? 'Critical' : s >= 5 ? 'Medium' : 'Low';
  const severityBg = (s) => s >= 8 ? 'rgba(239,68,68,0.15)' : s >= 5 ? 'rgba(234,179,8,0.15)' : 'rgba(34,197,94,0.15)';
  const severityText = (s) => s >= 8 ? '#FCA5A5' : s >= 5 ? '#FDE68A' : '#86EFAC';
  const scoreBg = (score) => score > 0.7 ? 'rgba(239,68,68,0.2)' : score > 0.4 ? 'rgba(234,179,8,0.2)' : score > 0 ? 'rgba(34,197,94,0.2)' : 'rgba(255,255,255,0.04)';
  const scoreText = (score) => score > 0.7 ? '#FCA5A5' : score > 0.4 ? '#FDE68A' : score > 0 ? '#86EFAC' : '#475569';
  const globalScoreColor = (s) => s > 7 ? '#EF4444' : s > 4 ? '#F59E0B' : '#22C55E';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{
        background: 'linear-gradient(135deg, rgba(239,68,68,0.08), rgba(123,47,255,0.08))',
        border: '1px solid rgba(239,68,68,0.25)',
        borderRadius: '16px',
        padding: '24px',
      }}>
        <p style={{ fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.12em', color: '#EF4444', fontWeight: 700, marginBottom: '10px' }}>
          The damage begins at the job description itself
        </p>
        <p style={{ color: '#CBD5E1', lineHeight: 1.7, fontSize: '0.95rem', marginBottom: '12px' }}>
          Before a single candidate reads it, the JD is already silently eliminating people. Phrases like "IIT/NIT preferred", "Hindi fluency mandatory", "young and dynamic" — each quietly closes the door on entire groups. The problem unique to India: these biases stack. "IIT preferred" + "Hindi mandatory" doesn't just exclude independently — it specifically and doubly excludes a South Indian state-college graduate.
        </p>
      </div>

      <div style={{
        background: 'rgba(255,255,255,0.03)',
        border: '1px solid rgba(255,255,255,0.08)',
        borderRadius: '14px',
        padding: '20px',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'white' }}>Paste Your Job Description</h3>
          <button
            onClick={handleLoadDemo}
            style={{
              fontSize: '0.8rem', padding: '6px 14px', borderRadius: '6px',
              border: '1px solid rgba(123,47,255,0.4)',
              background: 'rgba(123,47,255,0.12)', color: '#A78BFA',
              cursor: 'pointer', fontWeight: 600,
            }}
          >
            Load Demo
          </button>
        </div>
        <textarea
          value={jdText}
          onChange={(e) => setJdText(e.target.value)}
          placeholder="Paste the job description here..."
          rows={10}
          style={{
            width: '100%', boxSizing: 'border-box',
            padding: '14px', borderRadius: '10px',
            border: '1px solid rgba(255,255,255,0.12)',
            background: 'rgba(0,0,0,0.3)', color: '#E2E8F0',
            fontSize: '0.9rem', lineHeight: 1.6,
            resize: 'vertical', outline: 'none',
            fontFamily: 'inherit',
          }}
        />
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '12px' }}>
          <button
            onClick={handleAnalyze}
            disabled={loading || !jdText.trim()}
            style={{
              padding: '11px 28px', borderRadius: '9px', border: 'none',
              background: loading || !jdText.trim() ? 'rgba(123,47,255,0.35)' : 'linear-gradient(135deg, #7B2FFF, #E91E8C)',
              color: 'white', fontWeight: 700, fontSize: '0.95rem',
              cursor: loading || !jdText.trim() ? 'not-allowed' : 'pointer',
            }}
          >
            {loading ? '🔍 Scanning…' : 'Detect Bias'}
          </button>
        </div>
      </div>

      {error && (
        <div style={{
          background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)',
          borderRadius: '8px', padding: '12px', color: '#FCA5A5', fontSize: '0.9rem',
        }}>
          {error}
        </div>
      )}

      {isDemo && (
        <div style={{
          background: 'rgba(59,130,246,0.08)', border: '1px solid rgba(59,130,246,0.25)',
          borderRadius: '8px', padding: '10px 14px', color: '#93C5FD', fontSize: '0.85rem',
        }}>
          Backend unavailable — showing local analysis.
        </div>
      )}

      {result && (
        <>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'auto 1fr',
            gap: '20px',
            background: 'rgba(255,255,255,0.03)',
            border: '1px solid rgba(255,255,255,0.08)',
            borderRadius: '14px',
            padding: '20px',
          }}>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '4px' }}>
              <svg width="100" height="100" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="42" fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="10" />
                <circle
                  cx="50" cy="50" r="42" fill="none"
                  stroke={globalScoreColor(result.overall_bias_score)}
                  strokeWidth="10"
                  strokeDasharray={`${2 * Math.PI * 42 * result.overall_bias_score / 10} ${2 * Math.PI * 42}`}
                  strokeLinecap="round"
                  transform="rotate(-90 50 50)"
                />
                <text x="50" y="46" textAnchor="middle" fill="white" fontSize="20" fontWeight="800">
                  {result.overall_bias_score.toFixed(1)}
                </text>
                <text x="50" y="62" textAnchor="middle" fill="#94A3B8" fontSize="9"> / 10</text>
              </svg>
            </div>
            <div>
              <div style={{ display: 'flex', gap: '12px', marginBottom: '14px', flexWrap: 'wrap' }}>
                {[
                  { label: 'Flags', value: result.bias_flags.length, color: '#F59E0B' },
                  { label: 'Critical', value: result.bias_flags.filter(f => f.severity >= 8).length, color: '#EF4444' },
                  { label: 'Compounds', value: result.matrix.length, color: '#A78BFA' },
                ].map(stat => (
                  <div key={stat.label} style={{ padding: '10px 16px', borderRadius: '10px', background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.07)', textAlign: 'center' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: 800, color: stat.color }}>{stat.value}</div>
                    <div style={{ fontSize: '0.72rem', color: '#94A3B8' }}>{stat.label}</div>
                  </div>
                ))}
              </div>
              <p style={{ color: '#CBD5E1', fontSize: '0.9rem', lineHeight: 1.6 }}>{result.summary}</p>
            </div>
          </div>

          {result.bias_flags.length > 0 && (
            <div>
              <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'white', marginBottom: '14px' }}>Detected Patterns</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {result.bias_flags.map((flag, i) => (
                  <div key={i} style={{
                    background: 'rgba(255,255,255,0.025)',
                    border: `1px solid ${flag.color}33`,
                    borderLeft: `4px solid ${flag.color}`,
                    borderRadius: '12px', padding: '16px',
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '10px' }}>
                      <div>
                        <span style={{ fontSize: '0.72rem', textTransform: 'uppercase', color: flag.color, fontWeight: 700 }}>
                          {flag.label}
                        </span>
                        <div style={{ marginTop: '4px', display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                          {flag.intersectional_axes.slice(1).map(ax => (
                            <span key={ax} style={{ fontSize: '0.72rem', padding: '2px 8px', borderRadius: '100px', background: 'rgba(167,139,250,0.12)', color: '#C4B5FD', fontWeight: 600 }}>
                              ⟳ {AXIS_LABELS[ax]}
                            </span>
                          ))}
                        </div>
                      </div>
                      <span style={{ padding: '4px 12px', borderRadius: '6px', fontSize: '0.78rem', fontWeight: 700, background: severityBg(flag.severity), color: severityText(flag.severity), whiteSpace: 'nowrap' }}>
                        {severityLabel(flag.severity)}
                      </span>
                    </div>
                    <div style={{ background: 'rgba(239,68,68,0.08)', border: '1px solid rgba(239,68,68,0.2)', borderRadius: '8px', padding: '8px 12px', marginBottom: '10px', fontSize: '0.88rem', color: '#FCA5A5', fontFamily: 'monospace' }}>
                      "{flag.trigger_phrase}"
                    </div>
                    <p style={{ color: '#CBD5E1', fontSize: '0.88rem', lineHeight: 1.6, marginBottom: '8px' }}>{flag.explanation}</p>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '0.82rem' }}>
                      <div style={{ padding: '8px 12px', borderRadius: '8px', background: 'rgba(239,68,68,0.07)', border: '1px solid rgba(239,68,68,0.15)' }}>
                        <div style={{ color: '#94A3B8', marginBottom: '2px', fontSize: '0.72rem', textTransform: 'uppercase' }}>Affected</div>
                        <div style={{ color: '#FCA5A5' }}>{flag.harmed_demographic}</div>
                      </div>
                      <div style={{ padding: '8px 12px', borderRadius: '8px', background: 'rgba(34,197,94,0.07)', border: '1px solid rgba(34,197,94,0.15)' }}>
                        <div style={{ color: '#94A3B8', marginBottom: '2px', fontSize: '0.72rem', textTransform: 'uppercase' }}>Rewrite to</div>
                        <div style={{ color: '#86EFAC', fontStyle: 'italic' }}>"{flag.suggested_rewrite}"</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {result.matrix.length > 0 && (
            <div style={{ background: 'rgba(255,255,255,0.025)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '14px', padding: '20px', overflowX: 'auto' }}>
              <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'white', marginBottom: '12px' }}>Compound Bias Matrix</h3>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.8rem', minWidth: '500px' }}>
                <thead>
                  <tr>
                    <th style={{ padding: '8px', color: '#64748B', textAlign: 'left', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>×</th>
                    {AXES.map(ax => (
                      <th key={ax} style={{ padding: '8px 6px', color: '#94A3B8', fontWeight: 600, textAlign: 'center', borderBottom: '1px solid rgba(255,255,255,0.06)', fontSize: '0.75rem' }}>
                        {AXIS_LABELS[ax]}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {AXES.map(rowAx => (
                    <tr key={rowAx}>
                      <td style={{ padding: '8px', color: '#94A3B8', fontWeight: 600, borderRight: '1px solid rgba(255,255,255,0.06)', fontSize: '0.75rem' }}>
                        {AXIS_LABELS[rowAx]}
                      </td>
                      {AXES.map(colAx => {
                        if (rowAx === colAx) {
                          return <td key={colAx} style={{ padding: '6px', textAlign: 'center' }}>—</td>;
                        }
                        const cell = result.matrix.find(m => (m.axis_row === rowAx && m.axis_col === colAx) || (m.axis_row === colAx && m.axis_col === rowAx));
                        const score = cell?.score || 0;
                        return (
                          <td key={colAx} style={{ padding: '6px', textAlign: 'center' }}>
                            <div style={{ padding: '5px 4px', borderRadius: '6px', background: scoreBg(score), color: scoreText(score), fontWeight: score > 0 ? 700 : 400, fontSize: '0.8rem', cursor: score > 0 ? 'help' : 'default' }} title={cell?.compound_harm || ''}>
                              {score > 0 ? (score * 10).toFixed(1) : '·'}
                            </div>
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {result.bias_flags.length > 0 && (
            <div style={{ background: 'rgba(255,255,255,0.025)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '14px', padding: '20px' }}>
              <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'white', marginBottom: '16px' }}>Generate Inclusive Rewrite</h3>
              <button
                onClick={handleRewrite}
                disabled={rewriteLoading}
                style={{
                  width: '100%', padding: '12px', borderRadius: '9px', border: 'none',
                  background: rewriteLoading ? 'rgba(123,47,255,0.35)' : 'linear-gradient(135deg, #7B2FFF, #E91E8C)',
                  color: 'white', fontWeight: 700, fontSize: '0.95rem',
                  cursor: rewriteLoading ? 'not-allowed' : 'pointer',
                }}
              >
                {rewriteLoading ? 'Rewriting…' : 'Generate Inclusive JD'}
              </button>

              {rewriteResult && (
                <div style={{ marginTop: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  <div style={{ padding: '12px 16px', borderRadius: '9px', background: 'rgba(34,197,94,0.09)', border: '1px solid rgba(34,197,94,0.25)', color: '#86EFAC', fontSize: '0.9rem', fontWeight: 600 }}>
                    Score: {rewriteResult.original_bias_score?.toFixed(1)} → {rewriteResult.new_bias_score?.toFixed(1)} ({(rewriteResult.original_bias_score - rewriteResult.new_bias_score).toFixed(1)} reduction)
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
                    <div style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.07)', borderRadius: '12px', padding: '14px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                        <h4 style={{ color: 'white', fontWeight: 700, fontSize: '0.9rem' }}>Original</h4>
                        <span style={{ background: 'rgba(239,68,68,0.2)', color: '#FCA5A5', padding: '3px 8px', borderRadius: '5px', fontSize: '0.75rem', fontWeight: 700 }}>
                          {rewriteResult.original_bias_score?.toFixed(1)}
                        </span>
                      </div>
                      <p style={{ color: '#94A3B8', fontSize: '0.85rem', lineHeight: 1.6, maxHeight: '280px', overflowY: 'auto', whiteSpace: 'pre-wrap' }}>
                        {jdText}
                      </p>
                    </div>
                    <div style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(34,197,94,0.2)', borderRadius: '12px', padding: '14px' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                        <h4 style={{ color: 'white', fontWeight: 700, fontSize: '0.9rem' }}>Inclusive</h4>
                        <span style={{ background: 'rgba(34,197,94,0.2)', color: '#86EFAC', padding: '3px 8px', borderRadius: '5px', fontSize: '0.75rem', fontWeight: 700 }}>
                          {rewriteResult.new_bias_score?.toFixed(1)}
                        </span>
                      </div>
                      <p style={{ color: '#CBD5E1', fontSize: '0.85rem', lineHeight: 1.6, maxHeight: '280px', overflowY: 'auto', whiteSpace: 'pre-wrap' }}>
                        {rewriteResult.rewritten_jd}
                      </p>
                    </div>
                  </div>

                  {rewriteResult.changes.length > 0 && (
                    <div style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.07)', borderRadius: '12px', padding: '16px', overflowX: 'auto' }}>
                      <h4 style={{ color: 'white', fontWeight: 700, fontSize: '0.88rem', marginBottom: '12px' }}>Changes</h4>
                      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.83rem' }}>
                        <thead>
                          <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
                            <th style={{ padding: '8px', textAlign: 'left', color: '#64748B' }}>Original</th>
                            <th style={{ padding: '8px', textAlign: 'left', color: '#64748B' }}>Replacement</th>
                            <th style={{ padding: '8px', textAlign: 'left', color: '#64748B' }}>Type</th>
                          </tr>
                        </thead>
                        <tbody>
                          {rewriteResult.changes.map((c, i) => (
                            <tr key={i} style={{ borderBottom: '1px solid rgba(255,255,255,0.04)' }}>
                              <td style={{ padding: '8px', color: '#FCA5A5', fontFamily: 'monospace' }}>{c.original}</td>
                              <td style={{ padding: '8px', color: '#86EFAC' }}>{c.replacement}</td>
                              <td style={{ padding: '8px', color: '#94A3B8', fontSize: '0.8rem' }}>{c.reason}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}
