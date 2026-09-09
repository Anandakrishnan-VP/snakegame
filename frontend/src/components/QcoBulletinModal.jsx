import React, { useState, useMemo } from 'react';
import { 
  X, 
  ExternalLink, 
  RefreshCw, 
  Calendar, 
  ShieldCheck, 
  AlertTriangle, 
  Clock, 
  CheckCircle2, 
  Search, 
  Building2, 
  FileText, 
  MessageSquare,
  Sparkles,
  ArrowRight
} from 'lucide-react';

export default function QcoBulletinModal({
  isOpen,
  onClose,
  bulletinData,
  onRefresh,
  isRefreshing,
  onAskAboutStandard,
  t = (k) => k
}) {
  const [activeFilter, setActiveFilter] = useState('all'); // 'all', 'extended', 'upcoming', 'active'
  const [searchQuery, setSearchQuery] = useState('');

  const notices = bulletinData?.notices || [];

  const filteredNotices = useMemo(() => {
    return notices.filter((n) => {
      // Tab filter
      if (activeFilter === 'extended' && n.status !== 'extended') return false;
      if (activeFilter === 'upcoming' && n.status !== 'upcoming') return false;
      if (activeFilter === 'active' && n.status !== 'active') return false;

      // Text search
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matches = (
          (n.title && n.title.toLowerCase().includes(q)) ||
          (n.standard_code && n.standard_code.toLowerCase().includes(q)) ||
          (n.product_category && n.product_category.toLowerCase().includes(q)) ||
          (n.summary && n.summary.toLowerCase().includes(q)) ||
          (n.ministry && n.ministry.toLowerCase().includes(q))
        );
        if (!matches) return false;
      }
      return true;
    });
  }, [notices, activeFilter, searchQuery]);

  const counts = useMemo(() => {
    return {
      all: notices.length,
      extended: notices.filter(n => n.status === 'extended').length,
      upcoming: notices.filter(n => n.status === 'upcoming').length,
      active: notices.filter(n => n.status === 'active').length,
    };
  }, [notices]);

  const formatLastSynced = (isoString) => {
    if (!isoString) return 'Just now';
    try {
      const d = new Date(isoString);
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    } catch {
      return 'Just now';
    }
  };

  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(17, 19, 21, 0.65)',
      backdropFilter: 'blur(8px)',
      WebkitBackdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '20px'
    }}>
      <div 
        className="animate-fade-in"
        style={{
          backgroundColor: 'var(--bg-card)',
          borderRadius: '16px',
          width: '100%',
          maxWidth: '860px',
          maxHeight: '90vh',
          display: 'flex',
          flexDirection: 'column',
          boxShadow: '0 24px 60px -12px rgba(0, 0, 0, 0.4)',
          border: '1px solid var(--border-subtle)',
          overflow: 'hidden'
        }}
      >
        {/* Modal Header */}
        <div style={{
          padding: '16px 20px',
          background: 'linear-gradient(135deg, #052e22 0%, #031c15 100%)',
          color: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          borderBottom: '1px solid rgba(16, 185, 129, 0.3)',
          flexShrink: 0
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '9px',
              background: 'rgba(16, 185, 129, 0.2)',
              border: '1px solid rgba(16, 185, 129, 0.4)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#34d399'
            }}>
              <ShieldCheck size={20} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <h3 style={{ fontSize: '1.05rem', fontWeight: 700, margin: 0, color: '#ffffff', fontFamily: 'Outfit, sans-serif' }}>
                  {t('bulletin_title') || 'Official Gazette & QCO Regulatory Bulletin'}
                </h3>
                <span style={{
                  fontSize: '0.65rem',
                  padding: '2px 7px',
                  borderRadius: '9999px',
                  background: 'rgba(16, 185, 129, 0.25)',
                  color: '#6ee7b7',
                  fontWeight: 700,
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '4px',
                  letterSpacing: '0.03em'
                }}>
                  <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#34d399', display: 'inline-block' }}></span>
                  LIVE GAZETTE FEED
                </span>
              </div>
              <p style={{ fontSize: '0.74rem', color: '#cbd5e1', margin: '2px 0 0 0' }}>
                {t('bulletin_subtitle') || 'Real-time tracking of Quality Control Orders, Ministry deadline extensions & mandatory compliance dates'}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: '#cbd5e1',
              cursor: 'pointer',
              padding: '6px',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => { e.currentTarget.style.color = '#ffffff'; e.currentTarget.style.background = 'rgba(255,255,255,0.1)'; }}
            onMouseLeave={(e) => { e.currentTarget.style.color = '#cbd5e1'; e.currentTarget.style.background = 'transparent'; }}
          >
            <X size={18} />
          </button>
        </div>

        {/* Toolbar: Live Sync info + Refresh Button + Search */}
        <div style={{
          padding: '12px 20px',
          background: 'var(--bg-surface)',
          borderBottom: '1px solid var(--border-subtle)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '10px',
          flexShrink: 0
        }}>
          {/* Sync status & Refresh button */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <button
              onClick={onRefresh}
              disabled={isRefreshing}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '6px 12px',
                borderRadius: '8px',
                border: '1px solid var(--border-subtle)',
                background: 'var(--bg-card)',
                color: 'var(--accent-aqua)',
                fontWeight: 600,
                fontSize: '0.78rem',
                cursor: isRefreshing ? 'wait' : 'pointer',
                transition: 'all 0.2s ease',
                boxShadow: '0 1px 4px rgba(0,0,0,0.05)'
              }}
              onMouseEnter={(e) => { if (!isRefreshing) e.currentTarget.style.borderColor = 'var(--accent-aqua)'; }}
              onMouseLeave={(e) => { if (!isRefreshing) e.currentTarget.style.borderColor = 'var(--border-subtle)'; }}
            >
              <RefreshCw size={13} className={isRefreshing ? 'animate-spin' : ''} />
              <span>{isRefreshing ? 'Syncing Gazette...' : 'Sync with Live Gazette'}</span>
            </button>

            <span style={{ fontSize: '0.73rem', color: 'var(--text-muted)' }}>
              Last Synced: <strong>{formatLastSynced(bulletinData?.last_synced)}</strong>
            </span>
          </div>

          {/* Quick Filter Search */}
          <div style={{ position: 'relative', width: '240px' }}>
            <Search size={13} style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
            <input
              type="text"
              placeholder="Search standard, order..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                width: '100%',
                padding: '6px 10px 6px 28px',
                borderRadius: '8px',
                border: '1px solid var(--border-subtle)',
                background: 'var(--bg-card)',
                color: 'var(--text-primary)',
                fontSize: '0.78rem',
                outline: 'none'
              }}
              onFocus={(e) => { e.currentTarget.style.borderColor = 'var(--accent-aqua)'; }}
              onBlur={(e) => { e.currentTarget.style.borderColor = 'var(--border-subtle)'; }}
            />
          </div>
        </div>

        {/* Filter Tabs */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          padding: '8px 20px',
          background: 'var(--bg-canvas)',
          borderBottom: '1px solid var(--border-subtle)',
          flexShrink: 0
        }}>
          {[
            { id: 'all', label: 'All Regulatory Orders', count: counts.all },
            { id: 'extended', label: '⚡ Relief & MSME Extensions', count: counts.extended },
            { id: 'upcoming', label: '⏳ Upcoming Deadlines', count: counts.upcoming },
            { id: 'active', label: '🛡️ Enforced QCOs', count: counts.active },
          ].map((tab) => {
            const isActive = activeFilter === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveFilter(tab.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '5px',
                  padding: '5px 11px',
                  borderRadius: '7px',
                  border: 'none',
                  background: isActive ? 'var(--btn-primary-bg)' : 'transparent',
                  color: isActive ? 'var(--btn-primary-text)' : 'var(--text-secondary)',
                  fontWeight: 600,
                  fontSize: '0.75rem',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease'
                }}
              >
                <span>{tab.label}</span>
                <span style={{
                  fontSize: '0.68rem',
                  padding: '1px 5px',
                  borderRadius: '9999px',
                  background: isActive ? 'rgba(255,255,255,0.2)' : 'var(--bg-surface)',
                  color: isActive ? '#ffffff' : 'var(--text-muted)'
                }}>
                  {tab.count}
                </span>
              </button>
            );
          })}
        </div>

        {/* Notice Cards List */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '16px 20px',
          display: 'flex',
          flexDirection: 'column',
          gap: '12px'
        }}>
          {filteredNotices.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--text-muted)' }}>
              <FileText size={32} style={{ opacity: 0.4, marginBottom: '8px' }} />
              <p style={{ margin: 0, fontSize: '0.88rem', fontWeight: 500 }}>No government notices match your search or filter.</p>
              <p style={{ margin: '4px 0 0', fontSize: '0.75rem' }}>Click "Sync with Live Gazette" to scan official portals for fresh notifications.</p>
            </div>
          ) : (
            filteredNotices.map((notice) => {
              const isExtended = notice.status === 'extended';
              const isUpcoming = notice.status === 'upcoming';
              const badgeBg = isExtended ? 'rgba(59, 130, 246, 0.12)' : isUpcoming ? 'rgba(245, 158, 11, 0.12)' : 'rgba(16, 185, 129, 0.12)';
              const badgeBorder = isExtended ? 'rgba(59, 130, 246, 0.3)' : isUpcoming ? 'rgba(245, 158, 11, 0.3)' : 'rgba(16, 185, 129, 0.3)';
              const badgeColor = isExtended ? '#2563eb' : isUpcoming ? '#d97706' : '#059669';

              return (
                <div
                  key={notice.id}
                  style={{
                    backgroundColor: 'var(--bg-card)',
                    borderRadius: '12px',
                    border: '1px solid var(--border-subtle)',
                    padding: '14px 16px',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '10px',
                    transition: 'all 0.2s ease',
                    boxShadow: '0 2px 6px rgba(0,0,0,0.03)'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = 'var(--accent-aqua)';
                    e.currentTarget.style.boxShadow = '0 4px 12px rgba(13, 148, 136, 0.08)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = 'var(--border-subtle)';
                    e.currentTarget.style.boxShadow = '0 2px 6px rgba(0,0,0,0.03)';
                  }}
                >
                  {/* Top line: Category, Standard Tag, Status Badge */}
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '8px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <span style={{
                        fontSize: '0.72rem',
                        fontWeight: 700,
                        padding: '3px 8px',
                        borderRadius: '6px',
                        background: 'rgba(13, 148, 136, 0.12)',
                        color: 'var(--accent-aqua)',
                        fontFamily: 'JetBrains Mono, monospace'
                      }}>
                        {notice.standard_code}
                      </span>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600 }}>
                        {notice.product_category}
                      </span>
                    </div>

                    <span style={{
                      fontSize: '0.7rem',
                      fontWeight: 700,
                      padding: '3px 8px',
                      borderRadius: '9999px',
                      background: badgeBg,
                      border: `1px solid ${badgeBorder}`,
                      color: badgeColor,
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '4px'
                    }}>
                      {isExtended && <Clock size={11} />}
                      {isUpcoming && <AlertTriangle size={11} />}
                      {!isExtended && !isUpcoming && <CheckCircle2 size={11} />}
                      {notice.status_label}
                    </span>
                  </div>

                  {/* Title & Gazette S.O. */}
                  <div>
                    <h4 style={{ fontSize: '0.92rem', fontWeight: 700, color: 'var(--text-primary)', margin: 0, lineHeight: 1.3 }}>
                      {notice.title}
                    </h4>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '4px', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                      <span style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                        <Building2 size={12} /> {notice.ministry}
                      </span>
                      <span>•</span>
                      <span style={{ fontFamily: 'JetBrains Mono, monospace' }}>
                        {notice.gazette_so}
                      </span>
                    </div>
                  </div>

                  {/* Summary */}
                  <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', lineHeight: 1.45, margin: 0 }}>
                    {notice.summary}
                  </p>

                  {/* Enforcement Date strip */}
                  <div style={{
                    padding: '6px 10px',
                    borderRadius: '8px',
                    background: 'var(--bg-surface)',
                    border: '1px solid var(--border-subtle)',
                    fontSize: '0.74rem',
                    color: 'var(--text-primary)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    flexWrap: 'wrap',
                    gap: '6px'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                      <Calendar size={13} color="var(--accent-aqua)" />
                      <span><strong>Timeline:</strong> {notice.enforcement_date}</span>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <a
                        href={notice.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{
                          color: 'var(--accent-aqua)',
                          textDecoration: 'none',
                          fontSize: '0.72rem',
                          fontWeight: 600,
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '3px'
                        }}
                      >
                        Official Gazette PDF <ExternalLink size={10} />
                      </a>

                      {onAskAboutStandard && (
                        <button
                          onClick={() => {
                            onAskAboutStandard(`What are the exact QCO compliance deadlines and Scheme-I licensing steps for ${notice.standard_code} (${notice.product_category})?`);
                            onClose();
                          }}
                          style={{
                            background: 'var(--btn-primary-bg)',
                            color: 'var(--btn-primary-text)',
                            border: 'none',
                            borderRadius: '6px',
                            padding: '3px 9px',
                            fontSize: '0.72rem',
                            fontWeight: 600,
                            cursor: 'pointer',
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '4px',
                            transition: 'all 0.15s ease'
                          }}
                        >
                          <MessageSquare size={10} /> Ask Saathi <ArrowRight size={10} />
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}
