import React, { useState, useRef, useEffect } from 'react';
import { 
  Send, 
  Mic, 
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

export default function ChatView({
  onInspectEvidence,
  onOpenVoice,
  onStartJourney,
  voiceTranscript,
  setVoiceTranscript,
  initialQuery,
  currentLang = 'en',
  setCurrentLang,
  t = (k) => k
}) {
  const [messages, setMessages] = useState([
    {
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
    }
  ]);

  const [inputQuery, setInputQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [persona, setPersona] = useState('msme'); // 'msme', 'consumer', 'general'
  const [activeTopic, setActiveTopic] = useState(null);
  const [sessionId] = useState(() => 'sess-' + Math.random().toString(36).substring(2, 9));

  const messagesEndRef = useRef(null);

  const quickPrompts = [
    { label: 'Bottle Rules', query: 'I am manufacturing stainless steel vacuum water bottles for kids. What are the rules?' },
    { label: 'Toy Safety', query: 'What are the mandatory quality standards and test requirements for toys?' },
    { label: 'Pronoun Lab Test', query: 'Where is the testing lab for it in Mumbai?' },
    { label: 'MSME Concessions', query: 'What fee concessions are available for MSMEs and startups in BIS certification?' },
    { label: 'Hindi Mode', query: 'खिलौनों के लिए क्या नियम हैं?' }
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  useEffect(() => {
    if (voiceTranscript) {
      sendMessage(voiceTranscript);
      setVoiceTranscript('');
    }
  }, [voiceTranscript]);

  useEffect(() => {
    if (initialQuery) {
      sendMessage(initialQuery);
    }
  }, [initialQuery]);

  const sendMessage = async (queryText) => {
    const textToSend = queryText || inputQuery;
    if (!textToSend.trim() || loading) return;

    const userMsg = {
      id: 'user-' + Date.now(),
      sender: 'user',
      text: textToSend
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputQuery('');
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: textToSend,
          session_id: sessionId,
          persona: persona,
          language: currentLang
        })
      });

      const data = await res.json();

      const assistantMsg = {
        id: 'asst-' + Date.now(),
        sender: 'assistant',
        answer: data.answer,
        what_it_means: data.what_it_means,
        next_action: data.next_action,
        evidence_tag: data.evidence_tag,
        from_cache: data.from_cache,
        provider: data.provider,
        active_topic: data.active_topic
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
        backdropFilter: 'blur(12px)'
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
              background: 'rgba(56, 189, 248, 0.15)',
              border: '1px solid rgba(56, 189, 248, 0.3)',
              borderRadius: '9999px',
              color: '#38bdf8',
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
            background: 'rgba(0, 0, 0, 0.3)',
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
                color: persona === 'msme' ? '#fff' : 'var(--text-secondary)',
                fontSize: '0.78rem',
                fontWeight: 600,
                cursor: 'pointer'
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
                color: persona === 'consumer' ? '#fff' : 'var(--text-secondary)',
                fontSize: '0.78rem',
                fontWeight: 600,
                cursor: 'pointer'
              }}
            >
              <Users size={13} /> {t('persona_consumer')}
            </button>
          </div>

          {/* Language Selector in Chat Header */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <Globe size={14} color="var(--accent-saffron)" />
            <select
              value={currentLang}
              onChange={(e) => setCurrentLang && setCurrentLang(e.target.value)}
              style={{
                padding: '4px 8px',
                borderRadius: '6px',
                background: 'rgba(0, 0, 0, 0.4)',
                border: '1px solid var(--border-subtle)',
                color: '#fff',
                fontSize: '0.78rem',
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
                background: 'linear-gradient(135deg, rgba(249, 115, 22, 0.25) 0%, rgba(249, 115, 22, 0.15) 100%)',
                border: '1px solid rgba(249, 115, 22, 0.3)',
                borderRadius: '16px 16px 4px 16px',
                color: '#fff',
                fontSize: '0.96rem',
                lineHeight: 1.5
              }}>
                {msg.text}
              </div>
            ) : (
              /* Assistant 4-Part Answer Card */
              <div className="glass-panel" style={{
                maxWidth: '88%',
                borderRadius: '16px',
                overflow: 'hidden',
                boxShadow: 'var(--shadow-card)'
              }}>
                {/* 1. Direct Answer */}
                <div style={{ padding: '18px 20px', background: 'rgba(255, 255, 255, 0.02)', borderBottom: '1px solid var(--border-subtle)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                    <div style={{
                      width: '24px',
                      height: '24px',
                      borderRadius: '50%',
                      background: 'var(--accent-saffron)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: '#fff',
                      fontSize: '0.75rem',
                      fontWeight: 700
                    }}>
                      IS
                    </div>
                    <span style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--accent-saffron)' }}>{t('card_answer')}</span>
                    {msg.from_cache && (
                      <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <Clock size={11} /> Cached Result
                      </span>
                    )}
                  </div>
                  <p style={{ margin: 0, fontSize: '0.98rem', color: '#fff', lineHeight: 1.6, fontWeight: 500 }}>
                    {msg.answer}
                  </p>
                </div>

                {/* 2. What this means */}
                {msg.what_it_means && (
                  <div style={{ padding: '14px 20px', background: 'rgba(0, 0, 0, 0.2)', borderBottom: '1px solid var(--border-subtle)' }}>
                    <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em', fontWeight: 600 }}>
                      {t('card_meaning')}
                    </span>
                    <p style={{ margin: '4px 0 0', fontSize: '0.9rem', color: '#cbd5e1', lineHeight: 1.5 }}>
                      {msg.what_it_means}
                    </p>
                  </div>
                )}

                {/* 3. What to do next */}
                {msg.next_action && (
                  <div style={{ padding: '14px 20px', background: 'rgba(56, 189, 248, 0.04)', borderBottom: '1px solid var(--border-subtle)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <CornerDownRight size={14} color="#38bdf8" />
                      <span style={{ fontSize: '0.78rem', color: '#38bdf8', textTransform: 'uppercase', letterSpacing: '0.04em', fontWeight: 600 }}>
                        {t('card_action')}
                      </span>
                    </div>
                    <p style={{ margin: '4px 0 0', fontSize: '0.9rem', color: '#e2e8f0', lineHeight: 1.5, fontWeight: 500 }}>
                      {msg.next_action}
                    </p>

                    {onStartJourney && (msg.active_topic || (msg.evidence_tag && msg.evidence_tag.reference && msg.evidence_tag.reference.includes('IS '))) && (
                      <div style={{ marginTop: '12px' }}>
                        <button
                          onClick={() => onStartJourney(msg.active_topic || msg.evidence_tag.reference)}
                          style={{
                            background: 'linear-gradient(135deg, rgba(249, 115, 22, 0.2) 0%, rgba(234, 88, 12, 0.3) 100%)',
                            border: '1px solid var(--accent-saffron)',
                            color: '#fff',
                            borderRadius: '6px',
                            padding: '6px 14px',
                            fontSize: '0.82rem',
                            fontWeight: 600,
                            cursor: 'pointer',
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '6px',
                            transition: 'all 0.2s ease',
                            boxShadow: '0 2px 10px rgba(249, 115, 22, 0.2)'
                          }}
                        >
                          <Award size={14} color="var(--accent-saffron-light)" />
                          <span>Start My Certification Journey 🚀</span>
                        </button>
                      </div>
                    )}
                  </div>
                )}

                {/* 4. Clickable Source & Evidence Tag */}
                {msg.evidence_tag && (
                  <div style={{
                    padding: '12px 20px',
                    background: 'rgba(0, 0, 0, 0.35)',
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
                        color: '#38bdf8',
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
                            background: 'rgba(56, 189, 248, 0.12)',
                            border: '1px solid rgba(56, 189, 248, 0.3)',
                            borderRadius: '6px',
                            color: '#38bdf8',
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
                          background: 'rgba(255, 255, 255, 0.06)',
                          border: '1px solid var(--border-subtle)',
                          borderRadius: '6px',
                          color: 'var(--accent-saffron-light)',
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
          <div style={{ display: 'flex', gap: '8px', padding: '12px 18px', background: 'var(--bg-glass)', borderRadius: '12px', width: 'fit-content' }}>
            <Sparkles size={18} color="var(--accent-saffron)" className="animate-spin" />
            <span style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>Consulting BIS knowledge base & compliance chain...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompt Chips */}
      <div style={{ padding: '8px 18px', display: 'flex', gap: '8px', overflowX: 'auto', background: 'rgba(0, 0, 0, 0.2)' }}>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', alignSelf: 'center', whiteSpace: 'nowrap' }}>{t('quick_prompt_title')}</span>
        {quickPrompts.map((qp, idx) => (
          <button
            key={idx}
            onClick={() => sendMessage(qp.query)}
            style={{
              whiteSpace: 'nowrap',
              fontSize: '0.78rem',
              padding: '4px 12px',
              borderRadius: '9999px',
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid var(--border-subtle)',
              color: 'var(--text-secondary)',
              cursor: 'pointer',
              transition: 'all 0.15s ease'
            }}
          >
            {qp.label}
          </button>
        ))}
      </div>

      {/* Input Bar */}
      <div style={{ padding: '16px', background: 'var(--bg-glass)', borderTop: '1px solid var(--border-subtle)', borderRadius: '0 0 12px 12px' }}>
        <form onSubmit={(e) => { e.preventDefault(); sendMessage(); }} style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <button
            type="button"
            onClick={onOpenVoice}
            title={t('chat_listening')}
            style={{
              padding: '12px',
              borderRadius: '10px',
              background: 'rgba(255, 255, 255, 0.06)',
              border: '1px solid var(--border-subtle)',
              color: 'var(--accent-saffron)',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            <Mic size={20} />
          </button>

          <input
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            placeholder={t('chat_placeholder')}
            style={{
              flex: 1,
              padding: '14px 18px',
              backgroundColor: 'var(--bg-input)',
              border: '1px solid var(--border-subtle)',
              borderRadius: '10px',
              color: '#fff',
              fontSize: '0.95rem',
              outline: 'none'
            }}
          />

          <button
            type="submit"
            disabled={!inputQuery.trim() || loading}
            className="btn-primary"
            style={{ padding: '14px 22px', borderRadius: '10px', opacity: !inputQuery.trim() || loading ? 0.6 : 1 }}
          >
            <Send size={18} />
          </button>
        </form>

        <p style={{ margin: '8px 0 0', fontSize: '0.72rem', color: 'var(--text-muted)', textAlign: 'center' }}>
          {t('chat_disclaimer')}
        </p>
      </div>
    </div>
  );
}
