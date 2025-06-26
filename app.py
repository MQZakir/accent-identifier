import streamlit as st
import os
import tempfile
import subprocess
import requests
import soundfile as sf
import time

# --- Custom CSS for minimalistic, modern, full black UI with subtle faded orange accents only for borders/lines ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, .stApp {
        background-color: #000 !important;
        color: #fff !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stTextInput > div > div > input {
        background: #18181b !important;
        color: #fff !important;
        border-radius: 1.2rem !important;
        border: 1.5px solid #ffb347 !important;
        font-size: 1.08rem;
        font-family: 'Inter', sans-serif !important;
    }
    .stButton > button {
        background: #18181b !important;
        color: #fff !important;
        border-radius: 1.5rem !important;
        font-weight: 600;
        font-size: 1.08rem;
        border: 1.5px solid #ffb347;
        transition: 0.2s;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 0 0px #ffb347;
    }
    .stButton > button:hover {
        background: #232323 !important;
        color: #fff !important;
        border: 1.5px solid #ffb347;
        box-shadow: 0 0 8px #ffb347;
    }
    .accent-card {
        background: #18181b;
        border-radius: 1.2rem;
        padding: 2rem 1.5rem 1.5rem 1.5rem;
        margin-top: 2rem;
        box-shadow: 0 2px 16px #ffb34722;
        text-align: center;
        border: 1.5px solid #ffb347;
        max-width: 480px;
        margin-left: auto;
        margin-right: auto;
        width: 90vw;
    }
    .accent-title {
        color: #fff;
        font-size: 2rem;
        margin-bottom: 0.5rem;
        letter-spacing: 0.5px;
        font-weight: 600;
        border-bottom: 2px solid #ffb347;
        display: inline-block;
        padding-bottom: 0.2rem;
        width: 100%;
        word-break: break-word;
    }
    .accent-confidence {
        color: #fff;
        font-size: 1.15rem;
        margin-bottom: 1rem;
        font-weight: 600;
        border-bottom: 1.5px solid #ffb347;
        display: inline-block;
        padding-bottom: 0.1rem;
        margin-top: 0.7rem;
        width: 100%;
        word-break: break-word;
    }
    .accent-summary {
        color: #fff;
        font-size: 1rem;
        margin-top: 1rem;
        word-break: break-word;
    }
    @media (max-width: 600px) {
        .accent-card {
            padding: 1.2rem 0.5rem 1rem 0.5rem;
            font-size: 0.98rem;
        }
        .accent-title {
            font-size: 1.2rem;
        }
        .accent-confidence {
            font-size: 1rem;
        }
        .accent-summary {
            font-size: 0.95rem;
        }
    }
    .stSpinner > div > div {
        color: #fff !important;
    }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="English Accent Identifier", page_icon="🗣️", layout="centered")

st.markdown("""
# 🗣️ <span style='color:#fff; font-family: Inter, sans-serif;'>English Accent Identifier</span>
""", unsafe_allow_html=True)

st.markdown("""
Paste a public video URL (YouTube, Loom, direct MP4, etc.) to analyze the speaker's English accent. This tool will extract up to 1 minute of audio and classify the accent using a state-of-the-art model.
""")

video_url = st.text_input('Video URL', placeholder='Paste your video link here...')

if st.button('Analyze') and video_url:
    with st.spinner('Downloading video and extracting audio...'):
        temp_dir = tempfile.mkdtemp()
        audio_path = os.path.join(temp_dir, 'audio.wav')
        video_path = os.path.join(temp_dir, 'video.mp4')
        try:
            if 'youtube.com' in video_url or 'youtu.be' in video_url or 'loom.com' in video_url:
                subprocess.run([
                    'yt-dlp',
                    '-f', 'bestaudio',
                    '-o', video_path,
                    video_url
                ], check=True)
            else:
                r = requests.get(video_url, stream=True)
                with open(video_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            # Extract up to 1 minute (60 seconds) of audio (or full audio if shorter). For more accuracy, please increase the number of seconds(change the '60' to a higher number)
            result = subprocess.run([
                'ffmpeg', '-y', '-i', video_path, '-t', '60', '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', audio_path
            ], capture_output=True, text=True)
            time.sleep(0.5)
            if result.returncode != 0 or not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
                st.error('Audio extraction failed. Please check your video link or try another video.')
            else:
                st.success('Audio extracted!')
                st.audio(audio_path)
                with st.spinner('Analyzing accent... This may take some time.'):
                    try:
                        import librosa
                        import numpy as np
                        import torchaudio
                        from speechbrain.pretrained.interfaces import foreign_class
                        audio_path_fixed = audio_path.replace("\\", "/")
                        audio, sr = librosa.load(audio_path_fixed, sr=16000, mono=True)
                        sf.write(audio_path_fixed, audio, sr)
                        classifier = foreign_class(
                            source="bookbot/english-accent-classifier",
                            pymodule_file="custom_interface.py",
                            classname="CustomEncoderWav2vec2Classifier",
                        )
                        out_prob, score, index, text_lab = classifier.classify_file(audio_path_fixed)
                        if isinstance(text_lab, list):
                            accent = text_lab[0].capitalize() if text_lab else "Unknown"
                        else:
                            accent = str(text_lab).capitalize()
                        confidence = float(score) * 100
                        st.markdown(f"""
                            <div class='accent-card'>
                                <div class='accent-title'>Accent: <span style='color:#fff'>{accent}</span></div>
                                <div class='accent-confidence'>Confidence: <b>{confidence:.1f}%</b></div>
                                <div class='accent-summary'>
                                    This result is based on the <b>bookbot/english-accent-classifier</b> model from Hugging Face.<br>
                                    The confidence score reflects the model's certainty.
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f'Accent analysis failed: {e}')
        except Exception as e:
            st.error(f'Error: {e}')

st.markdown("""
---
<small style='color:#fff; font-family: Inter, sans-serif;'>Made with ❤️ using <a href='https://streamlit.io/' style='color:#fff'>Streamlit</a> & <a href='https://speechbrain.github.io/' style='color:#fff'>SpeechBrain</a>.<br>For best results, use clear audio with minimal background noise.</small>
""", unsafe_allow_html=True) 