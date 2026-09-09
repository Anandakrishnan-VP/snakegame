import React from 'react';
import { X, ExternalLink, ShieldCheck, AlertCircle, FileText, BookOpen, Layers } from 'lucide-react';

export default function SourceInspectorModal({ isOpen, onClose, evidence }) {
  if (!isOpen || !evidence) return null;

  const status = evidence.status || 'confirmed';
  const isConfirmed = status.toLowerCase() === 'confirmed';
  const isNeedsVerification = status.toLowerCase().includes('verification');

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.7)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '20px'
    }}>
      <div 
        className="glass-panel animate-fade-in"
        style={{
          width: '100%',
          maxWidth: '680px',
          maxHeight: '90vh',
          display: 'flex',
          flexDirection: 'column',
          backgroundColor: 'var(--bg-card)',
          border: '1px solid var(--border-subtle)',
          boxShadow: 'var(--shadow-hover)',
          overflow: 'hidden'
        }}
      >
        {/* Header */}
        <div style={{
          padding: '20px 24px',
          borderBottom: '1px solid var(--border-subtle)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: 'linear-gradient(90deg, var(--accent-saffron-glow) 0%, transparent 100%)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '40px',
              height: '40px',
              borderRadius: '10px',
              background: 'var(--accent-saffron-glow)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--accent-saffron)'
            }}>
              <BookOpen size={22} />
            </div>
            <div>
              <h3 style={{ margin: 0, fontSize: '1.2rem', color: 'var(--text-primary)' }}>Official Source & Clause Inspector</h3>
              <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                Authorized clause summary & statutory gazette records
              </p>
            </div>
          </div>
          <button 
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-muted)',
              cursor: 'pointer',
              padding: '6px',
              borderRadius: '6px',
              display: 'flex',
              alignItems: 'center'
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Body */}
        <div style={{ padding: '24px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Status & Code Bar */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '10px',
            padding: '12px 16px',
            backgroundColor: 'var(--bg-surface)',
            borderRadius: '10px',
            border: '1px solid var(--border-subtle)'
          }}>
            <div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Standard Reference</span>
              <div style={{ fontWeight: 700, fontSize: '1.1rem', color: 'var(--accent-blue)', fontFamily: 'JetBrains Mono' }}>
                {evidence.reference || 'Indian Standard Record'}
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '6px 14px',
                borderRadius: '9999px',
                fontSize: '0.85rem',
                fontWeight: 600
              }} className={isConfirmed ? 'badge-confirmed' : isNeedsVerification ? 'badge-verification' : 'badge-not-determined'}>
                {isConfirmed ? <ShieldCheck size={16} /> : <AlertCircle size={16} />}
                {evidence.status ? evidence.status.toUpperCase() : 'CONFIRMED'}
              </span>
            </div>
          </div>

          {/* Clause Meta */}
          {evidence.clause_number && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '12px' }}>
              <div style={{ padding: '12px', background: 'var(--bg-surface)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Clause</span>
                <p style={{ margin: '4px 0 0', fontWeight: 600, color: 'var(--text-primary)' }}>{evidence.clause_number}</p>
              </div>
              {evidence.sub_clause && (
                <div style={{ padding: '12px', background: 'var(--bg-surface)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Sub-clause</span>
                  <p style={{ margin: '4px 0 0', fontWeight: 600, color: 'var(--text-primary)' }}>{evidence.sub_clause}</p>
                </div>
              )}
              {evidence.page && (
                <div style={{ padding: '12px', background: 'var(--bg-surface)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Publication Page</span>
                  <p style={{ margin: '4px 0 0', fontWeight: 600, color: 'var(--text-primary)' }}>Page {evidence.page}</p>
                </div>
              )}
              <div style={{ padding: '12px', background: 'var(--bg-surface)', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Source Category</span>
                <p style={{ margin: '4px 0 0', fontWeight: 600, color: 'var(--text-primary)', textTransform: 'capitalize' }}>{evidence.source_type || 'Gazette / Clause'}</p>
              </div>
            </div>
          )}

          {/* Clause Summary */}
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
              <FileText size={16} color="var(--accent-saffron)" />
              <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Technical Clause Summary & Statutory Order</span>
            </div>
            <div style={{
              padding: '16px',
              backgroundColor: 'var(--bg-surface)',
              borderLeft: '3px solid var(--accent-saffron)',
              borderRadius: '6px',
              color: 'var(--text-primary)',
              fontSize: '0.95rem',
              lineHeight: 1.6
            }}>
              {evidence.clause_summary || evidence.verbatim_excerpt || 'No specific clause summary available.'}
            </div>
            <p style={{ margin: '6px 0 0', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              Note: Unaltered standard publications are commercially published by BIS via Manak Online (www.manakonline.in).
            </p>
          </div>

          {/* QCO or Ministry details */}
          {evidence.qco_reference && (
            <div style={{
              padding: '12px 16px',
              backgroundColor: 'var(--bg-surface)',
              border: '1px solid var(--border-subtle)',
              borderRadius: '8px'
            }}>
              <span style={{ fontSize: '0.75rem', color: 'var(--accent-blue)', fontWeight: 600, textTransform: 'uppercase' }}>Government QCO Notification</span>
              <p style={{ margin: '4px 0 0', fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
                {evidence.qco_reference}
              </p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div style={{
          padding: '16px 24px',
          borderTop: '1px solid var(--border-subtle)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          backgroundColor: 'var(--bg-surface)'
        }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            Source: Bureau of Indian Standards & Ministry Gazette Orders
          </span>
          <div style={{ display: 'flex', gap: '12px' }}>
            {evidence.source_url && (
              <a 
                href={evidence.source_url} 
                target="_blank" 
                rel="noreferrer" 
                className="btn-primary"
                style={{ fontSize: '0.85rem', padding: '8px 16px', textDecoration: 'none' }}
              >
                View Official Portal <ExternalLink size={14} />
              </a>
            )}
            <button 
              onClick={onClose}
              className="btn-secondary"
              style={{ fontSize: '0.85rem', padding: '8px 16px' }}
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
