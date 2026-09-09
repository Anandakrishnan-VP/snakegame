import React, { useState, useRef, useEffect } from 'react';
import { 
  Send, 
  Mic, 
  Plus,
  Camera,
  Upload,
  X,
  Image as ImageIcon,
  ShieldCheck, 
  ArrowRight, 
  ExternalLink, 
  BookOpen, 
  Sparkles, 
  User, 
  Bot, 
  Building2, 
  Users, 
  Globe, 
  CornerDownRight, 
  HelpCircle,
  Clock,
  RotateCcw,
  Award
} from 'lucide-react';
import { SUPPORTED_LANGUAGES } from '../i18n/translations';
import { API_BASE_URL } from '../api/config';
import CameraModal from './CameraModal';

export default function ChatView({
  onInspectEvidence,
  onOpenVoice,
  onStartJourney,
  voiceTranscript,
  setVoiceTranscript,
  initialQuery,
  onClearInitialQuery,
  currentLang = 'en',
  setCurrentLang,
  t = (k) => k
}) {
  const DEFAULT_WELCOME_MESSAGE = {
    id: 'welcome',
    sender: 'assistant',
    answer: 'Namaste! I am BIS Saathi, your intelligent guide for Indian Standards, BIS certification schemes, testing laboratories, and consumer quality assurance.',
    what_it_means: 'I can recommend applicable standards for your product, clarify mandatory QCO regulations, verify licences, and locate NABL-accredited test facilities.',
    next_action: 'Type your product description below, choose a quick query, or toggle your persona for tailored guidance.',
    evidence_tag: {
      source_type: 'directory',
      reference: 'Bureau of Indian Standards',
      status: 'confirmed',
      clause_number: 'BIS Act 2016',
      clause_summary: 'The Bureau of Indian Standards is the National Standard Body of India established under the BIS Act 2016 for harmonious development of standardization, marking and quality certification.',
      verbatim_excerpt: 'The Bureau of Indian Standards is the National Standard Body of India established under the BIS Act 2016 for harmonious development of standardization, marking and quality certification.',
      source_url: 'https://www.bis.gov.in'
    }
  };

  const [messages, setMessages] = useState(() => {
    try {
      const saved = sessionStorage.getItem('bis_chat_messages');
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) {
          return parsed;
        }
      }
    } catch (e) {
      console.warn('Failed to load chat messages from sessionStorage', e);
    }
    return [DEFAULT_WELCOME_MESSAGE];
  });

  const [inputQuery, setInputQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [persona, setPersona] = useState(() => {
    try {
      return sessionStorage.getItem('bis_chat_persona') || 'msme';
    } catch (e) {
      return 'msme';
    }
  });
  const [activeTopic, setActiveTopic] = useState(() => {
    try {
      return sessionStorage.getItem('bis_chat_active_topic') || null;
    } catch (e) {
      return null;
    }
  });
  const [sessionId] = useState(() => {
    try {
      const saved = sessionStorage.getItem('bis_chat_session_id');
      if (saved) return saved;
      const newId = 'sess-' + Math.random().toString(36).substring(2, 9);
      sessionStorage.setItem('bis_chat_session_id', newId);
      return newId;
    } catch (e) {
      return 'sess-' + Math.random().toString(36).substring(2, 9);
    }
  });

  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [attachedImage, setAttachedImage] = useState(null);
  const [isPlusMenuOpen, setIsPlusMenuOpen] = useState(false);
  const [zoomedImage, setZoomedImage] = useState(null);
  const fileInputRef = useRef(null);
  const plusMenuRef = useRef(null);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (plusMenuRef.current && !plusMenuRef.current.contains(e.target)) {
        setIsPlusMenuOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleFileUpload = (e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    if (!file.type.startsWith('image/')) {
      alert('Please upload an image file (JPEG, PNG, WEBP).');
      return;
    }
    const reader = new FileReader();
    reader.onload = (ev) => {
      setAttachedImage(ev.target.result);
      setIsPlusMenuOpen(false);
    };
    reader.readAsDataURL(file);
    e.target.value = '';
  };

  const msmePrompts = [
    { label: 'Bottle Manufacturing', query: 'I am manufacturing stainless steel vacuum water bottles for kids. What are the rules?' },
    { label: 'Toy Compliance', query: 'What are the mandatory quality standards and test requirements to manufacture toys?' },
    { label: 'Scheme-I Steps', query: 'What are the exact factory audit and Scheme-I steps for ISI certification?' },
    { label: 'MSME Concessions', query: 'What fee concessions are available for MSMEs and startups in BIS certification?' },
    { label: 'Hindi MSME Mode', query: 'खिलौना निर्माण के लिए बीआईएस प्रमाणन प्रक्रिया क्या है?' }
  ];

  const consumerPrompts = [
    { label: 'Bottle Safety Check', query: 'How can I verify if a stainless steel water bottle is safe and genuine before buying?' },
    { label: 'Toy Safety for Kids', query: 'Are plastic toys safe for toddlers and how do I check the ISI mark?' },
    { label: 'Check Gold Hallmark', query: 'How do I verify 6-digit HUID gold hallmark on jewellery using BIS Care app?' },
    { label: 'Report Defective Item', query: 'How can I file a complaint against a defective or fake ISI-marked product?' },
    { label: 'Hindi Consumer Mode', query: 'सोने के आभूषणों पर हॉलमार्क HUID की जांच कैसे करें?' }
  ];

  const quickPrompts = persona === 'consumer' ? consumerPrompts : msmePrompts;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  // Persist messages across page navigation and reloads until the site is closed
  useEffect(() => {
    try {
      sessionStorage.setItem('bis_chat_messages', JSON.stringify(messages));
    } catch (e) {
      console.warn('Failed to save messages to sessionStorage', e);
    }
  }, [messages]);

  useEffect(() => {
    try {
      sessionStorage.setItem('bis_chat_persona', persona);
    } catch (e) {}
  }, [persona]);

  useEffect(() => {
    try {
      if (activeTopic) {
        sessionStorage.setItem('bis_chat_active_topic', activeTopic);
      } else {
        sessionStorage.removeItem('bis_chat_active_topic');
      }
    } catch (e) {}
  }, [activeTopic]);

  const handleResetChat = () => {
    const newSessionId = 'sess-' + Math.random().toString(36).substring(2, 9);
    try {
      sessionStorage.setItem('bis_chat_session_id', newSessionId);
      sessionStorage.removeItem('bis_chat_active_topic');
      sessionStorage.setItem('bis_chat_messages', JSON.stringify([DEFAULT_WELCOME_MESSAGE]));
    } catch (e) {}
    setActiveTopic(null);
    setMessages([DEFAULT_WELCOME_MESSAGE]);
  };

  useEffect(() => {
    if (voiceTranscript) {
      sendMessage(voiceTranscript);
      setVoiceTranscript('');
    }
  }, [voiceTranscript]);

  useEffect(() => {
    if (initialQuery) {
      sendMessage(initialQuery);
      if (onClearInitialQuery) {
        onClearInitialQuery();
      }
    }
  }, [initialQuery]);

  const sendMessage = async (queryText) => {
    const rawText = queryText || inputQuery;
    const hasImage = Boolean(attachedImage);

    if (!rawText.trim() && !hasImage) return;
    if (loading) return;

    const imageToSend = attachedImage;
    const textToSend = rawText.trim() || (hasImage ? "Please identify what product is shown in this image, check the applicable Indian Standard (IS code), inspect any visible or missing ISI marks/CM/L licence numbers, and provide compliance details." : "");

    const userMsg = {
      id: 'user-' + Date.now(),
      sender: 'user',
      text: textToSend,
      image: imageToSend || null
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputQuery('');
    setAttachedImage(null);
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: textToSend,
          image_base64: imageToSend || null,
          session_id: sessionId,
          persona: persona,
          language: currentLang
        })
      });

      const data = await res.json();

      if (!data || !data.answer) {
        throw new Error(data?.detail || data?.error || "Incomplete response from BIS Saathi service.");
      }

      const assistantMsg = {
        id: 'asst-' + Date.now(),
        sender: 'assistant',
        answer: data.answer,
        what_it_means: data.what_it_means,
        next_action: data.next_action,
        evidence_tag: data.evidence_tag,
        from_cache: data.from_cache,
        provider: data.provider,
        active_topic: data.active_topic,
        persona: data.persona || persona
      };

      if (data.active_topic) {
        setActiveTopic(data.active_topic);
      }

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: 'err-' + Date.now(),
          sender: 'assistant',
          answer: 'Unable to connect to the BIS Saathi backend service.',
          what_it_means: 'The backend service may be starting up or temporarily unreachable.',
          next_action: 'Please try again in a few moments or check your connection.',
          evidence_tag: {
            source_type: 'directory',
            reference: 'BIS Saathi Service',
            status: 'not determined',
            verbatim_excerpt: 'Connection failed.',
            source_url: '#'
          }
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', maxWidth: '960px', margin: '0 auto', width: '100%' }}>
      {/* Header Bar Controls */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '12px',
        padding: '12px 18px',
        background: 'var(--bg-glass)',
        borderBottom: '1px solid var(--border-subtle)',
        borderRadius: '12px 12px 0 0',
        backdropFilter: 'blur(12px)',
        boxShadow: 'var(--shadow-card)'
      }}>
        {/* Active Topic Tag */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Session Topic:</span>
          {activeTopic ? (
            <span style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              padding: '3px 10px',
              background: 'var(--accent-blue-glow)',
              border: '1px solid var(--accent-blue)',
              borderRadius: '9999px',
              color: 'var(--accent-blue)',
              fontSize: '0.8rem',
              fontWeight: 700,
              fontFamily: 'JetBrains Mono'
            }}>
              <BookOpen size={13} /> {t('active_topic_badge')} {activeTopic}
            </span>
          ) : (
            <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', fontStyle: 'italic' }}>{t('topic_inquiry')}</span>
          )}
        </div>

        {/* Persona & Language Selectors */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
          {/* Persona Toggle */}
          <div style={{
            display: 'inline-flex',
            background: 'var(--bg-surface)',
            borderRadius: '8px',
            padding: '2px',
            border: '1px solid var(--border-subtle)'
          }}>
            <button
              onClick={() => setPersona('msme')}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '5px',
                padding: '4px 10px',
                borderRadius: '6px',
                border: 'none',
                background: persona === 'msme' ? 'var(--accent-saffron)' : 'transparent',
                color: persona === 'msme' ? '#ffffff' : 'var(--text-secondary)',
                fontSize: '0.78rem',
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              <Building2 size={13} /> {t('persona_msme')}
            </button>
            <button
              onClick={() => setPersona('consumer')}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '5px',
                padding: '4px 10px',
                borderRadius: '6px',
                border: 'none',
                background: persona === 'consumer' ? 'var(--accent-saffron)' : 'transparent',
                color: persona === 'consumer' ? '#ffffff' : 'var(--text-secondary)',
                fontSize: '0.78rem',
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              <Users size={13} /> {t('persona_consumer')}
            </button>
          </div>

          {/* Language Selector in Chat Header */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
            background: 'var(--bg-surface)',
            padding: '2px 8px',
            borderRadius: '8px',
            border: '1px solid var(--border-subtle)'
          }}>
            <Globe size={14} color="var(--accent-aqua)" />
            <select
              value={currentLang}
              onChange={(e) => setCurrentLang && setCurrentLang(e.target.value)}
              style={{
                padding: '3px 4px',
                borderRadius: '6px',
                background: 'transparent',
                border: 'none',
                color: 'var(--text-primary)',
                fontSize: '0.78rem',
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

          {/* New / Reset Chat Button */}
          <button
            onClick={handleResetChat}
            title="Clear chat and start fresh"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '5px',
              padding: '4px 10px',
              borderRadius: '6px',
              background: 'var(--btn-secondary-bg)',
              border: '1px solid var(--border-subtle)',
              color: 'var(--text-secondary)',
              fontSize: '0.78rem',
              fontWeight: 500,
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
          >
            <RotateCcw size={13} /> New Chat
          </button>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '20px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {messages.map((msg) => (
          <div key={msg.id} className="animate-fade-in" style={{
            display: 'flex',
            justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start'
          }}>
            {msg.sender === 'user' ? (
              /* User Bubble */
              <div style={{
                maxWidth: '75%',
                padding: '14px 18px',
                background: 'linear-gradient(135deg, #111315 0%, #1e2629 100%)',
                boxShadow: '0 4px 14px rgba(17, 19, 21, 0.25)',
                border: '1px solid rgba(207, 220, 220, 0.25)',
                borderRadius: '16px 16px 4px 16px',
                color: '#ffffff',
                fontSize: '0.96rem',
                lineHeight: 1.5,
                fontWeight: 500
              }}>
                {msg.image && (
                  <div style={{ marginBottom: msg.text ? '10px' : '0' }}>
                    <img
                      src={msg.image}
                      alt="Uploaded item"
                      onClick={() => setZoomedImage(msg.image)}
                      title="Click to enlarge photo"
                      style={{
                        maxWidth: '240px',
                        maxHeight: '200px',
                        borderRadius: '10px',
                        objectFit: 'cover',
                        display: 'block',
                        cursor: 'zoom-in',
                        border: '1px solid rgba(255, 255, 255, 0.25)',
                        boxShadow: '0 4px 10px rgba(0,0,0,0.35)'
                      }}
                    />
                    <div style={{ marginTop: '5px', display: 'flex', alignItems: 'center', gap: '5px' }}>
                      <span style={{
                        fontSize: '0.72rem',
                        color: '#99f6e4',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '4px',
                        fontWeight: 600
                      }}>
                        <Sparkles size={11} /> {t('vlm_badge') || 'Vision AI Inspected'}
                      </span>
                    </div>
                  </div>
                )}
                {msg.text && <div>{msg.text}</div>}
              </div>
            ) : (
              /* Assistant 4-Part Answer Card */
              <div className="glass-panel" style={{
                maxWidth: '88%',
                borderRadius: '16px',
                overflow: 'hidden',
                background: 'var(--bg-card)',
                boxShadow: 'var(--shadow-card)',
                border: '1px solid var(--border-subtle)'
              }}>
                {/* Persona Context Banner */}
                <div style={{
                  padding: '9px 20px',
                  background: msg.persona === 'consumer'
                    ? 'rgba(5, 150, 105, 0.08)'
                    : 'rgba(234, 88, 12, 0.08)',
                  borderBottom: '1px solid var(--border-subtle)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  flexWrap: 'wrap',
                  gap: '8px'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    {msg.persona === 'consumer' ? (
                      <span style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '6px',
                        padding: '3px 10px',
                        borderRadius: '9999px',
                        fontSize: '0.74rem',
                        fontWeight: 700,
                        color: '#059669',
                        background: 'rgba(16, 185, 129, 0.15)',
                        border: '1px solid rgba(16, 185, 129, 0.35)'
                      }}>
                        <Users size={12} /> Consumer Safety & Buying Advisory
                      </span>
                    ) : (
                      <span style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '6px',
                        padding: '3px 10px',
                        borderRadius: '9999px',
                        fontSize: '0.74rem',
                        fontWeight: 700,
                        color: 'var(--accent-saffron)',
                        background: 'var(--accent-saffron-glow)',
                        border: '1px solid var(--border-active)'
                      }}>
                        <Building2 size={12} /> MSME Compliance & Licensing Advisory
                      </span>
                    )}
                  </div>
                  {msg.from_cache && (
                    <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <Clock size={11} /> Cached Result
                    </span>
                  )}
                </div>

                {/* 1. Direct Answer */}
                <div style={{ padding: '18px 20px', background: 'transparent', borderBottom: '1px solid var(--border-subtle)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                    <div style={{
                      width: '24px',
                      height: '24px',
                      borderRadius: '50%',
                      background: msg.persona === 'consumer' ? 'var(--accent-emerald)' : 'var(--accent-saffron)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: '#ffffff',
                      fontSize: '0.75rem',
                      fontWeight: 700
                    }}>
                      {msg.persona === 'consumer' ? '🛡️' : 'IS'}
                    </div>
                    <span style={{
                      fontSize: '0.82rem',
                      fontWeight: 700,
                      color: msg.persona === 'consumer' ? 'var(--accent-emerald)' : 'var(--accent-saffron)',
                      textTransform: 'uppercase',
                      letterSpacing: '0.04em'
                    }}>
                      {msg.persona === 'consumer' ? 'Product Safety & Quality Summary' : 'Industrial Compliance Answer'}
                    </span>
                  </div>
                  <p style={{ margin: 0, fontSize: '0.98rem', color: 'var(--text-primary)', lineHeight: 1.6, fontWeight: 500 }}>
                    {msg.answer}
                  </p>
                </div>

                {/* 2. What this means */}
                {msg.what_it_means && (
                  <div style={{ padding: '14px 20px', background: 'var(--bg-surface)', borderBottom: '1px solid var(--border-subtle)' }}>
                    <span style={{
                      fontSize: '0.78rem',
                      color: msg.persona === 'consumer' ? 'var(--accent-emerald)' : 'var(--accent-saffron)',
                      textTransform: 'uppercase',
                      letterSpacing: '0.04em',
                      fontWeight: 600,
                      display: 'block',
                      marginBottom: '4px'
                    }}>
                      {msg.persona === 'consumer' ? '🔍 What to Check Before Buying (Packaging & Safety)' : '🏭 Factory & Scheme Implications (MSME & Audit)'}
                    </span>
                    <p style={{ margin: 0, fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                      {msg.what_it_means}
                    </p>
                  </div>
                )}

                {/* 3. What to do next */}
                {msg.next_action && (
                  <div style={{
                    padding: '14px 20px',
                    background: msg.persona === 'consumer' ? 'rgba(5, 150, 105, 0.04)' : 'rgba(2, 132, 199, 0.04)',
                    borderBottom: '1px solid var(--border-subtle)'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <CornerDownRight size={14} color={msg.persona === 'consumer' ? '#059669' : '#0284c7'} />
                      <span style={{
                        fontSize: '0.78rem',
                        color: msg.persona === 'consumer' ? '#059669' : '#0284c7',
                        textTransform: 'uppercase',
                        letterSpacing: '0.04em',
                        fontWeight: 600
                      }}>
                        {msg.persona === 'consumer' ? 'Citizen Action: Verify on BIS Care App / Grievance' : 'Manufacturer Roadmap: Form V & Testing Action'}
                      </span>
                    </div>
                    <p style={{ margin: '4px 0 0', fontSize: '0.9rem', color: 'var(--text-primary)', lineHeight: 1.5, fontWeight: 500 }}>
                      {msg.next_action}
                    </p>

                    {onStartJourney && msg.persona !== 'consumer' && (msg.active_topic || (msg.evidence_tag && msg.evidence_tag.reference && msg.evidence_tag.reference.includes('IS '))) && (
                      <div style={{ marginTop: '12px' }}>
                        <button
                          onClick={() => onStartJourney(msg.active_topic || msg.evidence_tag.reference)}
                          style={{
                            background: 'var(--accent-saffron)',
                            border: 'none',
                            color: '#ffffff',
                            borderRadius: '6px',
                            padding: '6px 14px',
                            fontSize: '0.82rem',
                            fontWeight: 600,
                            cursor: 'pointer',
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '6px',
                            transition: 'all 0.2s ease',
                            boxShadow: '0 2px 10px var(--accent-saffron-glow)'
                          }}
                        >
                          <Award size={14} /> Start Certification Journey Wizard <ArrowRight size={12} />
                        </button>
                      </div>
                    )}
                  </div>
                )}

                {/* 4. Clickable Source & Evidence Tag */}
                {msg.evidence_tag && (
                  <div style={{
                    padding: '12px 20px',
                    background: 'var(--bg-surface)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    flexWrap: 'wrap',
                    gap: '10px'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{t('card_source')}:</span>
                      <span style={{
                        fontSize: '0.8rem',
                        fontWeight: 600,
                        color: 'var(--accent-blue-deep)',
                        fontFamily: 'JetBrains Mono'
                      }}>
                        {msg.evidence_tag.reference || 'BIS Database'}
                      </span>
                      <span className={msg.evidence_tag.status === 'confirmed' ? 'badge-confirmed' : msg.evidence_tag.status === 'needs verification' ? 'badge-verification' : 'badge-not-determined'} style={{
                        fontSize: '0.72rem',
                        padding: '2px 8px',
                        borderRadius: '9999px',
                        fontWeight: 600
                      }}>
                        {msg.evidence_tag.status ? (msg.evidence_tag.status === 'confirmed' ? t('tag_confirmed') : t('tag_needs_ver')) : t('tag_confirmed')}
                      </span>
                    </div>

                    <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap' }}>
                      {msg.evidence_tag.source_url && (
                        <a
                          href={msg.evidence_tag.source_url}
                          target="_blank"
                          rel="noreferrer"
                          style={{
                            background: 'var(--accent-blue-glow)',
                            border: '1px solid var(--accent-blue)',
                            borderRadius: '6px',
                            color: 'var(--accent-blue)',
                            padding: '4px 10px',
                            fontSize: '0.78rem',
                            fontWeight: 600,
                            textDecoration: 'none',
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '5px',
                            transition: 'all 0.2s ease'
                          }}
                          title="Open official government source document or portal"
                        >
                          <ExternalLink size={12} /> Direct Document
                        </a>
                      )}
                      <button
                        onClick={() => onInspectEvidence(msg.evidence_tag)}
                        style={{
                          background: 'var(--bg-card)',
                          border: '1px solid var(--border-subtle)',
                          borderRadius: '6px',
                          color: 'var(--accent-aqua)',
                          padding: '4px 12px',
                          fontSize: '0.78rem',
                          fontWeight: 600,
                          cursor: 'pointer',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '5px',
                          transition: 'all 0.2s ease'
                        }}
                      >
                        <BookOpen size={13} /> {t('btn_inspect')} <ArrowRight size={12} />
                      </button>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div style={{ display: 'flex', gap: '8px', padding: '12px 18px', background: 'var(--bg-card)', border: '1px solid var(--border-subtle)', borderRadius: '12px', width: 'fit-content' }}>
            <Sparkles size={18} color="var(--accent-aqua)" className="animate-spin" />
            <span style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>Consulting BIS knowledge base & compliance chain...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompt Chips */}
      <div style={{ padding: '8px 18px', display: 'flex', gap: '8px', overflowX: 'auto', background: 'var(--bg-surface)', borderTop: '1px solid var(--border-subtle)' }}>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', alignSelf: 'center', whiteSpace: 'nowrap' }}>{t('quick_prompt_title')}</span>
        {quickPrompts.map((qp, idx) => (
          <button
            key={idx}
            onClick={() => sendMessage(qp.query)}
            style={{
              whiteSpace: 'nowrap',
              fontSize: '0.78rem',
              padding: '5px 12px',
              borderRadius: '9999px',
              background: 'var(--bg-card)',
              border: '1px solid var(--border-subtle)',
              color: 'var(--text-secondary)',
              cursor: 'pointer',
              transition: 'all 0.15s ease',
              boxShadow: '0 1px 3px rgba(0,0,0,0.04)'
            }}
          >
            {qp.label}
          </button>
        ))}
      </div>

      {/* Input Bar */}
      <div style={{ padding: '16px', background: 'var(--bg-glass)', borderTop: '1px solid var(--border-subtle)', borderRadius: '0 0 12px 12px' }}>
        {/* Attached Image Preview Strip */}
        {attachedImage && (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            marginBottom: '12px',
            padding: '8px 12px',
            background: 'var(--bg-card)',
            borderRadius: '10px',
            border: '1px solid var(--border-subtle)',
            boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
            width: 'fit-content'
          }}>
            <div style={{ position: 'relative' }}>
              <img
                src={attachedImage}
                alt="Selected preview"
                style={{
                  width: '52px',
                  height: '52px',
                  borderRadius: '8px',
                  objectFit: 'cover',
                  border: '1px solid var(--border-subtle)',
                  display: 'block'
                }}
              />
              <button
                type="button"
                onClick={() => setAttachedImage(null)}
                title={t('vlm_remove') || 'Remove photo'}
                style={{
                  position: 'absolute',
                  top: '-6px',
                  right: '-6px',
                  background: 'var(--cod-gray)',
                  color: '#ffffff',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '50%',
                  width: '20px',
                  height: '20px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  cursor: 'pointer',
                  padding: 0,
                  boxShadow: '0 2px 4px rgba(0,0,0,0.3)'
                }}
              >
                <X size={12} />
              </button>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
              <span style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                {t('vlm_preview_title') || 'Attached for Quality & ISI/Hallmark Inspection'}
              </span>
              <span style={{ fontSize: '0.74rem', color: 'var(--accent-aqua)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <Sparkles size={11} /> Vision AI ready • Press send or type specific questions
              </span>
            </div>
          </div>
        )}

        {/* Hidden File Input */}
        <input
          type="file"
          ref={fileInputRef}
          accept="image/*"
          style={{ display: 'none' }}
          onChange={handleFileUpload}
        />

        <form onSubmit={(e) => { e.preventDefault(); sendMessage(); }} style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          {/* Voice Button */}
          <button
            type="button"
            onClick={onOpenVoice}
            title={t('chat_listening')}
            style={{
              padding: '12px',
              borderRadius: '10px',
              background: 'var(--bg-surface)',
              border: '1px solid var(--border-subtle)',
              color: 'var(--accent-aqua)',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 1px 3px rgba(0,0,0,0.04)',
              transition: 'all 0.15s ease'
            }}
          >
            <Mic size={20} />
          </button>

          {/* + Button for Camera and Files */}
          <div style={{ position: 'relative' }} ref={plusMenuRef}>
            <button
              type="button"
              id="btn-vlm-plus"
              onClick={() => setIsPlusMenuOpen((prev) => !prev)}
              title={t('btn_attach') || 'Attach Photo / Document'}
              style={{
                padding: '12px',
                borderRadius: '10px',
                background: isPlusMenuOpen || attachedImage ? 'var(--accent-aqua)' : 'var(--bg-surface)',
                border: '1px solid var(--border-subtle)',
                color: isPlusMenuOpen || attachedImage ? '#ffffff' : 'var(--accent-aqua)',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 1px 3px rgba(0,0,0,0.04)',
                transition: 'all 0.15s ease'
              }}
            >
              <Plus size={20} />
            </button>

            {/* Popover Menu with Camera and Add Files */}
            {isPlusMenuOpen && (
              <div style={{
                position: 'absolute',
                bottom: '125%',
                left: 0,
                background: 'var(--bg-card)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '12px',
                boxShadow: '0 12px 28px rgba(0, 0, 0, 0.25)',
                padding: '6px',
                display: 'flex',
                flexDirection: 'column',
                gap: '4px',
                minWidth: '230px',
                zIndex: 60,
                animation: 'fadeIn 0.15s ease-out'
              }}>
                <button
                  type="button"
                  id="btn-vlm-camera"
                  onClick={() => {
                    setIsPlusMenuOpen(false);
                    setIsCameraOpen(true);
                  }}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    padding: '10px 14px',
                    background: 'transparent',
                    border: 'none',
                    borderRadius: '8px',
                    color: 'var(--text-primary)',
                    fontSize: '0.88rem',
                    fontWeight: 500,
                    cursor: 'pointer',
                    textAlign: 'left',
                    transition: 'background 0.15s ease'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.background = 'var(--bg-surface)'}
                  onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                >
                  <div style={{
                    width: '32px',
                    height: '32px',
                    borderRadius: '8px',
                    background: 'rgba(13, 148, 136, 0.12)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'var(--accent-aqua)'
                  }}>
                    <Camera size={18} />
                  </div>
                  <div>
                    <div style={{ fontWeight: 600 }}>{t('btn_camera') || 'Camera'}</div>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Take live photo</div>
                  </div>
                </button>

                <button
                  type="button"
                  id="btn-vlm-upload"
                  onClick={() => {
                    setIsPlusMenuOpen(false);
                    if (fileInputRef.current) {
                      fileInputRef.current.click();
                    }
                  }}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    padding: '10px 14px',
                    background: 'transparent',
                    border: 'none',
                    borderRadius: '8px',
                    color: 'var(--text-primary)',
                    fontSize: '0.88rem',
                    fontWeight: 500,
                    cursor: 'pointer',
                    textAlign: 'left',
                    transition: 'background 0.15s ease'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.background = 'var(--bg-surface)'}
                  onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                >
                  <div style={{
                    width: '32px',
                    height: '32px',
                    borderRadius: '8px',
                    background: 'rgba(13, 148, 136, 0.12)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'var(--accent-aqua)'
                  }}>
                    <Upload size={18} />
                  </div>
                  <div>
                    <div style={{ fontWeight: 600 }}>{t('btn_upload') || 'Add Files'}</div>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Upload from device</div>
                  </div>
                </button>
              </div>
            )}
          </div>

          <input
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            placeholder={
              attachedImage
                ? "Optional: ask specific question or press send to analyze..."
                : persona === 'consumer'
                  ? t('chat_placeholder_consumer')
                  : t('chat_placeholder_msme')
            }
            style={{
              flex: 1,
              padding: '14px 18px',
              backgroundColor: 'var(--bg-input)',
              border: '1px solid var(--border-strong)',
              borderRadius: '10px',
              color: 'var(--text-primary)',
              fontSize: '0.95rem',
              outline: 'none',
              boxShadow: '0 1px 3px rgba(0,0,0,0.03)'
            }}
          />

          <button
            type="submit"
            disabled={(!inputQuery.trim() && !attachedImage) || loading}
            className="btn-primary"
            style={{
              padding: '14px 22px',
              borderRadius: '10px',
              opacity: (!inputQuery.trim() && !attachedImage) || loading ? 0.6 : 1,
              cursor: (!inputQuery.trim() && !attachedImage) || loading ? 'not-allowed' : 'pointer'
            }}
          >
            <Send size={18} />
          </button>
        </form>

        <p style={{ margin: '8px 0 0', fontSize: '0.72rem', color: 'var(--text-muted)', textAlign: 'center' }}>
          {t('chat_disclaimer')}
        </p>
      </div>

      {/* Live Camera Modal */}
      <CameraModal
        isOpen={isCameraOpen}
        onClose={() => setIsCameraOpen(false)}
        onCapture={(photoDataUrl) => setAttachedImage(photoDataUrl)}
        onCapturePhoto={(photoDataUrl) => setAttachedImage(photoDataUrl)}
        onSwitchToFileUpload={() => {
          if (fileInputRef.current) {
            fileInputRef.current.click();
          }
        }}
      />

      {/* Full Size Image Lightbox */}
      {zoomedImage && (
        <div
          onClick={() => setZoomedImage(null)}
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0, 0, 0, 0.85)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 9999,
            padding: '24px',
            backdropFilter: 'blur(4px)',
            cursor: 'zoom-out'
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{ position: 'relative', maxWidth: '90vw', maxHeight: '90vh' }}
          >
            <img
              src={zoomedImage}
              alt="Enlarged inspection"
              style={{
                maxWidth: '100%',
                maxHeight: '85vh',
                borderRadius: '12px',
                boxShadow: '0 20px 50px rgba(0,0,0,0.6)',
                objectFit: 'contain',
                border: '1px solid rgba(255,255,255,0.2)'
              }}
            />
            <button
              type="button"
              onClick={() => setZoomedImage(null)}
              style={{
                position: 'absolute',
                top: '-12px',
                right: '-12px',
                background: 'var(--cod-gray)',
                color: '#ffffff',
                border: '1px solid rgba(255,255,255,0.3)',
                borderRadius: '50%',
                width: '32px',
                height: '32px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                boxShadow: '0 4px 10px rgba(0,0,0,0.4)'
              }}
            >
              <X size={18} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
