import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from st_components.imports_and_utils import ask_gpt
import streamlit as st
from core.config_utils import update_key, load_key
from translations.translations import translate as t
from translations.translations import DISPLAY_LANGUAGES

def config_input(label, key, help=None):
    username = st.session_state.get('username')
    """Generic config input handler"""
    val = st.text_input(label, value=load_key(key, username=username), help=help)
    if val != load_key(key, username=username):
        update_key(key, val, username=username)
    return val

def page_setting():
    username = st.session_state.get('username')

    display_language = st.selectbox("Display Language 🌐", 
                                  options=list(DISPLAY_LANGUAGES.keys()),
                                  index=list(DISPLAY_LANGUAGES.values()).index(load_key("display_language", username=username)))
    if DISPLAY_LANGUAGES[display_language] != load_key("display_language", username=username):
        update_key("display_language", DISPLAY_LANGUAGES[display_language], username=username)
        st.rerun()

    with st.expander(t("Video Download Configuration"), expanded=True):
        h264 = st.toggle(t("Download H.264 (MP4)"), value=load_key("h264", username=username), help=t("Off for WebM format - smaller size but not supported by CapCut mobile"))
        if h264 != load_key("h264", username=username):
            update_key("h264", h264, username=username)
            st.rerun()
        metadata = st.toggle(t("Show YouTube metadata"), value=load_key("metadata", username=username))
        if metadata != load_key("metadata", username=username):
            update_key("metadata", metadata, username=username)
            st.rerun()
        windsurf_prompt = st.toggle(t("Enable strong prompt"), value=load_key("windsurf_prompt", username=username), help=t("Enable windsurf strong prompt: helps weak models keep proper nouns untranslated, may harm advanced models"))
        if windsurf_prompt != load_key("windsurf_prompt", username=username):
            update_key("windsurf_prompt", windsurf_prompt, username=username)
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
                index=list(langs.values()).index(load_key("whisper.language", username=username))
            )
            if langs[lang] != load_key("whisper.language", username=username):
                update_key("whisper.language", langs[lang], username=username)
                st.rerun()

        # add runtime selection in v2.2.0
        runtime = st.selectbox(t("WhisperX Runtime"), options=["local", "cloud"], index=["local", "cloud"].index(load_key("whisper.runtime", username=username)), help=t("Local runtime requires >8GB GPU, cloud runtime requires 302ai API key"))
        if runtime != load_key("whisper.runtime", username=username):
            update_key("whisper.runtime", runtime, username=username)
            st.rerun()
        if runtime == "cloud":
            config_input(t("WhisperX 302ai API"), "whisper.whisperX_302_api_key")

        with c2:
            target_language = st.text_input(t("Target Lang"), value=load_key("target_language", username=username), help=t("Input any language in natural language, as long as llm can understand"))
            if target_language != load_key("target_language", username=username):
                update_key("target_language", target_language, username=username)
                st.rerun()
        config_input(t("WhisperX vad_onset"), "whisper.vad_onset", help=t("Voice Activity Detection start threshold - Range: 0-1, higher more strict, lower more sensitive"))
        config_input(t("WhisperX vad_offset"), "whisper.vad_offset", help=t("Voice Activity Detection end threshold - Range: 0-1, lower detects weak signals, higher ends earlier"))
        roformer = st.toggle(t("Vocal separation enhance"), value=load_key("roformer", username=username), help=t("Recommended for videos with loud background noise, but will increase processing time"))
        if roformer != load_key("roformer", username=username):
            update_key("roformer", roformer, username=username)
            st.rerun()
        
        burn_subtitles = st.toggle(t("Burn-in Subtitles"), value=load_key("burn_subtitles", username=username), help=t("Whether to burn subtitles into the video, will increase processing time"))
        if burn_subtitles != load_key("burn_subtitles", username=username):
            update_key("burn_subtitles", burn_subtitles, username=username)
            st.rerun()

        parakeet = st.toggle("Use Parakeet", value=load_key("parakeet", username=username), help="Use Parakeet instead of whisperx")
        if parakeet != load_key("parakeet", username=username):
            update_key("parakeet", parakeet, username=username)
            st.rerun()

        config_input("Parakeet API", "parakeet_url")

    with st.expander(t("Dubbing Settings"), expanded=True):
        tts_methods = ["azure_tts", "openai_tts", "fish_tts", "sf_fish_tts", "edge_tts", "gpt_sovits", "custom_tts", "sf_cosyvoice2"]
        select_tts = st.selectbox(t("TTS Method"), options=tts_methods, index=tts_methods.index(load_key("tts_method", username=username)))
        if select_tts != load_key("tts_method", username=username):
            update_key("tts_method", select_tts, username=username)
            st.rerun()

        # sub settings for each tts method
        if select_tts == "sf_fish_tts":
            config_input(t("SiliconFlow API Key"), "sf_fish_tts.api_key")
            
            # Add mode selection dropdown
            mode_options = {
                "preset": t("Preset"),
                "custom": t("Refer_stable"),
                "dynamic": t("Refer_dynamic")
            }
            selected_mode = st.selectbox(
                t("Mode Selection"),
                options=list(mode_options.keys()),
                format_func=lambda x: mode_options[x],
                index=list(mode_options.keys()).index(load_key("sf_fish_tts.mode", username=username)) if load_key("sf_fish_tts.mode", username=username) in mode_options.keys() else 0
            )
            if selected_mode != load_key("sf_fish_tts.mode", username=username):
                update_key("sf_fish_tts.mode", selected_mode, username=username)
                st.rerun()
            if selected_mode == "preset":
                config_input("Voice", "sf_fish_tts.voice")

        elif select_tts == "openai_tts":
            config_input("302ai API", "openai_tts.api_key")
            config_input(t("OpenAI Voice"), "openai_tts.voice")

        elif select_tts == "fish_tts":
            config_input("302ai API", "fish_tts.api_key")
            fish_tts_character = st.selectbox(t("Fish TTS Character"), options=list(load_key("fish_tts.character_id_dict", username=username).keys()), index=list(load_key("fish_tts.character_id_dict", username=username).keys()).index(load_key("fish_tts.character", username=username)))
            if fish_tts_character != load_key("fish_tts.character", username=username):
                update_key("fish_tts.character", fish_tts_character, username=username)
                st.rerun()

        elif select_tts == "azure_tts":
            config_input("302ai API", "azure_tts.api_key")
            config_input(t("Azure Voice"), "azure_tts.voice")
        
        elif select_tts == "gpt_sovits":
            st.info(t("Please refer to Github homepage for GPT_SoVITS configuration"))
            config_input(t("SoVITS Character"), "gpt_sovits.character")
            
            refer_mode_options = {1: t("Mode 1: Use provided reference audio only"), 2: t("Mode 2: Use first audio from video as reference"), 3: t("Mode 3: Use each audio from video as reference")}
            selected_refer_mode = st.selectbox(
                t("Refer Mode"),
                options=list(refer_mode_options.keys()),
                format_func=lambda x: refer_mode_options[x],
                index=list(refer_mode_options.keys()).index(load_key("gpt_sovits.refer_mode", username=username)),
                help=t("Configure reference audio mode for GPT-SoVITS")
            )
            if selected_refer_mode != load_key("gpt_sovits.refer_mode", username=username):
                update_key("gpt_sovits.refer_mode", selected_refer_mode, username=username)
                st.rerun()
                
        elif select_tts == "edge_tts":
            config_input(t("Edge TTS Voice"), "edge_tts.voice")

        elif select_tts == "sf_cosyvoice2":
            config_input(t("SiliconFlow API Key"), "sf_cosyvoice2.api_key")
        
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
    base_url = load_key("api.base_url",username=username)
    api_key = load_key("api.key",username=username)
    
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
