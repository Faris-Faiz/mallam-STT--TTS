import streamlit as st
import os
from utils import autoplay_audio, get_answer_mallam, speech_to_text_mallam, text_to_speech_googletts
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *

# Float feature initialization
float_init()

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! How may I assist you today?"}
        ]
    if "api_key" not in st.session_state:
        st.session_state.api_key = None

initialize_session_state()

# Sidebar for API key input and clear chat button
with st.sidebar:
    st.title("⚙️ Settings")
    sidebar_api_key = st.text_input("Enter your Mesolitica API key", type="password", key="sidebar_api_key")
    if st.button("Submit API Key"):
        st.session_state.api_key = sidebar_api_key
        st.success("API key updated successfully!")
    
    # Add clear chat button
    if st.button("Clear Chat History"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! How may I assist you today?"}
        ]
        st.rerun()
        
    st.markdown("Powered by [Mesolitica](https://mesolitica.com/)'s Mallam API, built with 💖 by [Faris Faiz](https://www.linkedin.com/in/muhammad-faris-ahmad-faiz-ab9b35212/)")

st.title("OpenAI Conversational Chatbot 🤖")

if not st.session_state.api_key:
    st.warning("Please enter your Mesolitica API key in the sidebar to continue.")
    st.stop()

# Create footer container for the microphone
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if audio_bytes:
    # Write the audio bytes to a file
    with st.spinner("Transcribing..."):
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        transcript = speech_to_text_mallam(webm_file_path)
        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)
            os.remove(webm_file_path)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking🤔..."):
            final_response = get_answer_mallam(st.session_state.messages)
        with st.spinner("Generating audio response..."):    
            audio_file = text_to_speech_googletts(final_response)
            autoplay_audio(audio_file)
        st.write(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        os.remove(audio_file)

# Float the footer container and provide CSS to target it with
footer_container.float("bottom: 0rem;")
