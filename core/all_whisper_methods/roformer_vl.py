import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from rich.console import Console
from rich import print as rprint

# from torch.cuda import is_available as is_cuda_available
from typing import Optional
import gc
import streamlit as st
import threading

from transformers import AutoModel
import torch
import librosa
import soundfile
import time
from core.config_utils import config

# class PreloadedSeparator(Separator):
#     def __init__(self, model: BagOfModels, shifts: int = 1, overlap: float = 0.25,
#                  split: bool = True, segment: Optional[int] = None, jobs: int = 0):
#         self._model, self._audio_channels, self._samplerate = model, model.audio_channels, model.samplerate
#         device = "cuda" if is_cuda_available() else "mps" if torch.backends.mps.is_available() else "cpu"
#         self.update_parameter(device=device, shifts=shifts, overlap=overlap, split=split,
#                             segment=segment, jobs=jobs, progress=True, callback=None, callback_arg=None)

roformer_lock = threading.Lock()

def roformer_main():
    with roformer_lock:
        username = st.session_state.get('username')
        AUDIO_DIR = os.path.join("users", username, "output", "audio")
        RAW_AUDIO_FILE = os.path.join(AUDIO_DIR, "raw.mp3")
        BACKGROUND_AUDIO_FILE = os.path.join(AUDIO_DIR, "background.mp3")
        VOCAL_AUDIO_FILE = os.path.join(AUDIO_DIR, "vocal.mp3")

        if os.path.exists(VOCAL_AUDIO_FILE) and os.path.exists(BACKGROUND_AUDIO_FILE):
            rprint(f"[yellow]⚠️ {VOCAL_AUDIO_FILE} and {BACKGROUND_AUDIO_FILE} already exist, skip roformer processing.[/yellow]")
            return

        console = Console()
        os.makedirs(AUDIO_DIR, exist_ok=True)
        
        console.print("🤖 Loading <BS-RoFormer> model...")
        
        MODEL_DIR = config.model_dir
        if MODEL_DIR:
            os.makedirs(MODEL_DIR, exist_ok=True)
            console.print(f"📂 Model cache directory set to: {MODEL_DIR}")

        model = AutoModel.from_pretrained(
            "HiDolen/Mini-BS-RoFormer-V2-46.8M",
            trust_remote_code=True,
            cache_dir=MODEL_DIR
        ).to("cuda")
        
        console.print("🎵 Separating audio...")
        
        start = time.time()
        waveform, sr = librosa.load(RAW_AUDIO_FILE, sr=44100, mono=False)
        waveform_tensor = torch.tensor(waveform).float().to("cuda")
        with torch.no_grad():
            # result : [Drums, Bass, Other, Vocals]
            result = model.separate(waveform_tensor, batch_size=2, verbose=False)
        console.print(f"audio separation took {int(time.time() - start)} seconds")
        
        console.print("🎤 Saving vocals track...")

        background_data = (result[0] + result[1] + result[2]).cpu().numpy().T
        vocal_data = result[3].cpu().numpy().T

        start = time.time()
        soundfile.write(VOCAL_AUDIO_FILE, vocal_data, 44100)
        console.print(f"Write vocals track took {int(time.time() - start)} seconds")
        
        console.print("🎹 Saving background music...")
        start = time.time()
        soundfile.write(BACKGROUND_AUDIO_FILE, background_data, 44100)
        console.print(f"Write background music took {int(time.time() - start)} seconds")

        # Clean up memory
        del result, waveform_tensor, model, vocal_data, background_data
        gc.collect()
        torch.cuda.empty_cache()
        
        console.print("[green]✨ Audio separation completed![/green]")

if __name__ == "__main__":
    roformer_main()
