import React, { useState, useEffect } from 'react';
import { Mic, MicOff, Check, X, Edit3, Volume2 } from 'lucide-react';

export default function VoiceModal({ isOpen, onClose, onConfirm }) {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [recognition, setRecognition] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  useEffect(() => {
    if (!isOpen) {
      setTranscript('');
      setIsListening(false);
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setErrorMsg('Speech recognition is not supported in this browser. Please use Chrome/Edge or type your query.');
      return;
    }

    const recog = new SpeechRecognition();
    recog.continuous = false;
    recog.interimResults = true;
    recog.lang = 'en-IN'; // Indian English / Hinglish

    recog.onstart = () => {
      setIsListening(true);
      setErrorMsg(null);
    };

    recog.onresult = (event) => {
      const current = event.resultIndex;
      const text = event.results[current][0].transcript;
      setTranscript(text);
    };

    recog.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setIsListening(false);
      if (event.error === 'not-allowed') {
        setErrorMsg('Microphone access was denied. Please allow microphone permissions in your browser.');
      }
    };

    recog.onend = () => {
      setIsListening(false);
    };

    setRecognition(recog);
    try {
      recog.start();
    } catch (e) {
      console.error(e);
    }

    return () => {
      if (recog) recog.stop();
    };
  }, [isOpen]);

  if (!isOpen) return null;

  const toggleListening = () => {
    if (isListening && recognition) {
      recognition.stop();
    } else if (recognition) {
      try {
        recognition.start();
      } catch (e) {
        console.error(e);
      }
    }
  };

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.75)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '20px'
    }}>
      <div className="glass-panel animate-fade-in" style={{
        width: '100%',
        maxWidth: '520px',
        backgroundColor: '#0d1322',
        border: '1px solid rgba(255, 255, 255, 0.15)',
        padding: '28px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        textAlign: 'center'
      }}>
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%', alignItems: 'center', marginBottom: '16px' }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--accent-saffron)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Volume2 size={16} /> Voice Input & Glance-Confirm
          </span>
          <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
            <X size={20} />
          </button>
        </div>

        {/* Mic Pulse Button */}
        <button
          onClick={toggleListening}
          style={{
            width: '76px',
            height: '76px',
            borderRadius: '50%',
            background: isListening ? 'linear-gradient(135deg, #ef4444, #dc2626)' : 'linear-gradient(135deg, #f97316, #ea580c)',
            border: 'none',
            color: '#fff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            boxShadow: isListening ? '0 0 25px rgba(239, 68, 68, 0.6)' : '0 0 25px rgba(249, 115, 22, 0.4)',
            transition: 'all 0.3s ease',
            margin: '12px 0 20px'
          }}
        >
          {isListening ? <Mic size={34} /> : <MicOff size={34} />}
        </button>

        <h4 style={{ margin: '0 0 6px 0', fontSize: '1.2rem', color: '#fff' }}>
          {isListening ? 'Listening... Speak your query' : 'Tap mic to resume speaking'}
        </h4>
        <p style={{ margin: '0 0 16px 0', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
          Review the transcribed text below to verify technical standard codes or numbers before sending.
        </p>

        {errorMsg && (
          <div style={{ padding: '10px 14px', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '8px', color: '#fca5a5', fontSize: '0.85rem', marginBottom: '14px', width: '100%' }}>
            {errorMsg}
          </div>
        )}

        {/* Editable Transcript Box */}
        <div style={{ width: '100%', position: 'relative', marginBottom: '20px' }}>
          <textarea
            value={transcript}
            onChange={(e) => setTranscript(e.target.value)}
            placeholder="Your spoken transcript will appear here. You can edit it manually..."
            rows={3}
            style={{
              width: '100%',
              padding: '12px 14px',
              backgroundColor: 'var(--bg-input)',
              border: '1px solid var(--border-subtle)',
              borderRadius: '10px',
              color: '#fff',
              fontSize: '0.95rem',
              outline: 'none',
              resize: 'none',
              lineHeight: 1.5
            }}
          />
        </div>

        {/* Buttons */}
        <div style={{ display: 'flex', gap: '12px', width: '100%', justifyContent: 'flex-end' }}>
          <button
            onClick={onClose}
            className="btn-secondary"
            style={{ flex: 1, justifyContent: 'center' }}
          >
            Cancel
          </button>
          <button
            onClick={() => {
              if (transcript.trim()) {
                onConfirm(transcript.trim());
                onClose();
              }
            }}
            disabled={!transcript.trim()}
            className="btn-primary"
            style={{ flex: 1, justifyContent: 'center', opacity: !transcript.trim() ? 0.5 : 1 }}
          >
            <Check size={16} /> Confirm & Send
          </button>
        </div>
      </div>
    </div>
  );
}
