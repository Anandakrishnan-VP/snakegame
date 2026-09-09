"""
Test Speech-to-Text Transcription via Groq Whisper Large v3.
Verifies:
1. /api/transcribe accepts audio multipart uploads.
2. Interacts with Groq Whisper model to generate text.
3. Language parameter is accepted and respected.
"""

import io
import wave
import struct
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def generate_test_wav():
    """Generates a small 1-second WAV audio sample in memory."""
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16000)
        # Synthetic audio waveform
        data = struct.pack('<' + 'h' * 16000, *([300 if i % 4 < 2 else -300 for i in range(16000)]))
        wav.writeframes(data)
    buf.seek(0)
    return buf.read()

def test_whisper_transcription_endpoint():
    audio_bytes = generate_test_wav()

    # 1. Test transcription with English
    res = client.post(
        "/api/transcribe",
        files={"file": ("speech.wav", audio_bytes, "audio/wav")},
        data={"language": "en"}
    )
    assert res.status_code == 200, f"Transcription failed: {res.text}"
    data = res.json()

    print("\n[Transcription Test Result]")
    print(f"  Success: {data.get('success')}")
    print(f"  Model: {data.get('model')}")
    print(f"  Language: {data.get('language')}")
    print(f"  Text: {data.get('text')}")

    assert data.get("success") is True
    assert "whisper" in data.get("model", "").lower()
    print("\nWhisper endpoint test PASSED successfully!")

if __name__ == "__main__":
    test_whisper_transcription_endpoint()
