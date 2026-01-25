<div align="center">

<img src="/docs/logo.png" alt="VideoLingo Logo" height="140">

# Connecting Every Frame of the World

<a href="https://trendshift.io/repositories/12200" target="_blank"><img src="https://trendshift.io/api/badge/repositories/12200" alt="Huanshere%2FVideoLingo | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[**English**](/translations/README.en.md)｜[**简体中文**](/README.md)｜[**繁體中文**](/translations/README.zh-TW.md)｜[**日本語**](/translations/README.ja.md)｜[**Español**](/translations/README.es.md)｜[**Русский**](/translations/README.ru.md)｜[**Français**](/translations/README.fr.md)

</div>

A secondary development version based on [Huanshere/VideoLingo](https://github.com/Huanshere/VideoLingo).  
For the original complete features and documentation, please refer to the [original repository](https://github.com/Huanshere/VideoLingo).


## Recent Updates

January 2026
- Updated dependencies - including the old av version that was causing errors previously
- Optimized automatic dependency installation script
- Updated new Streamlit width/icon width setting methods
- Added feature to get available models
- Automatic maintenance of translation files
- Modified button font color
- Sidebar RoFormer toggle switch
- Updated to latest version of WhisperX
- Replaced Demucs with BS-RoFormer

December 2025
- Hidden YouTube download progress bar
- Fixed path errors

November 2025
- Fixed path errors
- Fixed colon splitting error
- Fixed cover image
- Enabled headless mode

November 2025
- Fixed alignment failure issue
- Added support for Parakeet transcription
**https://github.com/lost0427/parakeet-api-vl**

September 2025
- Fixed archiving to history
- WhisperX parameter settings update
- Strong prompt word updates
- Cover image proxy
- Display standard and maximum cover images
- Fixed metadata background color issue
- Handle youtube shorts
- Windows service script
- Custom vad parameters
- Release time conversion
- Image and text style modifications
- Download video button
- youtu.be support
- Clean YouTube links
- Updated option translations
- Show YouTube video info toggle
- Optional download h264 (mp4) toggle
- Show YouTube video info and cover image
- Prevent multiple WhisperX running simultaneously
- Prevent multiple demucs running simultaneously causing errors
- Multi-user authentication example configuration file
- Added user login system, preliminary multi-user support completed

## Note

This repository does not maintain the dubbing functionality

## Installation Method

```
conda create -n videolingo python==3.11.13
conda activate videolingo
python ./install.py
```