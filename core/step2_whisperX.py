import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich import print as rprint
import subprocess

from core.config_utils import config
from core.all_whisper_methods.roformer_vl import roformer_main
from core.all_whisper_methods.audio_preprocess import process_transcription, convert_video_to_audio, split_audio, save_results, compress_audio
from core.step1_ytdlp import find_video_files

import streamlit as st

def enhance_vocals(vocals_ratio=2.50):
    username = st.session_state.get('username')
    ENHANCED_VOCAL_PATH = os.path.join("users", username, "output", "audio", "enhanced_vocals.mp3")
    
    AUDIO_DIR = os.path.join("users", username, "output", "audio")
    RAW_AUDIO_FILE = os.path.join(AUDIO_DIR, "raw.mp3")
    VOCAL_AUDIO_FILE = os.path.join(AUDIO_DIR, "vocal.mp3")

    """Enhance vocals audio volume"""
    if not config.for_user(username).roformer:
        return RAW_AUDIO_FILE
        
    try:
        print(f"[cyan]🎙️ Enhancing vocals with volume ratio: {vocals_ratio}[/cyan]")
        ffmpeg_cmd = (
            f'ffmpeg -y -i "{VOCAL_AUDIO_FILE}" '
            f'-filter:a "volume={vocals_ratio}" '
            f'"{ENHANCED_VOCAL_PATH}"'
        )
        subprocess.run(ffmpeg_cmd, shell=True, check=True, capture_output=True)
        
        return ENHANCED_VOCAL_PATH
    except subprocess.CalledProcessError as e:
        print(f"[red]Error enhancing vocals: {str(e)}[/red]")
        return VOCAL_AUDIO_FILE  # Fallback to original vocals if enhancement fails
    
def transcribe():
    username = st.session_state.get('username')
    AUDIO_DIR = os.path.join("users", username, "output", "audio")
    CLEANED_CHUNKS_EXCEL_PATH = os.path.join("users", username, "output", "log", "cleaned_chunks.xlsx")
    RAW_AUDIO_FILE = os.path.join(AUDIO_DIR, "raw.mp3")

    if os.path.exists(CLEANED_CHUNKS_EXCEL_PATH):
        rprint("[yellow]⚠️ Transcription results already exist, skipping transcription step.[/yellow]")
        return
    
    # step0 Convert video to audio
    username = st.session_state.get('username')
    video_file = find_video_files(username=username)
    convert_video_to_audio(video_file)

    # step1 roformer vocal separation:
    if config.for_user(username).roformer:
        roformer_main()
    
    # step2 Compress audio
    choose_audio = enhance_vocals() if config.for_user(username).roformer else RAW_AUDIO_FILE
    
    base_path = os.path.join("users", username, "output", "audio")
    WHISPER_FILE = os.path.join(base_path, "for_whisper.mp3")

    whisper_audio = compress_audio(choose_audio, WHISPER_FILE)    
    
    # step4 Transcribe audio
    all_results = []
    transcription_method = config.for_user(username).transcription_method

    if transcription_method == "parakeet":
        from core.all_whisper_methods.parakeet import parakeet_transcribe as para
        rprint("[cyan]🎤 Transcribing audio with Parakeet...[/cyan]")
        target_len = int(config.for_user(username).target_len)
        segments = split_audio(whisper_audio, target_len=target_len)
        for start, end in segments:
            result = para(whisper_audio, username, start, end)
            all_results.append(result)

    elif transcription_method == "qwenasr":
        from core.all_whisper_methods.qwenasr import qwenasr_transcribe as qwen
        rprint("[cyan]🎤 Transcribing audio with QwenASR...[/cyan]")
        target_len = int(config.for_user(username).target_len)
        segments = split_audio(whisper_audio, target_len=target_len)
        for start, end in segments:
            result = qwen(whisper_audio, username, start, end)
            all_results.append(result)

    else:  # whisperX (default)
        if config.for_user(username).whisper.runtime == "local":
            from core.all_whisper_methods.whisperX_local import transcribe_audio as ts
            rprint("[cyan]🎤 Transcribing audio with local model...[/cyan]")
        else:
            from core.all_whisper_methods.whisperX_302 import transcribe_audio_302 as ts
            rprint("[cyan]🎤 Transcribing audio with 302 API...[/cyan]")
        segments = split_audio(whisper_audio)
        for start, end in segments:
            result = ts(whisper_audio, start, end, username=username)
            all_results.append(result)
    
    # step5 Combine results
    combined_result = {'segments': []}
    for i, result in enumerate(all_results):
        if 'error' in result:
            error_msg = result['error']
            rprint(f"[red]❌ Transcription segment {i} failed: {error_msg}[/red]")
            raise RuntimeError(f"Transcription failed at segment {i}: {error_msg}")
        if 'segments' not in result:
            rprint(f"[red]❌ Transcription segment {i} returned unexpected format: {result}[/red]")
            raise RuntimeError(f"Transcription segment {i} returned unexpected format (missing 'segments' key)")
        combined_result['segments'].extend(result['segments'])
    
    # step6 Process df
    df = process_transcription(combined_result)
    save_results(df)
        
if __name__ == "__main__":
    transcribe()
