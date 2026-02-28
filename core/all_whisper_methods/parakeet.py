from core.config_utils import config
import requests
import os
import subprocess
import tempfile
from urllib.parse import urljoin

import threading
transcription_lock = threading.Lock()

def parakeet_transcribe(
    audio_file: str,
    username: str,
    start: float,
    end: float
):
    """
    Transcribes a segment of an audio file using a specified transcription API.
    
    Args:
        audio_file (str): Path to the original full audio file.
        username (str): Username for config lookup.
        start (float): Start time (in seconds) of the segment to transcribe.
        end (float): End time (in seconds) of the segment to transcribe.
    
    Returns:
        dict: Transcription result with global timestamps.
    """
    with transcription_lock:
        print("parakeeeeeeet")
        parakeet_url = config.for_user(username).parakeet_url
        parakeet_url = urljoin(parakeet_url, 'transcribe')
        # parakeet_url = "http://127.0.0.1:5005/transcribe"
        if not os.path.exists(audio_file):
            return {"error": "Original audio file not found."}

        if start >= end:
            return {"error": "Invalid segment: start >= end."}

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
            temp_audio_path = temp_audio.name

        try:
            duration = end - start
            ffmpeg_cmd = [
                'ffmpeg',
                '-y',
                '-i', audio_file,
                '-ss', str(start),
                '-t', str(duration),
                '-vn',                # No video
                '-ar', '16000',       # Audio sample rate 16kHz
                '-ac', '1',           # Mono
                '-acodec', 'pcm_s16le',  # PCM 16-bit little-endian (standard WAV)
                temp_audio_path
            ]
            result = subprocess.run(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            print(temp_audio_path)
            if not os.path.exists(temp_audio_path) or os.path.getsize(temp_audio_path) == 0:
                return {"error": "Failed to create audio segment with ffmpeg."}

            with open(temp_audio_path, 'rb') as f:
                files = {
                    'audio': (os.path.basename(temp_audio_path), f)
                }
                response = requests.post(parakeet_url, files=files)
                response.raise_for_status()
                raw_result = response.json()

            word_timestamps = raw_result.get("word_timestamps", [])
            if not word_timestamps:
                print("警告：API 返回缺少 word_timestamps，使用空结构。")
                return {
                    "segments": [],
                    "word_segments": []
                }

            words_with_score = [
                {
                    "word": w["word"],
                    "start": w["start"] + start,
                    "end": w["end"] + start,
                    "score": 0.85
                }
                for w in word_timestamps
            ]

            formatted_result = {
                "segments": [{
                    "start": words_with_score[0]["start"],
                    "end": words_with_score[-1]["end"],
                    "text": " ".join(w["word"] for w in words_with_score),
                    "words": words_with_score
                }],
                "word_segments": words_with_score
            }

            return formatted_result

        except subprocess.CalledProcessError as e:
            return {
                "error": "FFmpeg failed to extract audio segment.",
                "ffmpeg_stderr": e.stderr.decode('utf-8', errors='ignore') if e.stderr else str(e)
            }
        except requests.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
        finally:
            if os.path.exists(temp_audio_path):
                try:
                    os.unlink(temp_audio_path)
                except OSError:
                    pass


if __name__ == "__main__":
    # Example usage
    whisper_audio = r""
    segments = [(0, 300)]
    # result = parakeet_transcribe(
    #     audio_file=original_audio,
    #     username="your_username",
    #     start=1,
    #     end=25.8
    # )
    # print(result)
    all_results = []

    reload_interval = 10
    count = 0

    for start, end in segments:
        print(whisper_audio)
        print(start)
        print(end)
        result = parakeet_transcribe(whisper_audio, "1", start, end)
        all_results.append(result)
        count += 1

        if count % reload_interval == 0:
            print(f"已完成 {count} 次转录，重新加载模型中...")

    print(all_results)

    combined_result = {'segments': []}
    for result in all_results:
        combined_result['segments'].extend(result['segments'])

    print(combined_result)
