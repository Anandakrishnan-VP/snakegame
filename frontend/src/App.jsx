import React, { useState, useEffect, useLayoutEffect } from 'react';
import { 
  MessageSquare, 
  ShieldCheck, 
  FlaskConical, 
  BookOpen, 
  Sparkles, 
  CheckCircle2, 
  Award, 
  FileText, 
  Search, 
  ArrowRight, 
  ExternalLink, 
  Globe, 
  Compass,
  Sun,
  Moon,
  Bell
} from 'lucide-react';

import ChatView from './components/ChatView';
import JourneyView from './components/JourneyView';
import VerificationPanel from './components/VerificationPanel';
import LabFinder from './components/LabFinder';
import DirectoryBrowser from './components/DirectoryBrowser';
import SourceInspectorModal from './components/SourceInspectorModal';
import VoiceModal from './components/VoiceModal';
import QcoBulletinModal from './components/QcoBulletinModal';
import Footer from './components/Footer';
import { SUPPORTED_LANGUAGES, getTranslation } from './i18n/translations';
import { API_BASE_URL } from './api/config';

export default function App() {
  const [activeTab, setActiveTab] = useState('chat'); // 'chat', 'journey', 'verify', 'labs', 'directory'
  const [currentLang, setCurrentLang] = useState('en');
  const [selectedEvidence, setSelectedEvidence] = useState(null);
  const [isSourceModalOpen, setIsSourceModalOpen] = useState(false);
  const [isVoiceModalOpen, setIsVoiceModalOpen] = useState(false);
  const [voiceTranscript, setVoiceTranscript] = useState('');
  const [initialChatQuery, setInitialChatQuery] = useState('');
  const [journeyStandardId, setJourneyStandardId] = useState(null);
  const [apiStatus, setApiStatus] = useState('checking');

  // Live Gazette & QCO Bulletin state
  const [isBulletinOpen, setIsBulletinOpen] = useState(false);
  const [bulletinData, setBulletinData] = useState(null);
  const [isBulletinRefreshing, setIsBulletinRefreshing] = useState(false);
  const [isAlertDismissed, setIsAlertDismissed] = useState(false);

  const fetchBulletin = async (refresh = false) => {
    if (refresh) setIsBulletinRefreshing(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/qco-bulletin${refresh ? '?refresh=true' : ''}`);
      if (res.ok) {
        const data = await res.json();
        setBulletinData(data);
      }
    } catch (err) {
      console.error("Failed to fetch QCO bulletin", err);
    } finally {
      if (refresh) setIsBulletinRefreshing(false);
    }
  };

  useEffect(() => {
    fetchBulletin();
  }, []);

  // Theme State (defaulting to 'light' with localStorage persistence)
  const [theme, setTheme] = useState(() => {
    try {
      return localStorage.getItem('bis_saathi_theme') || 'light';
    } catch (e) {
      return 'light';
    }
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    try {
      localStorage.setItem('bis_saathi_theme', theme);
    } catch (e) {}
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  const t = (key) => getTranslation(currentLang, key);

  // Check backend health
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/api/health`);
        if (res.ok) setApiStatus('online');
        else setApiStatus('offline');
      } catch (e) {
        setApiStatus('offline');
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleInspectEvidence = (evidence) => {
    setSelectedEvidence(evidence);
    setIsSourceModalOpen(true);
  };

  const handleSelectStandardFromDirectory = (standard) => {
    setInitialChatQuery(`What are the testing and certification requirements for ${standard.is_code} (${standard.title})?`);
    setActiveTab('chat');
    window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
  };

  // Robust zero-latency scroll reset before browser paints to prevent any footer flicker/blink
  useLayoutEffect(() => {
    window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
    document.documentElement.scrollTop = 0;
    document.body.scrollTop = 0;
  }, [activeTab]);

  return (
    <div style={{
      height: activeTab === 'chat' ? '100vh' : 'auto',
      minHeight: '100vh',
      maxHeight: activeTab === 'chat' ? '100vh' : 'none',
      overflow: activeTab === 'chat' ? 'hidden' : 'visible',
      display: 'flex',
      flexDirection: 'column'
    }}>
      {/* Top Navbar */}
      <header style={{
        backgroundColor: 'var(--bg-glass)',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
        borderBottom: '1px solid var(--border-subtle)',
        position: 'sticky',
        top: 0,
        zIndex: 100,
        flexShrink: 0,
        transition: 'background-color 0.3s ease, border-color 0.3s ease'
      }}>
        <div style={{
          maxWidth: '1440px',
          margin: '0 auto',
          padding: '8px 16px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '12px',
          width: '100%',
          boxSizing: 'border-box'
        }}>
          {/* Logo & Title */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexShrink: 0, minWidth: 0 }}>
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '9px',
              background: 'linear-gradient(135deg, #111315 0%, #0d9488 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#ffffff',
              boxShadow: '0 3px 10px rgba(13, 148, 136, 0.25)',
              flexShrink: 0
            }}>
              <Award size={20} />
            </div>
            <div style={{ minWidth: 0 }}>
              <span className="font-heading" style={{ fontSize: '1.12rem', color: 'var(--text-primary)', fontWeight: 800, display: 'block', lineHeight: 1.1 }}>
                BIS Saathi
              </span>
              <span title={t('subtitle')} style={{ fontSize: '0.64rem', color: 'var(--text-muted)', display: 'block', marginTop: '1px', maxWidth: '200px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {t('subtitle')}
              </span>
            </div>
          </div>

          {/* Navigation Pills */}
          <nav style={{
            display: 'flex',
            alignItems: 'center',
            gap: '3px',
            background: 'var(--bg-surface)',
            padding: '3px',
            borderRadius: '11px',
            border: '1px solid var(--border-subtle)',
            flex: '0 1 auto',
            minWidth: 0,
            overflowX: 'auto',
            scrollbarWidth: 'none',
            WebkitOverflowScrolling: 'touch'
          }}>
            {[
              { id: 'chat', labelKey: 'tab_chat', icon: MessageSquare },
              { id: 'journey', labelKey: 'tab_journey', icon: Compass },
              { id: 'verify', labelKey: 'tab_verify', icon: ShieldCheck },
              { id: 'labs', labelKey: 'tab_labs', icon: FlaskConical },
              { id: 'directory', labelKey: 'tab_directory', icon: BookOpen }
            ].map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => { setActiveTab(tab.id); window.scrollTo({ top: 0, left: 0, behavior: 'instant' }); }}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '5px',
                    height: '30px',
                    padding: '0 10px',
                    borderRadius: '8px',
                    border: 'none',
                    background: isActive ? 'var(--btn-primary-bg)' : 'transparent',
                    color: isActive ? 'var(--btn-primary-text)' : 'var(--text-secondary)',
                    fontWeight: 600,
                    fontSize: '0.78rem',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                    whiteSpace: 'nowrap',
                    flexShrink: 0
                  }}
                >
                  <Icon size={14} />
                  <span>{t(tab.labelKey)}</span>
                </button>
              );
            })}
          </nav>

          {/* Right Controls: Global Language Selector, Theme Switcher & Status */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0, marginLeft: 'auto' }}>
            {/* Live Gazette Notices Icon Button */}
            <button
              onClick={() => setIsBulletinOpen(true)}
              title={t('bulletin_title') || 'View Live Government Gazette Notices & QCOs'}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                position: 'relative',
                width: '36px',
                height: '36px',
                borderRadius: '10px',
                background: 'var(--bg-surface)',
                border: '1px solid var(--border-subtle)',
                color: 'var(--text-primary)',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                flexShrink: 0
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = 'var(--accent-aqua)';
                e.currentTarget.style.color = 'var(--accent-aqua)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'var(--border-subtle)';
                e.currentTarget.style.color = 'var(--text-primary)';
              }}
            >
              <Bell size={16} color="var(--accent-aqua)" />
              {bulletinData?.notices?.length > 0 && (
                <span style={{
                  position: 'absolute',
                  top: '-4px',
                  right: '-4px',
                  fontSize: '0.62rem',
                  padding: '1px 5px',
                  borderRadius: '9999px',
                  background: 'linear-gradient(135deg, #0d9488 0%, #14b8a6 100%)',
                  color: '#ffffff',
                  fontWeight: 700,
                  boxShadow: '0 2px 6px rgba(13, 148, 136, 0.4)',
                  lineHeight: 1.2
                }}>
                  {bulletinData.notices.length}
                </span>
              )}
            </button>

            {/* Theme Switcher Toggle */}
            <button
              onClick={toggleTheme}
              title={`Switch to ${theme === 'light' ? 'Dark' : 'Light'} Mode`}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '36px',
                height: '36px',
                borderRadius: '10px',
                background: 'var(--bg-surface)',
                border: '1px solid var(--border-subtle)',
                color: 'var(--text-primary)',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                flexShrink: 0
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor = 'var(--accent-aqua)';
                e.currentTarget.style.color = 'var(--accent-aqua)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor = 'var(--border-subtle)';
                e.currentTarget.style.color = 'var(--text-primary)';
              }}
            >
              {theme === 'light' ? (
                <Moon size={15} color="var(--primary-cod-gray)" />
              ) : (
                <Sun size={15} color="#fbbf24" />
              )}
            </button>

            {/* Global Indian Language Dropdown */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              height: '36px',
              background: 'var(--bg-surface)',
              padding: '0 10px',
              borderRadius: '10px',
              border: '1px solid var(--border-subtle)',
              boxShadow: '0 2px 6px rgba(0,0,0,0.05)',
              flexShrink: 0
            }}>
              <Globe size={14} color="var(--accent-aqua)" style={{ flexShrink: 0 }} />
              <select
                value={currentLang}
                onChange={(e) => setCurrentLang(e.target.value)}
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--text-primary)',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  outline: 'none',
                  cursor: 'pointer',
                  maxWidth: '145px',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap'
                }}
              >
                {SUPPORTED_LANGUAGES.map((l) => (
                  <option key={l.code} value={l.code} style={{ background: 'var(--bg-card)', color: 'var(--text-primary)' }}>
                    {l.native} ({l.label})
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </header>

      {/* Live Gazette Regulatory Alert Strip */}
      {!isAlertDismissed && bulletinData?.notices?.length > 0 && (
        <div style={{
          background: 'linear-gradient(90deg, rgba(13, 148, 136, 0.12) 0%, rgba(20, 184, 166, 0.06) 50%, rgba(13, 148, 136, 0.12) 100%)',
          borderBottom: '1px solid rgba(13, 148, 136, 0.22)',
          padding: '6px 16px',
          display: 'flex',
          alignItems: 'center',
          fontSize: '0.75rem',
          color: 'var(--text-primary)',
          flexShrink: 0,
          width: '100%',
          boxSizing: 'border-box',
          overflow: 'hidden'
        }}>
          <div style={{ maxWidth: '1440px', margin: '0 auto', width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', minWidth: 0, overflow: 'hidden' }}>
              <span style={{
                background: 'var(--btn-primary-bg)',
                color: '#ffffff',
                fontSize: '0.64rem',
                fontWeight: 700,
                padding: '2px 7px',
                borderRadius: '5px',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px',
                flexShrink: 0,
                letterSpacing: '0.02em'
              }}>
                <span style={{ width: '5px', height: '5px', borderRadius: '50%', background: '#34d399', display: 'inline-block' }}></span>
                {t('gazette_alert')}
              </span>
              <span style={{ fontWeight: 700, color: 'var(--accent-aqua)', flexShrink: 0, fontFamily: 'JetBrains Mono, monospace' }}>
                {bulletinData.notices[0]?.standard_code}:
              </span>
              <span style={{ color: 'var(--text-secondary)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontWeight: 500 }}>
                {bulletinData.notices[0]?.title} — {bulletinData.notices[0]?.enforcement_date}
              </span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
              <button
                onClick={() => setIsBulletinOpen(true)}
                style={{
                  background: 'var(--bg-card)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '6px',
                  padding: '3px 9px',
                  fontSize: '0.72rem',
                  fontWeight: 600,
                  color: 'var(--accent-aqua)',
                  cursor: 'pointer',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '4px',
                  transition: 'all 0.15s ease'
                }}
              >
                {t('view_gazette_bulletin')} ({bulletinData.notices.length}) →
              </button>
              <button
                onClick={() => setIsAlertDismissed(true)}
                title="Dismiss Alert"
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--text-muted)',
                  cursor: 'pointer',
                  padding: '2px 5px',
                  fontSize: '0.8rem',
                  display: 'flex',
                  alignItems: 'center'
                }}
              >
                ✕
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Content Area */}
      <main style={{
        flex: activeTab === 'chat' ? 1 : '1 0 auto',
        minHeight: activeTab === 'chat' ? 0 : 'calc(100vh - 53px)',
        height: activeTab === 'chat' ? '100%' : 'auto',
        overflow: activeTab === 'chat' ? 'hidden' : 'visible',
        boxSizing: 'border-box',
        padding: activeTab === 'chat' ? '8px 20px' : '24px 20px',
        maxWidth: activeTab === 'chat' ? '1100px' : '1280px',
        margin: '0 auto',
        width: '100%',
        display: 'flex',
        flexDirection: 'column'
      }}>
        {/* Chat tab fills viewport exactly so typing bar is pinned at bottom with zero page scroll */}
        <div style={{
          display: activeTab === 'chat' ? 'flex' : 'none',
          flexDirection: 'column',
          height: '100%',
          flex: 1,
          minHeight: 0,
          overflow: 'hidden'
        }}>
          <ChatView
            onInspectEvidence={handleInspectEvidence}
            onOpenVoice={() => setIsVoiceModalOpen(true)}
            onStartJourney={(standardCode) => {
              setJourneyStandardId(standardCode);
              setActiveTab('journey');
              window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
            }}
            voiceTranscript={voiceTranscript}
            setVoiceTranscript={setVoiceTranscript}
            initialQuery={initialChatQuery}
            onClearInitialQuery={() => setInitialChatQuery('')}
            currentLang={currentLang}
            setCurrentLang={setCurrentLang}
            t={t}
          />
        </div>

        {activeTab === 'journey' && (
          <JourneyView
            initialStandardId={journeyStandardId}
            currentLang={currentLang}
            t={t}
          />
        )}

        {activeTab === 'verify' && <VerificationPanel currentLang={currentLang} t={t} />}

        {activeTab === 'labs' && <LabFinder currentLang={currentLang} t={t} />}

        {activeTab === 'directory' && (
          <DirectoryBrowser onSelectStandard={handleSelectStandardFromDirectory} currentLang={currentLang} t={t} />
        )}
      </main>

      {/* Official BIS Saathi Footer (Rendered on scrollable tabs, hidden on fixed chat) */}
      {activeTab !== 'chat' && (
        <Footer onNavigateTab={(tab) => {
          setActiveTab(tab);
          window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
        }} />
      )}

      {/* Source Inspector Modal */}
      <SourceInspectorModal
        isOpen={isSourceModalOpen}
        onClose={() => setIsSourceModalOpen(false)}
        evidence={selectedEvidence}
      />

      {/* Voice Transcript Modal */}
      <VoiceModal
        isOpen={isVoiceModalOpen}
        onClose={() => setIsVoiceModalOpen(false)}
        defaultLang={currentLang}
        onConfirm={(transcript) => {
          setVoiceTranscript(transcript);
        }}
      />

      {/* Live QCO & Gazette Bulletin Modal */}
      <QcoBulletinModal
        isOpen={isBulletinOpen}
        onClose={() => setIsBulletinOpen(false)}
        bulletinData={bulletinData}
        onRefresh={() => fetchBulletin(true)}
        isRefreshing={isBulletinRefreshing}
        onAskAboutStandard={(query) => {
          setInitialChatQuery(query);
          setActiveTab('chat');
          window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
        }}
        t={t}
      />
    </div>
  );
}
