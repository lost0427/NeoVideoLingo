import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from st_components.imports_and_utils import ask_gpt
import streamlit as st
from core.config_utils import config
from translations.translations import translate as t
from translations.translations import DISPLAY_LANGUAGES

def config_input(label, key, help=None):
    username = st.session_state.get('username')
    """Generic config input handler"""
    val = st.text_input(label, value=config.get_path(key, username=username), help=help)
    if val != config.get_path(key, username=username):
        config.set_path(key, val, username=username)
    return val

def page_setting():
    username = st.session_state.get('username')

    display_language = st.selectbox("Display Language 🌐", 
                                  options=list(DISPLAY_LANGUAGES.keys()),
                                  index=list(DISPLAY_LANGUAGES.values()).index(config.for_user(username).display_language))
    if DISPLAY_LANGUAGES[display_language] != config.for_user(username).display_language:
        config.set_path('display_language', DISPLAY_LANGUAGES[display_language], username=username)
        st.rerun()

    with st.expander(t("Video Download Configuration"), expanded=True):
        h264 = st.toggle(t("Download H.264 (MP4)"), value=config.for_user(username).h264, help=t("Off for WebM format - smaller size but not supported by CapCut mobile"))
        if h264 != config.for_user(username).h264:
            config.set_path('h264', h264, username=username)
            st.rerun()
        metadata = st.toggle(t("Show YouTube metadata"), value=config.for_user(username).metadata)
        if metadata != config.for_user(username).metadata:
            config.set_path('metadata', metadata, username=username)
            st.rerun()
        windsurf_prompt = st.toggle(t("Enable strong prompt"), value=config.for_user(username).windsurf_prompt, help=t("Enable windsurf strong prompt: helps weak models keep proper nouns untranslated, may harm advanced models"))
        if windsurf_prompt != config.for_user(username).windsurf_prompt:
            config.set_path('windsurf_prompt', windsurf_prompt, username=username)
            st.rerun()
        
    with st.expander(t("LLM Configuration"), expanded=True):
        config_input(t("API_KEY"), "api.key")
        config_input(t("BASE_URL"), "api.base_url", help=t("Openai format, will add /v1/chat/completions automatically"))
        
        c1, c2 = st.columns([4, 1])
        with c1:
            config_input(t("MODEL"), "api.model", help=t("click to check API validity")+ " 👉")
        with c2:
            if st.button("📡", key="api"):
                st.toast(t("API Key is valid") if check_api() else t("API Key is invalid"), 
                        icon="✅" if check_api() else "❌")
        
        # Add model list fetching functionality
        if st.button(t("🔄 Fetch Available Models"), key="fetch_models"):
            try:
                available_models = fetch_available_models()
                if available_models:
                    st.session_state.available_models = available_models
                    count = len(available_models)
                    st.success(t("Found {count} models").format(count=count))

                    with st.expander(t("📋 Available Models"), expanded=False):
                        model_list_text = "\n".join([f"- {model}" for model in available_models])
                        st.markdown(model_list_text)

                else:
                    st.warning("No models found")
            except Exception as e:
                st.error(f"Error fetching models: {str(e)}")
    
    with st.expander(t("Subtitles Settings"), expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            langs = {
                "🇺🇸 English": "en",
                "🇨🇳 简体中文": "zh",
                "🇪🇸 Español": "es",
                "🇷🇺 Русский": "ru",
                "🇫🇷 Français": "fr",
                "🇩🇪 Deutsch": "de",
                "🇮🇹 Italiano": "it",
                "🇯🇵 日本語": "ja"
            }
            lang = st.selectbox(
                t("Recog Lang"),
                options=list(langs.keys()),
                index=list(langs.values()).index(config.for_user(username).whisper.language)
            )
            if langs[lang] != config.for_user(username).whisper.language:
                config.set_path('whisper.language', langs[lang], username=username)
                st.rerun()

        # add runtime selection in v2.2.0
        runtime = st.selectbox(t("WhisperX Runtime"), options=["local", "cloud"], index=["local", "cloud"].index(config.for_user(username).whisper.runtime), help=t("Local runtime requires >8GB GPU, cloud runtime requires 302ai API key"))
        if runtime != config.for_user(username).whisper.runtime:
            config.set_path('whisper.runtime', runtime, username=username)
            st.rerun()
        if runtime == "cloud":
            config_input(t("WhisperX 302ai API"), "whisper.whisperX_302_api_key")

        with c2:
            target_language = st.text_input(t("Target Lang"), value=config.for_user(username).target_language, help=t("Input any language in natural language, as long as llm can understand"))
            if target_language != config.for_user(username).target_language:
                config.set_path('target_language', target_language, username=username)
                st.rerun()
        config_input(t("WhisperX vad_onset"), "whisper.vad_onset", help=t("Voice Activity Detection start threshold - Range: 0-1, higher more strict, lower more sensitive"))
        config_input(t("WhisperX vad_offset"), "whisper.vad_offset", help=t("Voice Activity Detection end threshold - Range: 0-1, lower detects weak signals, higher ends earlier"))
        roformer = st.toggle(t("Vocal separation enhance"), value=config.for_user(username).roformer, help=t("Recommended for videos with loud background noise, but will increase processing time"))
        if roformer != config.for_user(username).roformer:
            config.set_path('roformer', roformer, username=username)
            st.rerun()
        
        burn_subtitles = st.toggle(t("Burn-in Subtitles"), value=config.for_user(username).burn_subtitles, help=t("Whether to burn subtitles into the video, will increase processing time"))
        if burn_subtitles != config.for_user(username).burn_subtitles:
            config.set_path('burn_subtitles', burn_subtitles, username=username)
            st.rerun()

        transcription_methods = ["whisperX", "parakeet", "qwenasr"]
        current_method = config.for_user(username).transcription_method
        if current_method not in transcription_methods:
            current_method = "whisperX"
        selected_method = st.selectbox(
            t("Transcription Method"),
            options=transcription_methods,
            index=transcription_methods.index(current_method),
            help=t("Select the transcription engine: whisperX, Parakeet, or QwenASR")
        )
        if selected_method != config.for_user(username).transcription_method:
            config.set_path('transcription_method', selected_method, username=username)
            st.rerun()

        if selected_method == "parakeet":
            config_input("Parakeet API", "parakeet_url")
        elif selected_method == "qwenasr":
            config_input("QwenASR API", "qwenasr_url")

    with st.expander(t("Dubbing Settings"), expanded=True):
        tts_methods = ["edge_tts", "gpt_sovits", "custom_tts"]
        current_tts_method = config.for_user(username).tts_method
        if current_tts_method not in tts_methods:
            current_tts_method = "edge_tts"
            config.set_path('tts_method', current_tts_method, username=username)
        select_tts = st.selectbox(t("TTS Method"), options=tts_methods, index=tts_methods.index(current_tts_method))
        if select_tts != config.for_user(username).tts_method:
            config.set_path('tts_method', select_tts, username=username)
            st.rerun()

        # sub settings for each tts method
        if select_tts == "gpt_sovits":
            st.info(t("Please refer to Github homepage for GPT_SoVITS configuration"))
            config_input(t("SoVITS Character"), "gpt_sovits.character")
            
            refer_mode_options = {1: t("Mode 1: Use provided reference audio only"), 2: t("Mode 2: Use first audio from video as reference"), 3: t("Mode 3: Use each audio from video as reference")}
            selected_refer_mode = st.selectbox(
                t("Refer Mode"),
                options=list(refer_mode_options.keys()),
                format_func=lambda x: refer_mode_options[x],
                index=list(refer_mode_options.keys()).index(config.for_user(username).gpt_sovits.refer_mode),
                help=t("Configure reference audio mode for GPT-SoVITS")
            )
            if selected_refer_mode != config.for_user(username).gpt_sovits.refer_mode:
                config.set_path('gpt_sovits.refer_mode', selected_refer_mode, username=username)
                st.rerun()
                
        elif select_tts == "edge_tts":
            config_input(t("Edge TTS Voice"), "edge_tts.voice")

        elif select_tts == "custom_tts":
            st.info(t("Configure your custom TTS in core/all_tts_functions/custom_tts.py"))
        
def check_api():
    try:
        resp = ask_gpt("This is a test, response 'message':'success' in json format.", 
                      response_json=True, log_title='None')
        return resp.get('message') == 'success'
    except Exception:
        return False

def fetch_available_models():
    """Fetch available models from the API endpoint"""
    import requests
    import json
    username = st.session_state.get('username')
    base_url = config.for_user(username).api.base_url
    api_key = config.for_user(username).api.key
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    if base_url.endswith("/v1"):
        models_url = base_url.replace("/v1", "/v1/models")
    else:
        models_url = f"{base_url.rstrip('/')}/v1/models" if base_url else ""
    
    if not models_url:
        raise ValueError("Invalid base URL configuration")
    
    response = requests.get(models_url, headers=headers)
    response.raise_for_status()
    data = response.json()
    
    # Extract model names from the response (typically in a 'data' field with 'id' for each model)
    models = []
    if 'data' in data:
        for model in data['data']:
            if 'id' in model:
                models.append(model['id'])
    else:
        # Fallback: if there's no 'data' field, try to extract model names differently
        # This handles cases where the API might return models in a different format
        for key, value in data.items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict) and 'id' in item:
                        models.append(item['id'])
    
    return sorted(models)  # Return sorted list of model names
