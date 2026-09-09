import React, { useState, useEffect } from 'react';
import { FlaskConical, MapPin, Mail, Phone, ShieldCheck, Search, Filter } from 'lucide-react';
import { API_BASE_URL } from '../api/config';

export default function LabFinder({ currentLang = 'en', t = (k) => k }) {
  const [labs, setLabs] = useState([]);
  const [city, setCity] = useState('');
  const [selectedStandard, setSelectedStandard] = useState('');
  const [loading, setLoading] = useState(false);

  const cities = ['All Cities', 'Ghaziabad', 'Mumbai', 'Delhi', 'Chennai', 'Kolkata', 'Chandigarh', 'Pune', 'Bengaluru'];
  const standardsList = [
    { code: '', label: 'All Standards' },
    { code: 'IS 17803:2022', label: 'IS 17803 (Stainless Steel Vacuum Flasks)' },
    { code: 'IS 9873 (Part 1):2019', label: 'IS 9873 (Safety of Toys)' },
    { code: 'IS 16046 (Part 2):2018', label: 'IS 16046 (Lithium-ion Batteries & Power Banks)' },
    { code: 'IS 4151:2015', label: 'IS 4151 (Two-Wheeler Helmets)' },
    { code: 'IS 14543:2016', label: 'IS 14543 (Packaged Drinking Water)' },
    { code: 'IS 1489 (Part 1):2015', label: 'IS 1489 (PPC Cement)' }
  ];

  const fetchLabs = async () => {
    setLoading(true);
    try {
      let url = `${API_BASE_URL}/api/labs?`;
      if (selectedStandard) url += `is_code=${encodeURIComponent(selectedStandard)}&`;
      if (city && city !== 'All Cities') url += `city=${encodeURIComponent(city)}&`;

      const res = await fetch(url);
      const data = await res.json();
      setLabs(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Failed to fetch labs", err);
      setLabs([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLabs();
  }, [city, selectedStandard]);

  return (
    <div style={{ maxWidth: '950px', margin: '0 auto', padding: '10px' }}>
      <div style={{ textAlign: 'center', marginBottom: '24px' }}>
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          padding: '6px 14px',
          background: 'rgba(13, 148, 136, 0.12)',
          borderRadius: '9999px',
          color: 'var(--accent-aqua)',
          fontSize: '0.85rem',
          fontWeight: 600,
          marginBottom: '12px',
          border: '1px solid rgba(13, 148, 136, 0.28)'
        }}>
          <FlaskConical size={16} /> {t('labs_title')}
        </div>
        <h2 style={{ fontSize: '2rem', margin: '0 0 8px 0', color: 'var(--text-primary)' }}>
          {t('labs_title')}
        </h2>
        <p style={{ color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto', fontSize: '0.95rem' }}>
          {t('labs_subtitle')}
        </p>
      </div>

      {/* Filter Card */}
      <div className="glass-panel" style={{ padding: '20px', marginBottom: '24px', display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
        <div style={{ flex: '1 1 250px' }}>
          <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '6px', fontWeight: 600 }}>Filter by Standard</label>
          <select
            value={selectedStandard}
            onChange={(e) => setSelectedStandard(e.target.value)}
            style={{
              width: '100%',
              padding: '12px 14px',
              backgroundColor: 'var(--bg-input)',
              border: '1px solid var(--border-subtle)',
              borderRadius: '8px',
              color: 'var(--text-primary)',
              fontSize: '0.9rem',
              outline: 'none',
              transition: 'border-color 0.2s ease'
            }}
            onFocus={(e) => { e.currentTarget.style.borderColor = 'var(--accent-aqua)'; }}
            onBlur={(e) => { e.currentTarget.style.borderColor = 'var(--border-subtle)'; }}
          >
            {standardsList.map((s) => (
              <option key={s.code} value={s.code} style={{ background: 'var(--bg-card)', color: 'var(--text-primary)' }}>{s.label}</option>
            ))}
          </select>
        </div>

        <div style={{ flex: '1 1 200px' }}>
          <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '6px', fontWeight: 600 }}>{t('labs_filter_city')}</label>
          <select
            value={city}
            onChange={(e) => setCity(e.target.value)}
            style={{
              width: '100%',
              padding: '12px 14px',
              backgroundColor: 'var(--bg-input)',
              border: '1px solid var(--border-subtle)',
              borderRadius: '8px',
              color: 'var(--text-primary)',
              fontSize: '0.9rem',
              outline: 'none',
              transition: 'border-color 0.2s ease'
            }}
            onFocus={(e) => { e.currentTarget.style.borderColor = 'var(--accent-aqua)'; }}
            onBlur={(e) => { e.currentTarget.style.borderColor = 'var(--border-subtle)'; }}
          >
            {cities.map((c) => (
              <option key={c} value={c} style={{ background: 'var(--bg-card)', color: 'var(--text-primary)' }}>{c}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Result Status & Reset */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px', flexWrap: 'wrap', gap: '8px' }}>
        <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
          {loading ? 'Searching laboratories...' : (
            <>
              Showing <strong style={{ color: 'var(--text-primary)' }}>{labs.length}</strong> {labs.length === 1 ? 'laboratory' : 'laboratories'} {city && city !== 'All Cities' ? <>for <strong style={{ color: 'var(--accent-aqua)' }}>{city}</strong></> : 'across India'}
            </>
          )}
        </span>
        {((city && city !== 'All Cities') || selectedStandard) && (
          <button
            onClick={() => { setCity('All Cities'); setSelectedStandard(''); }}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--accent-aqua)',
              fontSize: '0.8rem',
              fontWeight: 600,
              cursor: 'pointer',
              textDecoration: 'underline'
            }}
          >
            Clear Filters
          </button>
        )}
      </div>

      {/* Empty State */}
      {!loading && labs.length === 0 && (
        <div className="glass-card" style={{ padding: '48px 24px', textAlign: 'center', color: 'var(--text-muted)' }}>
          <FlaskConical size={38} style={{ margin: '0 auto 12px auto', opacity: 0.4 }} />
          <p style={{ margin: 0, fontSize: '1.05rem', color: 'var(--text-primary)', fontWeight: 600 }}>No Testing Laboratories Found</p>
          <p style={{ margin: '8px 0 16px 0', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            No accredited lab matches your chosen standard and city filter.
          </p>
          <button
            onClick={() => { setCity('All Cities'); setSelectedStandard(''); }}
            className="btn-primary"
            style={{ fontSize: '0.82rem', padding: '6px 14px' }}
          >
            Show All Laboratories
          </button>
        </div>
      )}

      {/* Labs List */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(420px, 1fr))', gap: '16px' }}>
        {labs.map((lab) => (
          <div key={lab.lab_id} className="glass-card" style={{ padding: '20px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
            <div>
              {lab.fallback_note && (
                <div style={{
                  fontSize: '0.78rem',
                  color: '#b45309',
                  background: 'rgba(217, 119, 6, 0.12)',
                  border: '1px solid rgba(217, 119, 6, 0.28)',
                  borderRadius: '6px',
                  padding: '5px 10px',
                  marginBottom: '12px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  lineHeight: '1.3'
                }}>
                  <span>📍</span> {lab.fallback_note}
                </div>
              )}

              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '10px', marginBottom: '10px' }}>
                <h4 style={{ margin: 0, fontSize: '1.05rem', color: 'var(--text-primary)' }}>{lab.lab_name}</h4>
                <span style={{
                  fontSize: '0.75rem',
                  padding: '4px 10px',
                  borderRadius: '9999px',
                  background: lab.lab_type === 'Central' ? 'rgba(13, 148, 136, 0.14)' : 'var(--bg-surface)',
                  color: lab.lab_type === 'Central' ? 'var(--accent-aqua)' : 'var(--text-secondary)',
                  border: '1px solid var(--border-subtle)',
                  fontWeight: 600,
                  whiteSpace: 'nowrap'
                }}>
                  {lab.lab_type} Lab
                </span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '8px' }}>
                <MapPin size={15} color="var(--accent-aqua)" />
                <span>{lab.address}, {lab.city}, {lab.state}</span>
              </div>

              {lab.is_nabl_accredited && (
                <div style={{ display: 'inline-flex', alignItems: 'center', gap: '5px', color: '#059669', fontSize: '0.78rem', background: 'rgba(5, 150, 105, 0.1)', border: '1px solid rgba(5, 150, 105, 0.25)', padding: '3px 8px', borderRadius: '4px', marginBottom: '12px' }}>
                  <ShieldCheck size={14} /> NABL ISO/IEC 17025 Accredited
                </div>
              )}
            </div>

            <div style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: '12px', marginTop: '12px', display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '8px', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              {lab.contact_email && (
                <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                  <Mail size={13} /> {lab.contact_email}
                </span>
              )}
              {lab.phone && (
                <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                  <Phone size={13} /> {lab.phone}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
