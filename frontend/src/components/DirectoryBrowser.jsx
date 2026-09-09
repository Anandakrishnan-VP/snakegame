import React, { useState, useEffect } from 'react';
import { BookOpen, Search, ExternalLink, ShieldCheck, Tag, ArrowRight } from 'lucide-react';
import { API_BASE_URL } from '../api/config';

export default function DirectoryBrowser({ onSelectStandard, currentLang = 'en', t = (k) => k }) {
  const [standards, setStandards] = useState([]);
  const [search, setSearch] = useState('');
  const [division, setDivision] = useState('');
  const [loading, setLoading] = useState(false);

  const divisions = [
    'All Divisions',
    'Consumer Products',
    'Electronics',
    'Transport',
    'Food',
    'Civil',
    'Metallurgical',
    'Electrotechnical'
  ];

  const fetchStandards = async () => {
    setLoading(true);
    try {
      let url = `${API_BASE_URL}/api/directory?`;
      if (search) url += `search=${encodeURIComponent(search)}&`;
      if (division && division !== 'All Divisions') url += `division=${encodeURIComponent(division)}&`;

      const res = await fetch(url);
      const data = await res.json();
      setStandards(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Failed to fetch directory", err);
      setStandards([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timeout = setTimeout(() => {
      fetchStandards();
    }, 200);
    return () => clearTimeout(timeout);
  }, [search, division]);

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '10px' }}>
      <div style={{ textAlign: 'center', marginBottom: '24px' }}>
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          padding: '6px 14px',
          background: 'rgba(16, 185, 129, 0.12)',
          borderRadius: '9999px',
          color: '#34d399',
          fontSize: '0.85rem',
          fontWeight: 600,
          marginBottom: '12px'
        }}>
          <BookOpen size={16} /> {t('directory_title')}
        </div>
        <h2 style={{ fontSize: '2rem', margin: '0 0 8px 0', color: 'var(--text-primary)' }}>
          {t('directory_title')}
        </h2>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto', fontSize: '0.95rem' }}>
          {t('directory_subtitle')}
        </p>
      </div>

      {/* Filter Bar */}
      <div className="glass-panel" style={{ padding: '20px', marginBottom: '24px', display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
        <div style={{ flex: '2 1 300px', position: 'relative' }}>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder={t('directory_search_placeholder')}
            style={{
              width: '100%',
              padding: '12px 16px',
              backgroundColor: 'var(--bg-input)',
              border: '1px solid var(--border-strong)',
              borderRadius: '8px',
              color: 'var(--text-primary)',
              fontSize: '0.95rem',
              outline: 'none',
              boxShadow: '0 1px 3px rgba(0,0,0,0.03)'
            }}
          />
        </div>

        <div style={{ flex: '1 1 200px' }}>
          <select
            value={division}
            onChange={(e) => setDivision(e.target.value)}
            style={{
              width: '100%',
              padding: '12px 14px',
              backgroundColor: 'var(--bg-input)',
              border: '1px solid var(--border-strong)',
              borderRadius: '8px',
              color: 'var(--text-primary)',
              fontSize: '0.9rem',
              outline: 'none',
              boxShadow: '0 1px 3px rgba(0,0,0,0.03)'
            }}
          >
            {divisions.map((d) => (
              <option key={d} value={d} style={{ background: 'var(--bg-card)', color: 'var(--text-primary)' }}>{d}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(460px, 1fr))', gap: '16px' }}>
        {standards.map((s) => (
          <div key={s.is_code} className="glass-card" style={{ padding: '22px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '12px', marginBottom: '8px' }}>
                <span style={{
                  fontFamily: 'JetBrains Mono',
                  fontWeight: 700,
                  fontSize: '1.1rem',
                  color: 'var(--accent-blue)'
                }}>
                  {s.is_code}
                </span>

                <span className={s.qco_status === 'Mandatory' ? 'badge-confirmed' : 'badge-verification'} style={{
                  fontSize: '0.75rem',
                  padding: '4px 10px',
                  borderRadius: '9999px',
                  fontWeight: 700
                }}>
                  {s.qco_status.toUpperCase()}
                </span>
              </div>

              <h4 style={{ margin: '0 0 8px 0', fontSize: '1rem', color: 'var(--text-primary)', lineHeight: 1.4 }}>
                {s.title}
              </h4>

              <div style={{ fontSize: '0.8rem', color: 'var(--accent-saffron)', marginBottom: '10px' }}>
                Division: {s.division}
              </div>

              {s.qco_reference && (
                <div style={{
                  padding: '8px 12px',
                  backgroundColor: 'var(--bg-surface)',
                  borderLeft: '3px solid var(--accent-blue)',
                  borderRadius: '4px',
                  fontSize: '0.8rem',
                  color: 'var(--text-secondary)',
                  marginBottom: '12px'
                }}>
                  <strong>QCO:</strong> {s.qco_reference}
                </div>
              )}

              {s.synonyms && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexWrap: 'wrap', marginBottom: '12px' }}>
                  <Tag size={13} color="var(--text-muted)" />
                  {s.synonyms.split(',').slice(0, 4).map((syn, idx) => (
                    <span key={idx} style={{
                      fontSize: '0.72rem',
                      padding: '2px 8px',
                      background: 'var(--bg-surface)',
                      borderRadius: '4px',
                      color: 'var(--text-secondary)'
                    }}>
                      {syn.trim()}
                    </span>
                  ))}
                </div>
              )}
            </div>

            <div style={{
              borderTop: '1px solid var(--border-subtle)',
              paddingTop: '12px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <a
                href={s.source_url}
                target="_blank"
                rel="noreferrer"
                style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '4px', textDecoration: 'none' }}
              >
                Official Spec <ExternalLink size={12} />
              </a>

              {onSelectStandard && (
                <button
                  onClick={() => onSelectStandard(s)}
                  className="btn-secondary"
                  style={{ fontSize: '0.8rem', padding: '6px 12px' }}
                >
                  Consult Saathi <ArrowRight size={13} />
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
