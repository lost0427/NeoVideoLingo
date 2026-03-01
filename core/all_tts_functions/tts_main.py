import os
import sys
import re
from rich import print as rprint
from pydub import AudioSegment
import streamlit as st

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from core.config_utils import config
from core.all_whisper_methods.audio_preprocess import get_audio_duration
from core.all_tts_functions.gpt_sovits_tts import gpt_sovits_tts_for_videolingo
from core.all_tts_functions.edge_tts import edge_tts
from core.all_tts_functions.custom_tts import custom_tts
from core.ask_gpt import ask_gpt
from core.prompts_storage import get_correct_text_prompt

SUPPORTED_TTS_METHODS = {"edge_tts", "gpt_sovits", "custom_tts"}

def clean_text_for_tts(text):
    """Remove problematic characters for TTS"""
    chars_to_remove = ['&', '®', '™', '©']
    for char in chars_to_remove:
        text = text.replace(char, '')
    return text.strip()

def tts_main(text, save_as, number, task_df, username=None):
    text = clean_text_for_tts(text)
    # Check if text is empty or single character, single character voiceovers are prone to bugs
    cleaned_text = re.sub(r'[^\w\s]', '', text).strip()
    if not cleaned_text or len(cleaned_text) <= 1:
        silence = AudioSegment.silent(duration=100)  # 100ms = 0.1s
        silence.export(save_as, format="wav")
        rprint(f"Created silent audio for empty/single-char text: {save_as}")
        return
    
    # Skip if file exists
    if os.path.exists(save_as):
        return
    
    print(f"Generating <{text}...>")
    if username is None:
        username = st.session_state.get('username')
    TTS_METHOD = config.for_user(username).tts_method
    if TTS_METHOD not in SUPPORTED_TTS_METHODS:
        raise ValueError(
            f"Unsupported tts_method '{TTS_METHOD}'. Supported methods: {sorted(SUPPORTED_TTS_METHODS)}"
        )
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            if attempt >= max_retries - 1:
                print("Asking GPT to correct text...")
                correct_text = ask_gpt(get_correct_text_prompt(text), username=username, log_title='tts_correct_text')
                text = correct_text['text']
            if TTS_METHOD == 'gpt_sovits':
                gpt_sovits_tts_for_videolingo(text, save_as, number, task_df, username=username)
            elif TTS_METHOD == 'edge_tts':
                edge_tts(text, save_as, username=username)
            elif TTS_METHOD == 'custom_tts':
                custom_tts(text, save_as)
            
            # Check generated audio duration
            duration = get_audio_duration(save_as)
            if duration > 0:
                break
            else:
                if os.path.exists(save_as):
                    os.remove(save_as)
                if attempt == max_retries - 1:
                    print(f"Warning: Generated audio duration is 0 for text: {text}")
                    # Create silent audio file
                    silence = AudioSegment.silent(duration=100)  # 100ms silence
                    silence.export(save_as, format="wav")
                    return
                print(f"Attempt {attempt + 1} failed, retrying...")
        except Exception as e:
            if attempt == max_retries - 1:
                raise Exception(f"Failed to generate audio after {max_retries} attempts: {str(e)}")
            print(f"Attempt {attempt + 1} failed, retrying...")
