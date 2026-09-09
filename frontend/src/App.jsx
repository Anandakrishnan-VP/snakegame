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
  Compass
} from 'lucide-react';

import ChatView from './components/ChatView';
import JourneyView from './components/JourneyView';
import VerificationPanel from './components/VerificationPanel';
import LabFinder from './components/LabFinder';
import DirectoryBrowser from './components/DirectoryBrowser';
import SourceInspectorModal from './components/SourceInspectorModal';
import VoiceModal from './components/VoiceModal';
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
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top Navbar */}
      <header style={{
        backgroundColor: 'rgba(7, 9, 14, 0.85)',
        backdropFilter: 'blur(16px)',
        borderBottom: '1px solid var(--border-subtle)',
        position: 'sticky',
        top: 0,
        zIndex: 100
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
              background: 'linear-gradient(135deg, #f97316 0%, #1d4ed8 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#fff',
              boxShadow: '0 4px 15px rgba(249, 115, 22, 0.3)'
            }}>
              <Award size={24} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span className="font-heading" style={{ fontSize: '1.35rem', color: '#fff', fontWeight: 800 }}>
                  BIS Saathi
                </span>
                <span style={{
                  fontSize: '0.7rem',
                  padding: '2px 8px',
                  borderRadius: '4px',
                  background: 'rgba(249, 115, 22, 0.15)',
                  color: 'var(--accent-saffron)',
                  fontWeight: 700,
                  border: '1px solid rgba(249, 115, 22, 0.3)'
                }}>
                  SIH26107
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
            background: 'rgba(255, 255, 255, 0.04)',
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
                    background: isActive ? 'var(--accent-saffron)' : 'transparent',
                    color: isActive ? '#fff' : 'var(--text-secondary)',
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

          {/* Right Controls: Global Language Selector & Status */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            {/* Global Indian Language Dropdown */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              background: 'rgba(255, 255, 255, 0.06)',
              padding: '4px 10px',
              borderRadius: '10px',
              border: '1px solid rgba(249, 115, 22, 0.35)',
              boxShadow: '0 2px 8px rgba(0,0,0,0.2)'
            }}>
              <Globe size={15} color="var(--accent-saffron)" />
              <select
                value={currentLang}
                onChange={(e) => setCurrentLang(e.target.value)}
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: '#fff',
                  fontSize: '0.82rem',
                  fontWeight: 600,
                  outline: 'none',
                  cursor: 'pointer'
                }}
              >
                {SUPPORTED_LANGUAGES.map((l) => (
                  <option key={l.code} value={l.code} style={{ background: '#0b0f19', color: '#fff' }}>
                    {l.native} ({l.label})
                  </option>
                ))}
              </select>
            </div>

            {/* Backend Status Indicator */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{
                width: '8px',
                height: '8px',
                borderRadius: '50%',
                backgroundColor: apiStatus === 'online' ? '#10b981' : '#ef4444',
                boxShadow: apiStatus === 'online' ? '0 0 10px #10b981' : '0 0 10px #ef4444'
              }} />
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                {apiStatus === 'online' ? t('status_online') : t('status_connecting')}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main style={{ flex: 1, padding: '24px 20px', maxWidth: '1280px', margin: '0 auto', width: '100%' }}>
        {activeTab === 'chat' && (
          <div style={{ height: 'calc(100vh - 140px)', minHeight: '620px' }}>
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
              currentLang={currentLang}
              setCurrentLang={setCurrentLang}
              t={t}
            />
          </div>
        )}

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
