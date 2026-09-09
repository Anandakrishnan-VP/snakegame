import React, { useState, useEffect } from 'react';
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
  };

  return (
    <div style={{
      height: '100vh',
      maxHeight: '100vh',
      width: '100vw',
      overflow: 'hidden',
      display: 'flex',
      flexDirection: 'column',
      background: 'var(--bg-primary)',
      color: 'var(--text-primary)'
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
          maxWidth: '1280px',
          margin: '0 auto',
          padding: '12px 24px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '16px'
        }}>
          {/* Logo & Title */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <div style={{
              width: '42px',
              height: '42px',
              borderRadius: '10px',
              background: 'linear-gradient(135deg, #111315 0%, #0d9488 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#ffffff',
              boxShadow: '0 4px 14px rgba(13, 148, 136, 0.25)'
            }}>
              <Award size={24} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span className="font-heading" style={{ fontSize: '1.35rem', color: 'var(--text-primary)', fontWeight: 800 }}>
                  BIS Saathi
                </span>
              </div>
              <p style={{ margin: 0, fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                {t('subtitle')}
              </p>
            </div>
          </div>

          {/* Navigation Pills */}
          <nav style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            background: 'var(--bg-surface)',
            padding: '4px',
            borderRadius: '12px',
            border: '1px solid var(--border-subtle)',
            flexWrap: 'wrap'
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
                  onClick={() => setActiveTab(tab.id)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                    padding: '8px 14px',
                    borderRadius: '8px',
                    border: 'none',
                    background: isActive ? 'var(--btn-primary-bg)' : 'transparent',
                    color: isActive ? 'var(--btn-primary-text)' : 'var(--text-secondary)',
                    fontWeight: 600,
                    fontSize: '0.82rem',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease'
                  }}
                >
                  <Icon size={15} />
                  <span>{t(tab.labelKey)}</span>
                </button>
              );
            })}
          </nav>

          {/* Right Controls: Global Language Selector, Theme Switcher & Status */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            {/* Theme Switcher Toggle */}
            <button
              onClick={toggleTheme}
              title={`Switch to ${theme === 'light' ? 'Dark' : 'Light'} Mode`}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '7px 10px',
                borderRadius: '10px',
                background: 'var(--bg-surface)',
                border: '1px solid var(--border-subtle)',
                color: 'var(--text-primary)',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
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
                <Moon size={16} color="var(--primary-cod-gray)" />
              ) : (
                <Sun size={16} color="#fbbf24" />
              )}
            </button>

            {/* Global Indian Language Dropdown */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              background: 'var(--bg-surface)',
              padding: '4px 10px',
              borderRadius: '10px',
              border: '1px solid var(--border-subtle)',
              boxShadow: '0 2px 6px rgba(0,0,0,0.05)'
            }}>
              <Globe size={15} color="var(--accent-aqua)" />
              <select
                value={currentLang}
                onChange={(e) => setCurrentLang(e.target.value)}
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--text-primary)',
                  fontSize: '0.82rem',
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
        flex: 1,
        minHeight: 0,
        overflowY: activeTab === 'chat' ? 'hidden' : 'auto',
        padding: activeTab === 'chat' ? '6px 16px 6px 16px' : '20px',
        maxWidth: activeTab === 'chat' ? '1100px' : '1280px',
        margin: '0 auto',
        width: '100%',
        display: 'flex',
        flexDirection: 'column'
      }}>
        {/* Chat tab is kept mounted so navigating away and returning preserves chat conversation */}
        <div style={{
          display: activeTab === 'chat' ? 'flex' : 'none',
          flexDirection: 'column',
          height: '100%',
          flex: 1,
          minHeight: 0
        }}>
          <ChatView
            onInspectEvidence={handleInspectEvidence}
            onOpenVoice={() => setIsVoiceModalOpen(true)}
            onStartJourney={(standardCode) => {
              setJourneyStandardId(standardCode);
              setActiveTab('journey');
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
        window.scrollTo({ top: 0, behavior: 'smooth' });
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
