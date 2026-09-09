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
  Moon
} from 'lucide-react';

import ChatView from './components/ChatView';
import JourneyView from './components/JourneyView';
import VerificationPanel from './components/VerificationPanel';
import LabFinder from './components/LabFinder';
import DirectoryBrowser from './components/DirectoryBrowser';
import SourceInspectorModal from './components/SourceInspectorModal';
import VoiceModal from './components/VoiceModal';
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
      minHeight: '100vh',
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
          padding: '8px 24px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '16px'
        }}>
          {/* Logo & Title */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexShrink: 0 }}>
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
            <div>
              <span className="font-heading" style={{ fontSize: '1.12rem', color: 'var(--text-primary)', fontWeight: 800, display: 'block', lineHeight: 1.1 }}>
                BIS Saathi
              </span>
              <span style={{ fontSize: '0.64rem', color: 'var(--text-muted)', display: 'block', marginTop: '1px' }}>
                National Standards &amp; Compliance Intelligence
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
            flexShrink: 0
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
                    padding: '0 11px',
                    borderRadius: '8px',
                    border: 'none',
                    background: isActive ? 'var(--btn-primary-bg)' : 'transparent',
                    color: isActive ? 'var(--btn-primary-text)' : 'var(--text-secondary)',
                    fontWeight: 600,
                    fontSize: '0.78rem',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                    whiteSpace: 'nowrap'
                  }}
                >
                  <Icon size={14} />
                  <span>{t(tab.labelKey)}</span>
                </button>
              );
            })}
          </nav>

          {/* Right Controls: Global Language Selector, Theme Switcher & Status */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
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
              <Globe size={14} color="var(--accent-aqua)" />
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
                  cursor: 'pointer'
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

      {/* Main Content Area */}
      <main style={{
        flex: '1 0 auto',
        minHeight: 'calc(100vh - 53px)',
        boxSizing: 'border-box',
        padding: activeTab === 'chat' ? '8px 20px' : '24px 20px',
        maxWidth: activeTab === 'chat' ? '1100px' : '1280px',
        margin: '0 auto',
        width: '100%',
        display: 'flex',
        flexDirection: 'column'
      }}>
        {/* Chat tab fills viewport height minus header and padding so footer is off-screen until scrolled */}
        <div style={{
          display: activeTab === 'chat' ? 'flex' : 'none',
          flexDirection: 'column',
          height: 'calc(100vh - 69px)',
          minHeight: '520px',
          flex: 1
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

      {/* Official BIS Saathi Footer */}
      <Footer onNavigateTab={(tab) => {
        setActiveTab(tab);
        window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
      }} />

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
    </div>
  );
}
