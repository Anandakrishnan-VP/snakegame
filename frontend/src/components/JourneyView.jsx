import React, { useState, useEffect } from 'react';
import { 
  CheckCircle2, 
  Circle, 
  Download, 
  RotateCcw, 
  ExternalLink, 
  ShieldCheck, 
  Award, 
  Building2, 
  FlaskConical, 
  Clock, 
  FileText, 
  AlertCircle, 
  ArrowRight,
  ChevronDown,
  ChevronUp,
  Sparkles,
  Loader2
} from 'lucide-react';
import { API_BASE_URL } from '../api/config';

const QUICK_STANDARDS = [
  { code: 'IS 17803:2022', label: 'Steel Bottles (IS 17803)' },
  { code: 'IS 9873 (Part 1):2019', label: 'Toys Safety (IS 9873)' },
  { code: 'IS 4151:2015', label: 'Helmets (IS 4151)' },
  { code: 'IS 14543:2016', label: 'Drinking Water (IS 14543)' },
  { code: 'IS 16046 (Part 2):2018', label: 'Lithium Battery (CRS)' }
];

export default function JourneyView({ initialStandardId, currentLang = 'en', t = (k) => k }) {
  const [sessionId] = useState(() => {
    let sid = sessionStorage.getItem('bis_saathi_session_id');
    if (!sid) {
      sid = 'sess-' + Math.random().toString(36).substring(2, 9);
      sessionStorage.setItem('bis_saathi_session_id', sid);
    }
    return sid;
  });

  const [journeyType, setJourneyType] = useState('get_certified'); // 'get_certified' | 'verify_protect'
  const [selectedStandard, setSelectedStandard] = useState(initialStandardId || null);
  const [customInput, setCustomInput] = useState('');
  const [journey, setJourney] = useState(null);
  const [loading, setLoading] = useState(false);
  const [updatingStepId, setUpdatingStepId] = useState(null);
  const [expandedSteps, setExpandedSteps] = useState({ 'step-1': true });
  const [notFoundError, setNotFoundError] = useState(null);

  // On mount or when initialStandardId changes: check existing or load default template
  useEffect(() => {
    if (initialStandardId) {
      setSelectedStandard(initialStandardId);
      initJourney(initialStandardId, journeyType, true);
    } else {
      const cachedId = sessionStorage.getItem('active_journey_id');
      if (cachedId) {
        fetchExistingJourney(cachedId);
      } else {
        // Load default generic Scheme-I template for new users
        initJourney(null, 'get_certified', false);
      }
    }
  }, [initialStandardId]);

  const fetchExistingJourney = async (id) => {
    setLoading(true);
    setNotFoundError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/api/journey/${id}`);
      if (res.ok) {
        const data = await res.json();
        setJourney(data);
        if (data.standard_id) setSelectedStandard(data.standard_id);
        if (data.journey_type) setJourneyType(data.journey_type);
      } else {
        sessionStorage.removeItem('active_journey_id');
        initJourney(null, 'get_certified', false);
      }
    } catch (e) {
      console.error('Failed to restore journey:', e);
      initJourney(null, 'get_certified', false);
    } finally {
      setLoading(false);
    }
  };

  const initJourney = async (standardId, type, forceNew = false) => {
    setLoading(true);
    setNotFoundError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/api/journey/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          journey_type: type,
          standard_id: standardId || null,
          force_new: forceNew
        })
      });

      if (res.ok) {
        const data = await res.json();
        if (data.not_found) {
          setJourney(null);
          setNotFoundError({
            standardId: data.requested_standard || standardId,
            message: data.message || `No data found for Indian Standard "${standardId}".`,
            suggestion: data.suggestion || 'This standard is not currently available in our offline directory.'
          });
          sessionStorage.removeItem('active_journey_id');
        } else {
          setJourney(data);
          setNotFoundError(null);
          sessionStorage.setItem('active_journey_id', data.journey_id);
          // Expand first pending step
          const firstPending = (data.steps || []).find((s) => s.status !== 'done');
          if (firstPending) {
            setExpandedSteps({ [firstPending.step_id]: true });
          }
        }
      } else {
        const errData = await res.json().catch(() => ({}));
        setJourney(null);
        setNotFoundError({
          standardId: standardId,
          message: errData.detail || `No data found for standard "${standardId}".`,
          suggestion: 'Please verify the IS code or select from the supported standards below.'
        });
        sessionStorage.removeItem('active_journey_id');
      }
    } catch (e) {
      console.error('Failed to initialize journey:', e);
      setJourney(null);
      setNotFoundError({
        standardId: standardId,
        message: `Connection error loading standard "${standardId}".`,
        suggestion: 'Please check that the backend server is running.'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleToggleStep = async (stepId, currentStatus) => {
    if (!journey || updatingStepId) return;

    const newStatus = currentStatus === 'done' ? 'pending' : 'done';
    setUpdatingStepId(stepId);

    // Optimistic local update
    const prevSteps = [...journey.steps];
    const updatedSteps = prevSteps.map((s) => (s.step_id === stepId ? { ...s, status: newStatus } : s));
    const doneCount = updatedSteps.filter((s) => s.status === 'done').length;
    const optimisticScore = Math.round((doneCount / updatedSteps.length) * 100);

    setJourney((prev) => ({
      ...prev,
      steps: updatedSteps,
      readiness_score: optimisticScore
    }));

    try {
      const res = await fetch(`${API_BASE_URL}/api/journey/${journey.journey_id}/step/${stepId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      });

      if (res.ok) {
        const data = await res.json();
        setJourney(data);
      } else {
        // Rollback
        setJourney((prev) => ({ ...prev, steps: prevSteps }));
      }
    } catch (e) {
      console.error('Failed to update step:', e);
      setJourney((prev) => ({ ...prev, steps: prevSteps }));
    } finally {
      setUpdatingStepId(null);
    }
  };

  const toggleExpand = (stepId) => {
    setExpandedSteps((prev) => ({
      ...prev,
      [stepId]: !prev[stepId]
    }));
  };

  const handleDownloadPdf = () => {
    if (!journey) return;
    const url = `${API_BASE_URL}/api/journey/${journey.journey_id}/pdf`;
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `bis_saathi_roadmap_${journey.journey_id.slice(0, 8)}.pdf`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleSwitchType = (type) => {
    setJourneyType(type);
    setNotFoundError(null);
    if (type === 'verify_protect') {
      initJourney(null, type, true);
    } else {
      if (selectedStandard && !notFoundError) {
        initJourney(selectedStandard, type, true);
      } else {
        setJourney(null);
      }
    }
  };

  const handleSelectStandard = (code) => {
    setSelectedStandard(code);
    setNotFoundError(null);
    initJourney(code, 'get_certified', true);
  };

  const handleCustomSubmit = (e) => {
    e.preventDefault();
    if (!customInput.trim()) return;
    const val = customInput.trim();
    setSelectedStandard(val);
    setNotFoundError(null);
    initJourney(val, 'get_certified', true);
    setCustomInput('');
  };

  const score = journey?.readiness_score || 0;
  const scoreColor = score >= 80 ? '#22c55e' : score >= 40 ? '#f59e0b' : 'var(--accent-saffron)';
  const metadata = journey?.metadata || {};

  return (
    <div style={{ maxWidth: '1080px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header & Mode Switcher */}
      <div className="glass-panel" style={{ padding: '24px 28px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{
                width: '38px',
                height: '38px',
                borderRadius: '10px',
                background: 'linear-gradient(135deg, #111315 0%, #0d9488 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#ffffff',
                boxShadow: '0 4px 12px rgba(13, 148, 136, 0.25)'
              }}>
                <Award size={22} />
              </div>
              <div>
                <h2 style={{ margin: 0, fontSize: '1.4rem', color: 'var(--text-primary)', fontWeight: 700 }}>
                  {t('tab_journey') || 'Certification Journey & Compliance Roadmap'}
                </h2>
                <p style={{ margin: '2px 0 0', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                  Interactive step-by-step readiness wizard with live percentage and downloadable PDF roadmap.
                </p>
              </div>
            </div>
          </div>

          {/* Journey Type Toggle */}
          <div style={{
            display: 'flex',
            background: 'var(--bg-surface)',
            padding: '4px',
            borderRadius: '10px',
            border: '1px solid var(--border-subtle)'
          }}>
            <button
              onClick={() => handleSwitchType('get_certified')}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '8px 16px',
                borderRadius: '8px',
                border: 'none',
                background: journeyType === 'get_certified' ? 'var(--btn-primary-bg)' : 'transparent',
                color: journeyType === 'get_certified' ? 'var(--btn-primary-text)' : 'var(--text-secondary)',
                fontWeight: 600,
                fontSize: '0.82rem',
                cursor: 'pointer',
                transition: 'all 0.2s',
                boxShadow: journeyType === 'get_certified' ? '0 2px 8px rgba(17, 19, 21, 0.2)' : 'none'
              }}
            >
              <Building2 size={15} />
              <span>Get Certified (MSME)</span>
            </button>
            <button
              onClick={() => handleSwitchType('verify_protect')}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '8px 16px',
                borderRadius: '8px',
                border: 'none',
                background: journeyType === 'verify_protect' ? 'var(--accent-aqua)' : 'transparent',
                color: journeyType === 'verify_protect' ? '#ffffff' : 'var(--text-secondary)',
                fontWeight: 600,
                fontSize: '0.82rem',
                cursor: 'pointer',
                transition: 'all 0.2s',
                boxShadow: journeyType === 'verify_protect' ? '0 2px 8px var(--accent-aqua-glow)' : 'none'
              }}
            >
              <ShieldCheck size={15} />
              <span>Verify & Protect (Consumer)</span>
            </button>
          </div>
        </div>

        {/* Quick Standard Selection (Only for get_certified) */}
        {journeyType === 'get_certified' && (
          <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid var(--border-subtle)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Quick Standards:</span>
                {QUICK_STANDARDS.map((q) => (
                  <button
                    key={q.code}
                    onClick={() => handleSelectStandard(q.code)}
                    style={{
                      fontSize: '0.76rem',
                      padding: '4px 12px',
                      borderRadius: '9999px',
                      border: '1px solid',
                      borderColor: selectedStandard === q.code ? 'var(--border-active)' : 'var(--border-subtle)',
                      background: selectedStandard === q.code ? 'rgba(13, 148, 136, 0.14)' : 'var(--bg-surface)',
                      color: selectedStandard === q.code ? 'var(--accent-aqua)' : 'var(--text-secondary)',
                      cursor: 'pointer',
                      fontWeight: selectedStandard === q.code ? 600 : 500,
                      transition: 'all 0.15s'
                    }}
                  >
                    {q.label}
                  </button>
                ))}
              </div>

              {/* Custom Standard Input */}
              <form onSubmit={handleCustomSubmit} style={{ display: 'flex', gap: '6px' }}>
                <input
                  type="text"
                  placeholder="Or enter IS code (e.g. IS 269)..."
                  value={customInput}
                  onChange={(e) => setCustomInput(e.target.value)}
                  style={{
                    background: 'var(--bg-input)',
                    border: '1px solid var(--border-subtle)',
                    borderRadius: '6px',
                    padding: '6px 10px',
                    color: 'var(--text-primary)',
                    fontSize: '0.78rem',
                    width: '190px',
                    outline: 'none',
                    transition: 'border-color 0.2s'
                  }}
                  onFocus={(e) => { e.currentTarget.style.borderColor = 'var(--accent-aqua)'; }}
                  onBlur={(e) => { e.currentTarget.style.borderColor = 'var(--border-subtle)'; }}
                />
                <button
                  type="submit"
                  className="btn-primary"
                  style={{
                    padding: '6px 14px',
                    fontSize: '0.78rem'
                  }}
                >
                  Load
                </button>
              </form>
            </div>
          </div>
        )}
      </div>

      {loading ? (
        <div style={{ padding: '60px 0', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '14px' }}>
          <Loader2 size={32} color="var(--accent-aqua)" className="animate-spin" />
          <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Loading compliance roadmap and readiness metrics...</span>
        </div>
      ) : notFoundError ? (
        <div className="glass-panel" style={{
          padding: '36px 32px',
          background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(15, 23, 42, 0.95) 100%)',
          border: '1px solid rgba(239, 68, 68, 0.35)',
          borderRadius: '16px',
          boxShadow: '0 12px 40px rgba(239, 68, 68, 0.12)'
        }}>
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '20px', flexWrap: 'wrap' }}>
            <div style={{
              width: '56px',
              height: '56px',
              borderRadius: '14px',
              background: 'rgba(239, 68, 68, 0.18)',
              border: '1px solid rgba(239, 68, 68, 0.4)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#f87171',
              flexShrink: 0
            }}>
              <AlertCircle size={30} />
            </div>

            <div style={{ flex: 1, minWidth: '280px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
                <h3 style={{ margin: 0, fontSize: '1.3rem', color: 'var(--text-primary)', fontWeight: 700 }}>
                  No Data Found for "{notFoundError.standardId}"
                </h3>
                <span style={{
                  fontSize: '0.72rem',
                  padding: '2px 8px',
                  borderRadius: '4px',
                  background: 'rgba(239, 68, 68, 0.2)',
                  color: '#f87171',
                  fontWeight: 700,
                  border: '1px solid rgba(239, 68, 68, 0.4)'
                }}>
                  STANDARD NOT IN DATABASE
                </span>
              </div>

              <p style={{ margin: '10px 0 0', fontSize: '0.92rem', color: 'var(--text-primary)', lineHeight: 1.55 }}>
                {notFoundError.message}
              </p>
              <p style={{ margin: '8px 0 0', fontSize: '0.84rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                {notFoundError.suggestion}
              </p>

              {/* Action Buttons */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginTop: '20px', flexWrap: 'wrap' }}>
                <a
                  href="https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/indian_standards/isdetails"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-primary"
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '10px 18px',
                    fontSize: '0.85rem',
                    textDecoration: 'none',
                    borderRadius: '8px'
                  }}
                >
                  <ExternalLink size={16} />
                  <span>Search Official BIS Portal</span>
                </a>

                <button
                  onClick={() => {
                    setNotFoundError(null);
                    setSelectedStandard(null);
                  }}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '10px 18px',
                    fontSize: '0.85rem',
                    borderRadius: '8px',
                    background: 'var(--bg-surface)',
                    border: '1px solid var(--border-subtle)',
                    color: 'var(--text-primary)',
                    cursor: 'pointer'
                  }}
                >
                  <span>Browse Supported Standards</span>
                </button>
              </div>
            </div>
          </div>

          {/* Supported standards quick chooser */}
          <div style={{ marginTop: '28px', paddingTop: '20px', borderTop: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '12px' }}>
              Or choose one of our verified, fully-mapped Indian Standards:
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px' }}>
              {[
                { code: 'IS 17803:2022', title: 'Stainless Steel Flasks' },
                { code: 'IS 9873 (Part 1):2019', title: 'Toys Safety' },
                { code: 'IS 4151:2015', title: 'Helmets' },
                { code: 'IS 14543:2016', title: 'Packaged Drinking Water' },
                { code: 'IS 16046 (Part 2):2018', title: 'Lithium Battery' },
                { code: 'IS 269:2015', title: 'Portland Cement' }
              ].map((item) => (
                <button
                  key={item.code}
                  onClick={() => handleSelectStandard(item.code)}
                  style={{
                    padding: '12px 14px',
                    borderRadius: '8px',
                    background: 'var(--bg-surface)',
                    border: '1px solid var(--border-subtle)',
                    textAlign: 'left',
                    cursor: 'pointer',
                    color: 'var(--text-primary)',
                    transition: 'all 0.2s'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = 'var(--accent-aqua)';
                    e.currentTarget.style.background = 'var(--bg-card-hover)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = 'var(--border-subtle)';
                    e.currentTarget.style.background = 'var(--bg-surface)';
                  }}
                >
                  <div style={{ fontWeight: 600, fontSize: '0.84rem', color: 'var(--text-primary)' }}>{item.title}</div>
                  <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '2px', fontFamily: 'JetBrains Mono' }}>{item.code}</div>
                </button>
              ))}
            </div>
          </div>
        </div>
      ) : journey ? (
        <>
          {/* Prominent Call to Action Banner when viewing Default Template */}
          {(metadata.is_default_template || journey.standard_id === 'Scheme-I Template') ? (
            <div className="glass-panel" style={{
              padding: '20px 24px',
              background: 'linear-gradient(135deg, rgba(13, 148, 136, 0.12) 0%, var(--bg-surface) 100%)',
              border: '1px solid rgba(13, 148, 136, 0.35)',
              borderRadius: '14px',
              boxShadow: 'var(--shadow-card)'
            }}>
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '16px', flexWrap: 'wrap' }}>
                <div style={{ flex: 1, minWidth: '280px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                    <Sparkles size={20} color="var(--accent-aqua)" />
                    <span style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                      Showing Default Scheme-I Template • Choose Your Own Indian Standard (ISI)
                    </span>
                  </div>
                  <p style={{ margin: 0, fontSize: '0.86rem', color: 'var(--text-secondary)', lineHeight: 1.55 }}>
                    You are currently viewing the <b>general Scheme-I certification sequence</b>. Select your product below or enter an IS code to customize the milestones, mandatory Quality Control Orders (QCOs), and testing laboratories for your business.
                  </p>
                </div>
              </div>

              {/* Prominent Quick Selection Chips & Input */}
              <div style={{ marginTop: '16px', paddingTop: '14px', borderTop: '1px solid var(--border-subtle)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                  <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>
                    Select Your Product:
                  </span>
                  {QUICK_STANDARDS.map((q) => (
                    <button
                      key={q.code}
                      onClick={() => handleSelectStandard(q.code)}
                      style={{
                        fontSize: '0.78rem',
                        padding: '6px 12px',
                        borderRadius: '9999px',
                        border: '1px solid rgba(13, 148, 136, 0.35)',
                        background: 'rgba(13, 148, 136, 0.1)',
                        color: 'var(--accent-aqua)',
                        cursor: 'pointer',
                        fontWeight: 600,
                        transition: 'all 0.15s'
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.background = 'var(--accent-aqua)';
                        e.currentTarget.style.color = '#ffffff';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.background = 'rgba(13, 148, 136, 0.1)';
                        e.currentTarget.style.color = 'var(--accent-aqua)';
                      }}
                    >
                      {q.label}
                    </button>
                  ))}
                </div>

                <form onSubmit={handleCustomSubmit} style={{ display: 'flex', gap: '6px' }}>
                  <input
                    type="text"
                    placeholder="Enter IS code (e.g. IS 269)..."
                    value={customInput}
                    onChange={(e) => setCustomInput(e.target.value)}
                    style={{
                      background: 'var(--bg-input)',
                      border: '1px solid var(--border-subtle)',
                      borderRadius: '6px',
                      padding: '6px 10px',
                      color: 'var(--text-primary)',
                      fontSize: '0.78rem',
                      width: '180px',
                      outline: 'none',
                      transition: 'border-color 0.2s'
                    }}
                    onFocus={(e) => { e.currentTarget.style.borderColor = 'var(--accent-aqua)'; }}
                    onBlur={(e) => { e.currentTarget.style.borderColor = 'var(--border-subtle)'; }}
                  />
                  <button
                    type="submit"
                    className="btn-primary"
                    style={{ padding: '6px 12px', fontSize: '0.78rem' }}
                  >
                    Customize
                  </button>
                </form>
              </div>
            </div>
          ) : (
            /* Active Standard Indicator when user selected their own standard */
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '10px 16px',
              borderRadius: '8px',
              background: 'var(--bg-surface)',
              border: '1px solid var(--border-subtle)',
              fontSize: '0.82rem',
              color: 'var(--text-secondary)'
            }}>
              <div>
                Active Standard: <b style={{ color: 'var(--text-primary)' }}>{journey.standard_id}</b> ({metadata.title})
              </div>
              <button
                onClick={() => {
                  setSelectedStandard(null);
                  sessionStorage.removeItem('active_journey_id');
                  initJourney(null, 'get_certified', true);
                }}
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--accent-aqua)',
                  cursor: 'pointer',
                  fontSize: '0.78rem',
                  fontWeight: 600,
                  textDecoration: 'underline'
                }}
              >
                Reset to Default Template
              </button>
            </div>
          )}

          {/* Readiness Score & Action Hero */}
          <div className="glass-card" style={{
            padding: '24px 28px',
            background: 'var(--bg-card)',
            border: `1px solid var(--border-subtle)`,
            boxShadow: 'var(--shadow-card)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '20px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                {/* Score Dial / Badge */}
                <div style={{
                  width: '84px',
                  height: '84px',
                  borderRadius: '50%',
                  background: 'var(--bg-surface)',
                  border: `4px solid ${scoreColor}`,
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: `0 0 16px ${scoreColor}25`
                }}>
                  <span style={{ fontSize: '1.7rem', fontWeight: 800, color: scoreColor, lineHeight: 1 }}>
                    {score}%
                  </span>
                  <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginTop: '2px' }}>
                    Ready
                  </span>
                </div>

                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                      {metadata.title || journey.standard_id || 'Compliance Journey'}
                    </span>
                    {metadata.qco_status && (
                      <span style={{
                        fontSize: '0.72rem',
                        padding: '2px 8px',
                        borderRadius: '4px',
                        background: (metadata.is_default_template || journey.standard_id === 'Scheme-I Template')
                          ? 'rgba(13, 148, 136, 0.14)'
                          : metadata.qco_status.toLowerCase().includes('mandat') 
                            ? 'rgba(239, 68, 68, 0.15)' 
                            : 'rgba(34, 197, 94, 0.15)',
                        color: (metadata.is_default_template || journey.standard_id === 'Scheme-I Template')
                          ? 'var(--accent-aqua)'
                          : metadata.qco_status.toLowerCase().includes('mandat') 
                            ? '#f87171' 
                            : '#059669',
                        fontWeight: 700,
                        border: '1px solid currentColor'
                      }}>
                        {(metadata.is_default_template || journey.standard_id === 'Scheme-I Template') ? 'DEFAULT TEMPLATE' : metadata.qco_status.toUpperCase()}
                      </span>
                    )}
                  </div>
                  <p style={{ margin: '4px 0 0', fontSize: '0.84rem', color: 'var(--text-secondary)' }}>
                    <b>{journey.scheme}</b> • {journey.steps?.filter((s) => s.status === 'done').length} of {journey.steps?.length} milestones achieved • Free-form sequence
                  </p>
                </div>
              </div>

              {/* Action Buttons */}
              <div style={{ display: 'flex', gap: '10px' }}>
                <button
                  onClick={handleDownloadPdf}
                  className="btn-primary"
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '10px 18px',
                    fontSize: '0.88rem'
                  }}
                  title="Download clean 1-page printable compliance roadmap"
                >
                  <Download size={16} />
                  <span>Download Roadmap PDF</span>
                </button>

                <button
                  onClick={() => initJourney(selectedStandard, journeyType, true)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                    padding: '10px 14px',
                    borderRadius: '8px',
                    background: 'var(--bg-surface)',
                    border: '1px solid var(--border-subtle)',
                    color: 'var(--text-secondary)',
                    cursor: 'pointer',
                    fontSize: '0.85rem'
                  }}
                  title="Reset journey checklist"
                >
                  <RotateCcw size={15} />
                </button>
              </div>
            </div>

            {/* Progress Bar */}
            <div style={{ marginTop: '18px', width: '100%', height: '8px', background: 'var(--bg-surface)', borderRadius: '9999px', overflow: 'hidden' }}>
              <div style={{
                width: `${score}%`,
                height: '100%',
                background: scoreColor,
                borderRadius: '9999px',
                transition: 'width 0.4s ease'
              }} />
            </div>
          </div>

          {/* Stepper Checklist */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 4px' }}>
              <h3 style={{ margin: 0, fontSize: '1.05rem', color: 'var(--text-primary)', fontWeight: 600 }}>
                Compliance & Certification Milestones
              </h3>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                Check off items as your factory or team completes them:
              </span>
            </div>

            {(journey.steps || []).map((step, idx) => {
              const isDone = step.status === 'done';
              const isExpanded = !!expandedSteps[step.step_id];
              const isUpdating = updatingStepId === step.step_id;

              return (
                <div
                  key={step.step_id}
                  className="glass-card"
                  style={{
                    padding: '18px 22px',
                    borderLeft: `4px solid ${isDone ? '#059669' : 'var(--border-subtle)'}`,
                    background: isDone ? 'rgba(5, 150, 105, 0.05)' : 'var(--bg-card)',
                    transition: 'all 0.2s ease'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '14px' }}>
                    {/* Checkbox and Title */}
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '14px', flex: 1 }}>
                      <button
                        onClick={() => handleToggleStep(step.step_id, step.status)}
                        disabled={isUpdating}
                        style={{
                          background: 'transparent',
                          border: 'none',
                          color: isDone ? '#059669' : 'var(--text-muted)',
                          cursor: isUpdating ? 'wait' : 'pointer',
                          padding: 0,
                          marginTop: '2px',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          transition: 'transform 0.15s'
                        }}
                        title={isDone ? 'Mark as pending' : 'Mark as completed'}
                      >
                        {isUpdating ? (
                          <Loader2 size={22} className="animate-spin" color="var(--accent-aqua)" />
                        ) : isDone ? (
                          <CheckCircle2 size={22} color="#059669" />
                        ) : (
                          <Circle size={22} color="var(--text-muted)" />
                        )}
                      </button>

                      <div style={{ flex: 1 }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
                          <span style={{
                            fontSize: '0.72rem',
                            fontWeight: 700,
                            padding: '1px 6px',
                            borderRadius: '4px',
                            background: 'var(--bg-surface)',
                            color: 'var(--text-secondary)'
                          }}>
                            STEP {step.step_number}
                          </span>
                          <span style={{
                            fontSize: '0.98rem',
                            fontWeight: 600,
                            color: isDone ? 'var(--text-muted)' : 'var(--text-primary)',
                            textDecoration: isDone ? 'line-through' : 'none'
                          }}>
                            {step.title}
                          </span>

                          {step.indicative_timeline && (
                            <span style={{
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: '4px',
                              fontSize: '0.72rem',
                              color: 'var(--text-muted)',
                              background: 'var(--bg-surface)',
                              padding: '2px 8px',
                              borderRadius: '9999px'
                            }}>
                              <Clock size={11} /> {step.indicative_timeline}
                            </span>
                          )}
                        </div>

                        {/* Collapsed snippet or full view */}
                        {isExpanded ? (
                          <div style={{ marginTop: '10px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                            <p style={{ margin: 0, fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.55 }}>
                              {step.description}
                            </p>

                            {step.source_ref && (
                              <div style={{ marginTop: '4px' }}>
                                <a
                                  href={step.source_ref}
                                  target="_blank"
                                  rel="noreferrer"
                                  style={{
                                    fontSize: '0.76rem',
                                    color: 'var(--accent-aqua)',
                                    textDecoration: 'none',
                                    display: 'inline-flex',
                                    alignItems: 'center',
                                    gap: '4px'
                                  }}
                                >
                                  <ExternalLink size={12} /> Official Portal Reference
                                </a>
                              </div>
                            )}
                          </div>
                        ) : (
                          <p style={{ margin: '4px 0 0', fontSize: '0.82rem', color: 'var(--text-muted)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: '680px' }}>
                            {step.description}
                          </p>
                        )}
                      </div>
                    </div>

                    {/* Expand/Collapse Chevron */}
                    <button
                      onClick={() => toggleExpand(step.step_id)}
                      style={{
                        background: 'transparent',
                        border: 'none',
                        color: 'var(--text-muted)',
                        cursor: 'pointer',
                        padding: '4px'
                      }}
                    >
                      {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Matched Accredited Testing Facilities */}
          {metadata.labs && metadata.labs.length > 0 && (
            <div className="glass-card" style={{ padding: '20px 24px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                <FlaskConical size={18} color="var(--accent-aqua)" />
                <h4 style={{ margin: 0, fontSize: '0.95rem', color: 'var(--text-primary)' }}>
                  Accredited Testing Facilities Mapped to {journey.standard_id}
                </h4>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '12px' }}>
                {metadata.labs.map((lab, i) => (
                  <div key={i} style={{ padding: '12px 14px', background: 'var(--bg-surface)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
                    <div style={{ fontWeight: 600, fontSize: '0.85rem', color: 'var(--text-primary)' }}>{lab.name}</div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '3px' }}>
                      City: <b>{lab.city}</b> • Contact: {lab.phone}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      ) : (
        /* Welcome / Selection Empty State */
        <div className="glass-card" style={{ padding: '48px 32px', textAlign: 'center' }}>
          <div style={{
            width: '64px',
            height: '64px',
            borderRadius: '16px',
            background: 'rgba(13, 148, 136, 0.12)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--accent-aqua)',
            margin: '0 auto 18px',
            border: '1px solid rgba(13, 148, 136, 0.28)'
          }}>
            <Award size={32} />
          </div>

          <h3 style={{ margin: 0, fontSize: '1.3rem', color: 'var(--text-primary)', fontWeight: 700 }}>
            {journeyType === 'get_certified' ? 'Select a Product or Standard to Begin' : 'Enter a Licence or Hallmark to Verify'}
          </h3>
          <p style={{ margin: '8px auto 24px', fontSize: '0.9rem', color: 'var(--text-secondary)', maxWidth: '560px', lineHeight: 1.5 }}>
            {journeyType === 'get_certified' 
              ? 'Choose one of the common Indian Standards below, type an IS code into the search box above, or ask about your product in the Chat tab and click "Start My Certification Journey".'
              : 'Track the step-by-step verification, licensee scope audit, and authenticity confirmation for consumer protection.'}
          </p>

          {journeyType === 'get_certified' ? (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '14px', maxWidth: '780px', margin: '0 auto' }}>
              {[
                { code: 'IS 9873 (Part 1):2019', title: 'Children Toys Safety', qco: 'Mandatory QCO' },
                { code: 'IS 4151:2015', title: 'Two-Wheeler Helmets', qco: 'Mandatory QCO' },
                { code: 'IS 14543:2016', title: 'Packaged Drinking Water', qco: 'Mandatory QCO' },
                { code: 'IS 17803:2022', title: 'Stainless Steel Flasks', qco: 'Mandatory QCO' },
                { code: 'IS 16046 (Part 2):2018', title: 'Lithium Battery Cells', qco: 'CRS Mandatory' },
                { code: 'IS 1786:2008', title: 'TMT Steel Rebars', qco: 'Mandatory QCO' }
              ].map((item) => (
                <button
                  key={item.code}
                  onClick={() => handleSelectStandard(item.code)}
                  style={{
                    padding: '16px',
                    borderRadius: '10px',
                    background: 'var(--bg-surface)',
                    border: '1px solid var(--border-subtle)',
                    textAlign: 'left',
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    color: 'var(--text-primary)'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = 'var(--accent-aqua)';
                    e.currentTarget.style.background = 'var(--bg-card-hover)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = 'var(--border-subtle)';
                    e.currentTarget.style.background = 'var(--bg-surface)';
                  }}
                >
                  <div style={{ fontSize: '0.72rem', color: '#dc2626', fontWeight: 700, textTransform: 'uppercase' }}>
                    {item.qco}
                  </div>
                  <div style={{ fontWeight: 600, fontSize: '0.92rem', color: 'var(--text-primary)', marginTop: '4px' }}>
                    {item.title}
                  </div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '2px', fontFamily: 'JetBrains Mono' }}>
                    {item.code}
                  </div>
                </button>
              ))}
            </div>
          ) : (
            <div style={{ maxWidth: '420px', margin: '0 auto', display: 'flex', gap: '8px' }}>
              <input
                type="text"
                placeholder="Enter CM/L (e.g. 1234567) or HUID (e.g. AB1234)..."
                value={customInput}
                onChange={(e) => setCustomInput(e.target.value)}
                style={{
                  flex: 1,
                  background: 'var(--bg-input)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '8px',
                  padding: '10px 14px',
                  color: 'var(--text-primary)',
                  fontSize: '0.88rem',
                  outline: 'none',
                  transition: 'border-color 0.2s'
                }}
                onFocus={(e) => { e.currentTarget.style.borderColor = 'var(--accent-aqua)'; }}
                onBlur={(e) => { e.currentTarget.style.borderColor = 'var(--border-subtle)'; }}
              />
              <button
                onClick={() => {
                  if (customInput.trim()) {
                    initJourney(customInput.trim(), 'verify_protect', true);
                  }
                }}
                className="btn-primary"
                style={{ padding: '10px 18px', fontSize: '0.85rem' }}
              >
                Start Verification
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
