<div align="center">

<img src="/docs/logo.webp" alt="NeoVideoLingo Logo" height="140">

# Connecting Every Frame of the World

<a href="https://trendshift.io/repositories/12200" target="_blank"><img src="https://trendshift.io/api/badge/repositories/12200" alt="Huanshere%2FVideoLingo | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[**English**](/translations/README.en.md)｜[**简体中文**](/README.md)｜[**繁體中文**](/translations/README.zh-TW.md)｜[**日本語**](/translations/README.ja.md)｜[**Español**](/translations/README.es.md)｜[**Русский**](/translations/README.ru.md)｜[**Français**](/translations/README.fr.md)

</div>

A secondary development version based on [Huanshere/VideoLingo](https://github.com/Huanshere/VideoLingo).  
For the original complete features and documentation, please refer to the [original repository](https://github.com/Huanshere/VideoLingo).

## Introduction
NeoVideoLingo: One-stop high-quality video localization tool

🎥 Intelligent processing: Integrated yt-dlp download WhisperX / Parakeet recognition, precise subtitle segmentation through NLP algorithms.

📝 Perfect translation: Adopting a three-step process of "literal translation-reflection-free translation", combined with custom terminology libraries, avoiding machine translation feel.

✅ Visual experience: Strictly implementing Netflix subtitle standards, ensuring every sentence is displayed in a single line, stress-free reading.

🗣️ Voice synthesis: Coming soon indextts2.0 support.

🚀 Convenient operation: Streamlit interface one-click start, full-process log recording, supporting interruption and resumption anytime.

## Language Support
Input language support:

🇨🇳 Chinese | 🇺🇸 English | 🇷🇺 Russian | 🇫🇷 French | 🇩🇪 German | 🇮🇹 Italian | 🇪🇸 Spanish | 🇯🇵 Japanese | 🇧🇬 Bulgarian | 🇭🇷 Croatian | 🇨🇿 Czech | 🇩🇰 Danish | 🇳🇱 Dutch | 🇪🇪 Estonian | 🇫🇮 Finnish | 🇬🇷 Greek | 🇭🇺 Hungarian | 🇱🇻 Latvian | 🇱🇹 Lithuanian | 🇲🇹 Maltese | 🇵🇱 Polish | 🇵🇹 Portuguese | 🇷🇴 Romanian | 🇸🇰 Slovak | 🇸🇮 Slovenian | 🇸🇪 Swedish | 🇺🇦 Ukrainian | 🇭🇰 Cantonese | 🇸🇦 Arabic | 🇮🇩 Indonesian | 🇰🇷 Korean | 🇹🇭 Thai | 🇻🇳 Vietnamese | 🇹🇷 Turkish | 🇮🇳 Hindi | 🇲🇾 Malay | 🇵🇭 Filipino | 🇮🇷 Persian | 🇲🇰 Macedonian

Supported dialects:
Anhui, Northeast, Fujian, Gansu, Guizhou, Hebei, Henan, Hubei, Hunan, Jiangxi, Ningxia, Shandong, Shaanxi, Shanxi, Sichuan, Tianjin, Yunnan, Zhejiang, Cantonese (Hong Kong accent), Cantonese (Guangdong accent), Wu, Minnan

## Qwen3ASR Installation Tutorial
According to the official tutorial:

"To make our qwen-asr Python package easier to use, we provide a pre-built Docker image: qwenllm/qwen3-asr. You only need to install GPU drivers and download model files to run the code. Please follow the NVIDIA Container Toolkit installation guide to ensure Docker can access your GPU. If you're in mainland China and unable to connect to Docker Hub, you can use image caching to accelerate image pulling."

On Windows, install Docker, create a .ps1 file or directly input into PowerShell:

```
$LOCAL_WORKDIR = "F:\Docker\qwen3asr"
$HOST_PORT = 8700
$CONTAINER_PORT = 80
docker run --gpus all --name qwen3-asr `
    -v /var/run/docker.sock:/var/run/docker.sock `
    -p "${HOST_PORT}:${CONTAINER_PORT}" `
    --mount "type=bind,source=${LOCAL_WORKDIR},target=/data/shared/Qwen3-ASR" `
    --shm-size=4gb `
    -it qwenllm/qwen3-asr:latest
```
If network issues occur, try using

docker.1ms.run/qwenllm/qwen3-asr

After successfully downloading and starting the container, the transcription service will not start automatically. Check this project's

\core\all_whisper_methods\qwenasrvl.py

```
#vim /usr/local/bin/qwenasrvl
#chmod +x /usr/local/bin/qwenasrvl
#qwenasrvl
```
Follow the prompts to write the file and grant permissions, then run it. Using the vLLM framework, it runs on port 80 within the container (port 8700 on the host).

## Recent Updates
February 2026
- Optimized translation and auto-translation tools with reset to first step button
- Updated new transcription method Qwen3ASR
(Qwen3-ASR-1.7B + Qwen3-ForcedAligner-0.6B)
https://github.com/QwenLM/Qwen3-ASR

January 2026
- Updated dependencies - including previous problematic av version
- Optimized auto-installation script for dependencies
- Updated new Streamlit width/icon width setting methods
- Added function to retrieve available models
- Auto-maintenance of translation files
- Modified button font color
- Sidebar RoFormer toggle switch
- Updated to latest version of WhisperX
- Replaced Demucs with BS-RoFormer

December 2025
- Hidden YouTube download progress bar
- Fixed path error

November 2025
- Fixed path error
- Fixed colon split error
- Fixed cover image
- Enabled headless mode

October 2025
- Fixed alignment failure issue
- Added support for Parakeet transcription
**https://github.com/lost0427/parakeet-api-vl**

September 2025
- Fixed archiving to history
- Updated WhisperX parameter settings
- Updated strong prompt words
- Cover image proxy
- Display standard and maximum cover images
- Fixed metadata background color issue
- Handle YouTube Shorts
- Windows service script
- Custom VAD parameters
- Release time conversion
- Image and text style modifications
- Download video button
- youtu.be support
- Cleaned YouTube links
- Updated option translations
- Toggle for showing YouTube video info
- Optional download h264 (mp4) toggle
- Show YouTube video info and cover image
- Prevent multiple WhisperX from running simultaneously
- Prevent multiple demucs from running simultaneously causing errors
- Example configuration file for multi-user authentication
- Added user login system, preliminary multi-user support completed

## Note

This repository does not maintain the dubbing part

## Installation Method

```
conda create -n videolingo python==3.11.13
conda activate videolingo
python ./install.py
```