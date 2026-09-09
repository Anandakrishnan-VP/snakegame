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

  // On mount or when initialStandardId changes: check existing or prompt selection
  useEffect(() => {
    if (initialStandardId) {
      setSelectedStandard(initialStandardId);
      initJourney(initialStandardId, journeyType, true);
    } else {
      const cachedId = sessionStorage.getItem('active_journey_id');
      if (cachedId) {
        fetchExistingJourney(cachedId);
      }
      // If no cached journey and no initialStandardId, do NOT auto-load steel flasks!
    }
  }, [initialStandardId]);

  const fetchExistingJourney = async (id) => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/journey/${id}`);
      if (res.ok) {
        const data = await res.json();
        setJourney(data);
        if (data.standard_id) setSelectedStandard(data.standard_id);
        if (data.journey_type) setJourneyType(data.journey_type);
      } else {
        sessionStorage.removeItem('active_journey_id');
      }
    } catch (e) {
      console.error('Failed to restore journey:', e);
    } finally {
      setLoading(false);
    }
  };

  const initJourney = async (standardId, type, forceNew = false) => {
    setLoading(true);
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
        setJourney(data);
        sessionStorage.setItem('active_journey_id', data.journey_id);
        // Expand first pending step
        const firstPending = (data.steps || []).find((s) => s.status !== 'done');
        if (firstPending) {
          setExpandedSteps({ [firstPending.step_id]: true });
        }
      }
    } catch (e) {
      console.error('Failed to initialize journey:', e);
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
    initJourney(type === 'get_certified' ? selectedStandard : null, type, true);
  };

  const handleSelectStandard = (code) => {
    setSelectedStandard(code);
    initJourney(code, 'get_certified', true);
  };

  const handleCustomSubmit = (e) => {
    e.preventDefault();
    if (!customInput.trim()) return;
    setSelectedStandard(customInput.trim());
    initJourney(customInput.trim(), 'get_certified', true);
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
                color: '#fff',
                boxShadow: '0 4px 14px rgba(13, 148, 136, 0.25)'
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
                background: journeyType === 'get_certified' ? 'var(--accent-saffron)' : 'transparent',
                color: journeyType === 'get_certified' ? '#fff' : 'var(--text-secondary)',
                fontWeight: 600,
                fontSize: '0.82rem',
                cursor: 'pointer',
                transition: 'all 0.2s'
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
                background: journeyType === 'verify_protect' ? '#38bdf8' : 'transparent',
                color: journeyType === 'verify_protect' ? '#0f172a' : 'var(--text-secondary)',
                fontWeight: 600,
                fontSize: '0.82rem',
                cursor: 'pointer',
                transition: 'all 0.2s'
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
                      padding: '4px 10px',
                      borderRadius: '9999px',
                      border: '1px solid var(--border-subtle)',
                      background: selectedStandard === q.code ? 'rgba(249, 115, 22, 0.2)' : 'rgba(255, 255, 255, 0.04)',
                      color: selectedStandard === q.code ? 'var(--accent-saffron-light)' : 'var(--text-secondary)',
                      cursor: 'pointer',
                      fontWeight: selectedStandard === q.code ? 600 : 400
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
                    border: '1px solid var(--border-strong)',
                    borderRadius: '6px',
                    padding: '6px 10px',
                    color: 'var(--text-primary)',
                    fontSize: '0.78rem',
                    width: '190px',
                    outline: 'none'
                  }}
                />
                <button
                  type="submit"
                  style={{
                    background: 'var(--btn-secondary-bg)',
                    border: '1px solid var(--border-subtle)',
                    borderRadius: '6px',
                    color: 'var(--text-primary)',
                    padding: '6px 12px',
                    fontSize: '0.78rem',
                    cursor: 'pointer'
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
          <Loader2 size={32} color="var(--accent-saffron)" className="animate-spin" />
          <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Loading compliance roadmap and readiness metrics...</span>
        </div>
      ) : journey ? (
        <>
          {/* Readiness Score & Action Hero */}
          <div className="glass-panel" style={{
            padding: '24px 28px',
            background: 'var(--bg-card)',
            border: `1px solid ${scoreColor}40`,
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
                  boxShadow: `0 0 20px ${scoreColor}25`
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
                        background: metadata.qco_status.toLowerCase().includes('mandat') ? 'rgba(239, 68, 68, 0.15)' : 'rgba(34, 197, 94, 0.15)',
                        color: metadata.qco_status.toLowerCase().includes('mandat') ? '#f87171' : '#4ade80',
                        fontWeight: 700,
                        border: '1px solid currentColor'
                      }}>
                        {metadata.qco_status.toUpperCase()}
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
                    background: 'rgba(255, 255, 255, 0.06)',
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
                  className="glass-panel"
                  style={{
                    padding: '18px 22px',
                    borderLeft: `4px solid ${isDone ? '#22c55e' : 'var(--border-subtle)'}`,
                    background: isDone ? 'rgba(34, 197, 94, 0.05)' : 'var(--bg-card)',
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
                          color: isDone ? '#22c55e' : 'var(--text-muted)',
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
                          <Loader2 size={22} className="animate-spin" color="var(--accent-saffron)" />
                        ) : isDone ? (
                          <CheckCircle2 size={22} color="#22c55e" />
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
                            background: 'rgba(255, 255, 255, 0.08)',
                            color: 'var(--text-secondary)'
                          }}>
                            STEP {step.step_number}
                          </span>
                          <span style={{
                            fontSize: '0.98rem',
                            fontWeight: 600,
                            color: isDone ? '#e2e8f0' : '#fff',
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
                              background: 'rgba(0,0,0,0.2)',
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
                                    color: '#38bdf8',
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
            <div className="glass-panel" style={{ padding: '20px 24px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                <FlaskConical size={18} color="var(--accent-saffron)" />
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
        <div className="glass-panel" style={{ padding: '48px 32px', textAlign: 'center' }}>
          <div style={{
            width: '64px',
            height: '64px',
            borderRadius: '16px',
            background: 'rgba(249, 115, 22, 0.12)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--accent-saffron)',
            margin: '0 auto 18px'
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
                    e.currentTarget.style.borderColor = 'var(--accent-saffron)';
                    e.currentTarget.style.background = 'var(--accent-saffron-glow)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = 'var(--border-subtle)';
                    e.currentTarget.style.background = 'var(--bg-surface)';
                  }}
                >
                  <div style={{ fontSize: '0.72rem', color: '#f87171', fontWeight: 700, textTransform: 'uppercase' }}>
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
                  border: '1px solid var(--border-strong)',
                  borderRadius: '8px',
                  padding: '10px 14px',
                  color: 'var(--text-primary)',
                  fontSize: '0.88rem',
                  outline: 'none'
                }}
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
