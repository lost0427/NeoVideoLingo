#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#vim /usr/local/bin/qwenasrvl
#chmod +x /usr/local/bin/qwenasrvl
#qwenasrvl

import torch
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import Optional
from qwen_asr import Qwen3ASRModel
import tempfile
import os

asr_pipeline = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global asr_pipeline
    print("🚀 Starting Qwenasrvl custom service...")
    print("📦 Loading Qwen3 ASR (1.7B) and Forced Aligner (0.6B) models...")
    
    asr_pipeline = Qwen3ASRModel.LLM(
        model="Qwen/Qwen3-ASR-1.7B",
        forced_aligner="Qwen/Qwen3-ForcedAligner-0.6B",
        gpu_memory_utilization=0.8,
        forced_aligner_kwargs=dict(
            dtype=torch.float16,
            device_map="cuda:0",
        ),
        max_inference_batch_size=32,
        max_new_tokens=1024,
    )
    print("✅ Models loaded successfully! API is ready.")
    yield

app = FastAPI(lifespan=lifespan)

class AudioRequest(BaseModel):
    url: str
    language: str = None


def _do_transcribe(audio_source: str, language: Optional[str] = None):
    results = asr_pipeline.transcribe(
        audio=audio_source,
        language=language,
        return_time_stamps=True
    )

    res = results[0]
    timestamps = []

    if res.time_stamps:
        for ts in res.time_stamps:
            timestamps.append({
                "word": ts.text,
                "start": round(ts.start_time, 3),
                "end": round(ts.end_time, 3)
            })

    return {
        "text": res.text,
        "language": res.language,
        "timestamps": timestamps
    }


@app.post("/transcribe")
def transcribe(
    req: Optional[AudioRequest] = None,
    audio: Optional[UploadFile] = File(None),
    language: Optional[str] = Form(None)
):
    if audio is not None:
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp.write(audio.file.read())
            tmp_path = tmp.name
        try:
            return _do_transcribe(tmp_path, language)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    if req is not None:
        return _do_transcribe(req.url, req.language)

    return {"error": "Please provide an audio file (multipart upload) or a URL (JSON body)."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)