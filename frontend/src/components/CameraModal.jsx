import React, { useState, useRef, useEffect } from 'react';
import { Camera, X, RefreshCw, Check, AlertCircle, SwitchCamera, Upload } from 'lucide-react';

export default function CameraModal({ isOpen, onClose, onCapture, onSwitchToFileUpload }) {
  const [stream, setStream] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);
  const [facingMode, setFacingMode] = useState('environment'); // 'environment' (back) or 'user' (front)
  const [cameraError, setCameraError] = useState(null);
  const [isLoadingCamera, setIsLoadingCamera] = useState(false);

  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      setCapturedImage(null);
      setCameraError(null);
      startCamera(facingMode);
    } else {
      stopCamera();
    }
    return () => {
      stopCamera();
    };
  }, [isOpen, facingMode]);

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      setStream(null);
    }
  };

  const startCamera = async (mode) => {
    setIsLoadingCamera(true);
    setCameraError(null);
    stopCamera();

    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('Camera access is not supported by your browser or environment.');
      }

      const newStream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: mode,
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
        audio: false,
      });

      setStream(newStream);
      if (videoRef.current) {
        videoRef.current.srcObject = newStream;
      }
    } catch (err) {
      console.warn('Camera access error:', err);
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        setCameraError('Camera access was blocked. Please allow camera permissions in your browser or upload a file.');
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        setCameraError('No camera found on this device. You can upload an image file instead.');
      } else {
        setCameraError(err.message || 'Unable to start camera stream. Please use file upload.');
      }
    } finally {
      setIsLoadingCamera(false);
    }
  };

  const toggleFacingMode = () => {
    setFacingMode((prev) => (prev === 'environment' ? 'user' : 'environment'));
  };

  const handleCapture = () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;

    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const dataUrl = canvas.toDataURL('image/jpeg', 0.88);
    setCapturedImage(dataUrl);
    stopCamera();
  };

  const handleRetake = () => {
    setCapturedImage(null);
    startCamera(facingMode);
  };

  const handleConfirm = () => {
    const cb = onCapture || onCapturePhoto;
    if (capturedImage && cb) {
      cb(capturedImage);
      onClose();
    }
  };

  const handleSwitchToFile = () => {
    onClose();
    if (onSwitchToFileUpload) {
      onSwitchToFileUpload();
    }
  };

  if (!isOpen) return null;

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(11, 12, 13, 0.75)',
        backdropFilter: 'blur(10px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1100,
        padding: '16px',
      }}
    >
      <div
        className="glass-panel animate-fade-in"
        style={{
          width: '100%',
          maxWidth: '580px',
          backgroundColor: 'var(--bg-card)',
          border: '1px solid var(--border-subtle)',
          borderRadius: '16px',
          padding: '24px',
          display: 'flex',
          flexDirection: 'column',
          boxShadow: 'var(--shadow-hover)',
          overflow: 'hidden',
          position: 'relative',
        }}
      >
        {/* Header */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '16px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div
              style={{
                width: '36px',
                height: '36px',
                borderRadius: '8px',
                background: 'linear-gradient(135deg, #111315 0%, #0d9488 100%)',
                color: '#fff',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 2px 8px rgba(13, 148, 136, 0.25)',
              }}
            >
              <Camera size={20} />
            </div>
            <div>
              <h3 style={{ margin: 0, fontSize: '1.15rem', color: 'var(--text-primary)' }}>
                Live Product & Mark Scanner
              </h3>
              <p style={{ margin: '1px 0 0', fontSize: '0.76rem', color: 'var(--text-secondary)' }}>
                Align product, label, or ISI mark inside the frame
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            aria-label="Close camera"
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-muted)',
              cursor: 'pointer',
              padding: '6px',
              borderRadius: '6px',
            }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Viewfinder Viewport or Error */}
        <div
          style={{
            width: '100%',
            height: '340px',
            backgroundColor: '#000000',
            borderRadius: '12px',
            overflow: 'hidden',
            position: 'relative',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: '1px solid var(--border-subtle)',
          }}
        >
          {cameraError ? (
            <div style={{ padding: '24px', textAlign: 'center', color: '#fff', maxWidth: '380px' }}>
              <AlertCircle size={36} color="#ef4444" style={{ margin: '0 auto 12px' }} />
              <p style={{ margin: '0 0 8px', fontSize: '0.95rem', fontWeight: 600 }}>Camera Unavailable</p>
              <p style={{ margin: '0 0 16px', fontSize: '0.82rem', color: '#cbd5e1', lineHeight: 1.4 }}>
                {cameraError}
              </p>
              <button
                onClick={handleSwitchToFile}
                className="btn-primary"
                style={{ fontSize: '0.82rem', padding: '8px 16px' }}
              >
                <Upload size={14} /> Upload Image File Instead
              </button>
            </div>
          ) : capturedImage ? (
            <img
              src={capturedImage}
              alt="Captured item"
              style={{ width: '100%', height: '100%', objectFit: 'contain', backgroundColor: '#000' }}
            />
          ) : (
            <>
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
              />

              {/* Viewfinder Targeting Reticle */}
              <div
                style={{
                  position: 'absolute',
                  inset: '24px',
                  border: '2px dashed rgba(45, 212, 191, 0.65)',
                  borderRadius: '12px',
                  pointerEvents: 'none',
                  boxShadow: '0 0 0 9999px rgba(0, 0, 0, 0.3)',
                }}
              />

              <div
                style={{
                  position: 'absolute',
                  bottom: '12px',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  background: 'rgba(17, 19, 21, 0.75)',
                  backdropFilter: 'blur(6px)',
                  color: '#edf2f2',
                  fontSize: '0.76rem',
                  padding: '4px 12px',
                  borderRadius: '9999px',
                  pointerEvents: 'none',
                  whiteSpace: 'nowrap',
                }}
              >
                Hold steady & capture clearly
              </div>

              {/* Camera Switcher Button (if available) */}
              <button
                onClick={toggleFacingMode}
                title="Switch Camera (Front / Rear)"
                style={{
                  position: 'absolute',
                  top: '12px',
                  right: '12px',
                  background: 'rgba(17, 19, 21, 0.65)',
                  border: '1px solid rgba(237, 242, 242, 0.2)',
                  color: '#ffffff',
                  borderRadius: '50%',
                  width: '36px',
                  height: '36px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                }}
              >
                <SwitchCamera size={18} />
              </button>
            </>
          )}
        </div>

        {/* Hidden Canvas for Frame Grab */}
        <canvas ref={canvasRef} style={{ display: 'none' }} />

        {/* Bottom Actions */}
        <div
          style={{
            marginTop: '20px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '12px',
          }}
        >
          {capturedImage ? (
            <>
              <button
                onClick={handleRetake}
                className="btn-secondary"
                style={{ flex: 1, justifyContent: 'center', gap: '6px' }}
              >
                <RefreshCw size={15} /> Retake
              </button>
              <button
                onClick={handleConfirm}
                className="btn-primary"
                style={{ flex: 1, justifyContent: 'center', gap: '6px' }}
              >
                <Check size={16} /> Use Photo
              </button>
            </>
          ) : (
            <>
              <button
                onClick={handleSwitchToFile}
                className="btn-secondary"
                style={{ flex: 1, justifyContent: 'center', gap: '6px' }}
              >
                <Upload size={15} /> Upload File
              </button>
              <button
                onClick={handleCapture}
                disabled={isLoadingCamera || !!cameraError}
                className="btn-primary"
                style={{
                  flex: 1.5,
                  justifyContent: 'center',
                  gap: '8px',
                  opacity: isLoadingCamera || cameraError ? 0.6 : 1,
                }}
              >
                <Camera size={17} /> Capture Photo
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
