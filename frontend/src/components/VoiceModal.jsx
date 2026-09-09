import React, { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Check, X, RefreshCw, Volume2, Globe, Loader2, AlertCircle } from 'lucide-react';
import { API_BASE_URL } from '../api/config';

const INDIAN_LANGUAGES = [
  { code: 'auto', label: 'Auto-Detect (Any Indian Language)' },
  { code: 'hi', label: 'Hindi (हिन्दी)' },
  { code: 'en', label: 'Indian English' },
  { code: 'ta', label: 'Tamil (தமிழ்)' },
  { code: 'te', label: 'Telugu (తెలుగు)' },
  { code: 'mr', label: 'Marathi (मराठी)' },
  { code: 'bn', label: 'Bengali (বাংলা)' },
  { code: 'gu', label: 'Gujarati (ગુજરાતી)' },
  { code: 'kn', label: 'Kannada (ಕನ್ನಡ)' },
  { code: 'ml', label: 'Malayalam (മലയാളം)' },
  { code: 'pa', label: 'Punjabi (ਪੰਜਾਬੀ)' },
  { code: 'ur', label: 'Urdu (اردو)' },
];

export default function VoiceModal({ isOpen, onClose, onConfirm, defaultLang = 'auto' }) {
  const [selectedLang, setSelectedLang] = useState(defaultLang || 'auto');
  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [recordingSeconds, setRecordingSeconds] = useState(0);
  const [transcript, setTranscript] = useState('');
  const [detectedMeta, setDetectedMeta] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const streamRef = useRef(null);
  const timerIntervalRef = useRef(null);

  // Reset state on open/close
  useEffect(() => {
    if (!isOpen) {
      stopMediaTracks();
      clearInterval(timerIntervalRef.current);
      setIsRecording(false);
      setIsTranscribing(false);
      setRecordingSeconds(0);
      setTranscript('');
      setDetectedMeta(null);
      setErrorMsg(null);
    } else {
      setSelectedLang(defaultLang || 'auto');
      // Automatically prompt to start recording when modal opens
      startRecording();
    }
    return () => {
      stopMediaTracks();
      clearInterval(timerIntervalRef.current);
    };
  }, [isOpen]);

  const stopMediaTracks = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }
  };

  const startRecording = async () => {
    setErrorMsg(null);
    setTranscript('');
    setDetectedMeta(null);
    setRecordingSeconds(0);
    audioChunksRef.current = [];

    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('Microphone recording is not supported in this browser.');
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });

      streamRef.current = stream;

      // Select supported audio MIME type
      let options = {};
      if (typeof MediaRecorder.isTypeSupported === 'function') {
        if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
          options = { mimeType: 'audio/webm;codecs=opus' };
        } else if (MediaRecorder.isTypeSupported('audio/webm')) {
          options = { mimeType: 'audio/webm' };
        } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
          options = { mimeType: 'audio/mp4' };
        }
      }

      const recorder = new MediaRecorder(stream, options);
      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) {
          audioChunksRef.current.push(e.data);
        }
      };

      recorder.onstop = async () => {
        clearInterval(timerIntervalRef.current);
        setIsRecording(false);
        stopMediaTracks();

        const mimeType = recorder.mimeType || 'audio/webm';
        const audioBlob = new Blob(audioChunksRef.current, { type: mimeType });

        if (audioBlob.size < 500) {
          setErrorMsg('Recording was too short. Please hold the mic and speak your query.');
          return;
        }

        await processAudioWithGroqWhisper(audioBlob, mimeType);
      };

      recorder.start(250); // Collect slice every 250ms
      setIsRecording(true);

      // Start elapsed timer
      timerIntervalRef.current = setInterval(() => {
        setRecordingSeconds((prev) => prev + 1);
      }, 1000);
    } catch (err) {
      console.error('Recording initialization error:', err);
      setIsRecording(false);
      stopMediaTracks();
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        setErrorMsg('Microphone access was blocked. Please allow microphone permission in your browser URL bar.');
      } else {
        setErrorMsg(err.message || 'Could not start microphone recording.');
      }
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
  };

  const processAudioWithGroqWhisper = async (audioBlob, mimeType) => {
    setIsTranscribing(true);
    setErrorMsg(null);

    try {
      const ext = mimeType.includes('mp4') ? 'mp4' : 'webm';
      const formData = new FormData();
      formData.append('file', audioBlob, `voice_query.${ext}`);
      formData.append('language', selectedLang);

      const res = await fetch(`${API_BASE_URL}/api/transcribe`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server transcription failed (${res.status})`);
      }

      const data = await res.json();
      setTranscript(data.text || '');
      setDetectedMeta({
        language: data.language || selectedLang,
        duration: data.duration,
        model: data.model || 'whisper-large-v3',
      });
    } catch (err) {
      console.error('Whisper transcription error:', err);
      setErrorMsg(err.message || 'Transcription failed. Please try speaking again or type your query.');
    } finally {
      setIsTranscribing(false);
    }
  };

  const formatTime = (secs) => {
    const mins = Math.floor(secs / 60);
    const rem = secs % 60;
    return `${mins}:${rem < 10 ? '0' : ''}${rem}`;
  };

  if (!isOpen) return null;

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        backdropFilter: 'blur(10px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        padding: '20px',
      }}
    >
      <div
        className="glass-panel animate-fade-in"
        style={{
          width: '100%',
          maxWidth: '540px',
          backgroundColor: 'var(--bg-card)',
          border: '1px solid var(--border-subtle)',
          borderRadius: '16px',
          padding: '28px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
          boxShadow: 'var(--shadow-hover)',
        }}
      >
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%', alignItems: 'center', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span
              style={{
                fontSize: '0.85rem',
                color: 'var(--accent-saffron)',
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                background: 'rgba(249, 115, 22, 0.12)',
                padding: '4px 10px',
                borderRadius: '8px',
                border: '1px solid rgba(249, 115, 22, 0.25)',
              }}
            >
              <Volume2 size={15} /> Groq Whisper Large v3
            </span>
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              color: 'var(--text-muted)',
              cursor: 'pointer',
              padding: '4px',
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Indian Language Dropdown */}
        <div style={{ width: '100%', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '20px' }}>
          <Globe size={16} color="var(--accent-saffron)" />
          <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', whiteSpace: 'nowrap' }}>
            Language:
          </span>
          <select
            value={selectedLang}
            onChange={(e) => setSelectedLang(e.target.value)}
            disabled={isRecording || isTranscribing}
            style={{
              flex: 1,
              padding: '7px 12px',
              backgroundColor: 'var(--bg-surface)',
              border: '1px solid var(--border-subtle)',
              borderRadius: '8px',
              color: 'var(--text-primary)',
              fontSize: '0.85rem',
              outline: 'none',
              cursor: 'pointer',
            }}
          >
            {INDIAN_LANGUAGES.map((lang) => (
              <option key={lang.code} value={lang.code} style={{ background: 'var(--bg-card)', color: 'var(--text-primary)' }}>
                {lang.label}
              </option>
            ))}
          </select>
        </div>

        {/* Mic Pulse Button */}
        <div style={{ position: 'relative', margin: '8px 0 16px' }}>
          {isRecording && (
            <div
              style={{
                position: 'absolute',
                inset: '-10px',
                borderRadius: '50%',
                background: 'radial-gradient(circle, rgba(239, 68, 68, 0.4) 0%, rgba(239, 68, 68, 0) 70%)',
                animation: 'pulse 1.5s infinite ease-in-out',
              }}
            />
          )}

          <button
            onClick={isRecording ? stopRecording : startRecording}
            disabled={isTranscribing}
            style={{
              width: '84px',
              height: '84px',
              borderRadius: '50%',
              background: isRecording
                ? 'linear-gradient(135deg, #ef4444, #dc2626)'
                : 'linear-gradient(135deg, #f97316, #ea580c)',
              border: 'none',
              color: '#fff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: isTranscribing ? 'wait' : 'pointer',
              boxShadow: isRecording
                ? '0 0 30px rgba(239, 68, 68, 0.7)'
                : '0 0 25px rgba(249, 115, 22, 0.45)',
              transition: 'all 0.3s ease',
              position: 'relative',
              zIndex: 2,
            }}
          >
            {isTranscribing ? (
              <Loader2 size={36} className="animate-spin" />
            ) : isRecording ? (
              <Mic size={38} />
            ) : (
              <MicOff size={38} />
            )}
          </button>
        </div>

        {/* Status Text & Timer */}
        <div style={{ marginBottom: '16px' }}>
          {isRecording ? (
            <div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', color: '#ef4444', fontWeight: 700, fontSize: '1.1rem' }}>
                <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ef4444', display: 'inline-block' }} />
                Recording ({formatTime(recordingSeconds)})
              </div>
              <p style={{ margin: '4px 0 0', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                Speak your question clearly in your chosen language... Tap to finish.
              </p>
            </div>
          ) : isTranscribing ? (
            <div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', color: '#38bdf8', fontWeight: 600 }}>
                <Loader2 size={16} className="animate-spin" /> Transcribing with Groq Whisper Large v3...
              </div>
              <p style={{ margin: '4px 0 0', fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                Processing audio on ultra-fast Groq LPU hardware...
              </p>
            </div>
          ) : transcript ? (
            <div>
              <h4 style={{ margin: '0 0 4px', fontSize: '1.05rem', color: '#10b981' }}>
                Speech Transcribed Successfully!
              </h4>
              <p style={{ margin: 0, fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                Review and verify technical IS codes or numbers below before submitting.
              </p>
            </div>
          ) : (
            <div>
              <h4 style={{ margin: '0 0 4px', fontSize: '1.05rem', color: 'var(--text-primary)' }}>
                Ready to Record
              </h4>
              <p style={{ margin: 0, fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                Tap the microphone button to speak in any Indian language.
              </p>
            </div>
          )}
        </div>

        {/* Error Message */}
        {errorMsg && (
          <div
            style={{
              padding: '10px 14px',
              background: 'rgba(239, 68, 68, 0.12)',
              border: '1px solid rgba(239, 68, 68, 0.3)',
              borderRadius: '8px',
              color: '#fca5a5',
              fontSize: '0.85rem',
              marginBottom: '14px',
              width: '100%',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              textAlign: 'left',
            }}
          >
            <AlertCircle size={16} style={{ flexShrink: 0 }} />
            <span>{errorMsg}</span>
          </div>
        )}

        {/* Detected Language / Metadata Badge */}
        {detectedMeta && (
          <div
            style={{
              width: '100%',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '4px 10px',
              marginBottom: '6px',
              fontSize: '0.75rem',
              color: '#94a3b8',
            }}
          >
            <span>🌐 Detected: <strong style={{ color: '#38bdf8' }}>{detectedMeta.language}</strong></span>
            <span>⚡ Engine: <strong style={{ color: '#f59e0b' }}>Whisper Large v3</strong></span>
          </div>
        )}

        {/* Editable Transcript Box */}
        <div style={{ width: '100%', position: 'relative', marginBottom: '20px' }}>
          <textarea
            value={transcript}
            onChange={(e) => setTranscript(e.target.value)}
            placeholder="Transcribed text will appear here. You can manually edit or correct standard codes..."
            rows={3}
            disabled={isRecording || isTranscribing}
            style={{
              width: '100%',
              padding: '12px 14px',
              backgroundColor: 'var(--bg-input)',
              border: '1px solid var(--border-strong)',
              borderRadius: '10px',
              color: 'var(--text-primary)',
              fontSize: '0.95rem',
              outline: 'none',
              resize: 'none',
              lineHeight: 1.5,
              boxShadow: '0 1px 3px rgba(0,0,0,0.03)'
            }}
          />
        </div>

        {/* Action Buttons */}
        <div style={{ display: 'flex', gap: '10px', width: '100%', justifyContent: 'flex-end' }}>
          <button
            onClick={onClose}
            className="btn-secondary"
            style={{ flex: 1, justifyContent: 'center' }}
          >
            Cancel
          </button>

          {!isRecording && transcript && (
            <button
              onClick={startRecording}
              className="btn-secondary"
              style={{ flex: 1, justifyContent: 'center', gap: '6px' }}
            >
              <RefreshCw size={14} /> Re-record
            </button>
          )}

          {isRecording ? (
            <button
              onClick={stopRecording}
              className="btn-primary"
              style={{ flex: 1.5, justifyContent: 'center', background: '#ef4444', borderColor: '#ef4444' }}
            >
              <Check size={16} /> Stop & Transcribe
            </button>
          ) : (
            <button
              onClick={() => {
                if (transcript.trim()) {
                  onConfirm(transcript.trim());
                  onClose();
                }
              }}
              disabled={!transcript.trim() || isTranscribing}
              className="btn-primary"
              style={{ flex: 1.5, justifyContent: 'center', opacity: !transcript.trim() || isTranscribing ? 0.5 : 1 }}
            >
              <Check size={16} /> Confirm & Send
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
