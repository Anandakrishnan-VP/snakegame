import React, { useState } from 'react';
import { ShieldCheck, ShieldAlert, Search, Award, CheckCircle, AlertTriangle, Building, Calendar, Info } from 'lucide-react';

export default function VerificationPanel({ currentLang = 'en', t = (k) => k }) {
  const [code, setCode] = useState('');
  const [activeTab, setActiveTab] = useState('CML');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const sampleCodes = {
    CML: [
      { code: 'CML1234567', label: 'Milton Vacuum Flasks (Active)' },
      { code: 'CML7654321', label: 'Steelbird Helmets (Active)' },
      { code: 'CML9988776', label: 'AquaPure Water (Suspended Test)' }
    ],
    HUID: [
      { code: 'AB1234', label: 'Tanishq 22K 916 Gold Necklace' },
      { code: 'XY9876', label: 'Kalyan 18K 750 Gold Ring' },
      { code: 'K7M2P9', label: 'Malabar 22K 916 Bangle' }
    ],
    CRS: [
      { code: 'R-41001234', label: 'Samsung Li-ion Battery Pack' },
      { code: 'R-41005678', label: 'Xiaomi 20000mAh Power Bank' }
    ]
  };

  const handleVerify = async (codeToVerify) => {
    const targetCode = codeToVerify || code;
    if (!targetCode.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch('http://localhost:8000/api/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: targetCode })
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({
        found: false,
        message: 'Unable to connect to verification server. Please ensure backend is running.'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '850px', margin: '0 auto', padding: '10px' }}>
      {/* Title */}
      <div style={{ textAlign: 'center', marginBottom: '24px' }}>
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          padding: '6px 14px',
          background: 'rgba(249, 115, 22, 0.12)',
          borderRadius: '9999px',
          color: 'var(--accent-saffron)',
          fontSize: '0.85rem',
          fontWeight: 600,
          marginBottom: '12px'
        }}>
          <ShieldCheck size={16} /> {t('verify_title')}
        </div>
        <h2 style={{ fontSize: '2rem', margin: '0 0 8px 0', color: '#fff' }}>
          {t('verify_title')}
        </h2>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto', fontSize: '0.95rem' }}>
          {t('verify_subtitle')}
        </p>
      </div>

      {/* Tabs */}
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        gap: '10px',
        marginBottom: '20px'
      }}>
        {[
          { id: 'CML', label: 'ISI Mark (CM/L)' },
          { id: 'HUID', label: 'Gold Hallmark (HUID)' },
          { id: 'CRS', label: 'Electronics (CRS R-No)' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => {
              setActiveTab(tab.id);
              setCode('');
              setResult(null);
            }}
            style={{
              padding: '10px 20px',
              borderRadius: '10px',
              border: '1px solid',
              borderColor: activeTab === tab.id ? 'var(--accent-saffron)' : 'var(--border-subtle)',
              background: activeTab === tab.id ? 'rgba(249, 115, 22, 0.15)' : 'rgba(255, 255, 255, 0.03)',
              color: activeTab === tab.id ? 'var(--accent-saffron)' : 'var(--text-secondary)',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Search Input Card */}
      <div className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
        <form onSubmit={(e) => { e.preventDefault(); handleVerify(); }}>
          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
            <div style={{ flex: '1 1 300px', position: 'relative' }}>
              <input
                type="text"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder={t('verify_placeholder')}
                style={{
                  width: '100%',
                  padding: '14px 18px',
                  backgroundColor: 'var(--bg-input)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '10px',
                  color: '#fff',
                  fontSize: '1rem',
                  fontFamily: 'JetBrains Mono',
                  outline: 'none'
                }}
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="btn-primary"
              style={{ padding: '14px 28px', fontSize: '1rem' }}
            >
              <Search size={18} /> {loading ? 'Verifying...' : t('verify_btn')}
            </button>
          </div>
        </form>

        {/* Preset Samples */}
        <div style={{ marginTop: '16px', display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{t('verify_samples')}</span>
          {sampleCodes[activeTab].map((s) => (
            <button
              key={s.code}
              onClick={() => {
                setCode(s.code);
                handleVerify(s.code);
              }}
              style={{
                fontSize: '0.78rem',
                padding: '4px 10px',
                background: 'rgba(255, 255, 255, 0.05)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '6px',
                color: 'var(--text-secondary)',
                cursor: 'pointer'
              }}
            >
              {s.label} ({s.code})
            </button>
          ))}
        </div>
      </div>

      {/* Result Certificate Card */}
      {result && (
        <div className="glass-panel animate-fade-in" style={{ padding: '24px', borderLeft: result.found ? '4px solid #10b981' : '4px solid #ef4444' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px', marginBottom: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              {result.found ? (
                <div style={{
                  width: '44px',
                  height: '44px',
                  borderRadius: '50%',
                  background: 'rgba(16, 185, 129, 0.15)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#34d399'
                }}>
                  <CheckCircle size={26} />
                </div>
              ) : (
                <div style={{
                  width: '44px',
                  height: '44px',
                  borderRadius: '50%',
                  background: 'rgba(239, 68, 68, 0.15)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#f87171'
                }}>
                  <AlertTriangle size={26} />
                </div>
              )}
              <div>
                <h3 style={{ margin: 0, fontSize: '1.25rem', color: '#fff' }}>
                  {result.found ? 'Verified Genuine Licence Record' : 'Record Not Found / Unregistered'}
                </h3>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                  Identifier: <strong style={{ color: '#38bdf8', fontFamily: 'JetBrains Mono' }}>{result.extracted_code || code}</strong> ({result.code_type || activeTab})
                </span>
              </div>
            </div>

            {result.status && (
              <span className={result.status === 'Active' || result.status === 'Operative' ? 'badge-confirmed' : 'badge-not-determined'} style={{
                padding: '6px 14px',
                borderRadius: '9999px',
                fontSize: '0.85rem',
                fontWeight: 700
              }}>
                {result.status.toUpperCase()}
              </span>
            )}
          </div>

          {result.found ? (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginTop: '16px' }}>
              <div style={{ padding: '12px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Registered Licensee</span>
                <p style={{ margin: '4px 0 0', fontWeight: 600, color: '#fff' }}>{result.licensee_name}</p>
                {result.brand && <span style={{ fontSize: '0.8rem', color: 'var(--accent-saffron)' }}>Brand: {result.brand}</span>}
              </div>

              <div style={{ padding: '12px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Product Category & Standard</span>
                <p style={{ margin: '4px 0 0', fontWeight: 600, color: '#fff' }}>{result.product_category}</p>
                {result.is_code && <span style={{ fontSize: '0.8rem', color: '#38bdf8', fontFamily: 'JetBrains Mono' }}>{result.is_code}</span>}
              </div>

              <div style={{ padding: '12px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Validity Schedule</span>
                <p style={{ margin: '4px 0 0', fontWeight: 600, color: '#fff' }}>{result.validity_date}</p>
              </div>

              <div style={{ padding: '12px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px', gridColumn: '1 / -1' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Official Registry Details</span>
                <p style={{ margin: '4px 0 0', fontSize: '0.9rem', color: '#cbd5e1' }}>{result.details}</p>
              </div>
            </div>
          ) : (
            <div style={{ padding: '16px', backgroundColor: 'rgba(239, 68, 68, 0.08)', borderRadius: '8px', marginTop: '12px' }}>
              <p style={{ margin: 0, color: '#fca5a5', fontSize: '0.92rem' }}>
                {result.message}
              </p>
              <div style={{ marginTop: '10px', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Tip: Consumer complaints against fraudulent marks can be submitted through the official BIS Care App or www.manakonline.in.
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
