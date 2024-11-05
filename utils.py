from openai import OpenAI
import os
import base64
import streamlit as st
import requests
from gtts import gTTS
from IPython.display import Audio


def get_answer_mallam(messages):
    client_mallam = OpenAI(
        base_url="https://llm-router.nous.mesolitica.com",
        api_key=st.session_state.api_key
    )
    
    system_message = [{"role": "system", "content": """
        Anda merupakan seorang assistant AI dari Malaysia, dan nama anda merupakan Jupiter, dari
        Universiti Malaya. Anda teramatlah pintar dan boleh menjawab soalan-soalan yang diberikan, dan
        juga sayang Malaysia.
        
        Anda perlu:
        1) Jawab dalam 150 patah perkataan
        2) Menggunakan Bahasa Malaysia
        3) Please refer to yourself as "Jupiter" as that is your given name.
    """}]
    messages = system_message + messages
    response = client_mallam.chat.completions.create(
        model="mallam-small",
        messages=messages
    )
    return response.choices[0].message.content

def speech_to_text_mallam(audio_file_path):
    """Convert speech to text using Mesolitica API"""
    url = "https://api.mesolitica.com/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {st.session_state.api_key}"
    }
    
    data = {
        "model": "base",
        "response_format": "text",
        "timestamp_granularities": "segment",
        "enable_diarization": "false",
        "speaker_similarity": "0.5",
        "speaker_max_n": "5",
        "chunking_method": "naive",
        "vad_method": "silero",
        "minimum_silent_ms": "200",
        "minimum_trigger_vad_ms": "1500",
        "reject_segment_vad_ratio": "0.9",
        "stream": "false"
    }
    with open(audio_file_path, "rb") as audio_file:
        files = {"file": audio_file}
        response = requests.post(url, headers=headers, data=data, files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error in transcription: {response.text}")
        return None

def text_to_speech(input_text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path

def text_to_speech_googletts(input_text):
    tts = gTTS(input_text, lang="ms")
    audio_file_path = "temp_audio_play.mp3"
    tts.save(audio_file_path)
    return audio_file_path

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)