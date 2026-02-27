import json
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st

DISPLAY_LANGUAGES = {
    "🇬🇧 English": "en",
    "🇨🇳 简体中文": "zh-CN",
    "🇭🇰 繁体中文": "zh-HK",
    "🇯🇵 日本語": "ja",
    "🇪🇸 Español": "es",
    "🇷🇺 Русский": "ru",
    "🇫🇷 Français": "fr",
}

# Load the language file based on user selection
@st.cache_data
def get_translations(language):
    file_path = f'translations/{language}.json'
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to fetch the translation
def translate(key):
    lang = st.session_state.get('display_language', 'en')
    translations = get_translations(lang)
    translation = translations.get(key)
    if translation is None:
        print(f"Warning: Translation not found for key '{key}' in language '{lang}'")
        return key
    return translation