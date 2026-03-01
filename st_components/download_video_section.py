import streamlit as st
import os
import sys
import shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.config_utils import config
from core.step1_ytdlp import download_video_ytdlp, find_video_files
from time import sleep
import re
import subprocess
from translations.translations import translate as t
from urllib.parse import urlparse, parse_qs
import requests
from datetime import datetime, timezone, timedelta


def get_youtube_info(video_id):
    url = f"https://ytapi.apps.mattw.io/v3/videos?key=foo1&part=snippet&id={video_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        items = data.get("items", [])
        if items:
            snippet = items[0].get("snippet", {})
            title = snippet.get("title", "")
            publishedAt = snippet.get("publishedAt", "")
            description = snippet.get("description", "")
            channelTitle = snippet.get("channelTitle", "")
            return title, publishedAt, description, channelTitle
        else:
            return "", "", "", ""
    except Exception as e:
        print(f"Error fetching YouTube info: {e}")
        return "", "", "", ""


def download_video_section():
    st.header(t("a. Download or Upload Video"))
    with st.container(border=True):
        username = st.session_state.get('username')
        OUTPUT_DIR = os.path.join("users", username, "output")
        try:
            video_file = find_video_files(username=username)
            st.video(video_file)

            if config.for_user(username).metadata:
                url_file_path = os.path.join("users", username, "output", "url.txt")
                if os.path.exists(url_file_path):
                    with open(url_file_path, "r", encoding="utf-8") as f:
                        saved_url = f.read().strip()
                else:
                    saved_url = ""

                url_data = urlparse(saved_url)
                query = parse_qs(url_data.query)
                video_id = query.get("v", [None])[0]
                
                # Handle YouTube Shorts URLs
                if not video_id and "youtube.com/shorts/" in saved_url:
                    video_id = saved_url.split("/shorts/")[-1].split("?")[0]
                
                # Handle youtu.be URLs
                if not video_id and saved_url.startswith("https://youtu.be/"):
                    video_id = saved_url.split("/")[-1].split("?")[0]

                if video_id:
                    clean_url = saved_url if "youtube.com/shorts/" in saved_url or saved_url.startswith("https://youtu.be/") else f"https://www.youtube.com/watch?v={video_id}"
                    title, publishedAt, description, channelTitle = get_youtube_info(video_id)
                    publishedAt = datetime.fromisoformat(publishedAt.replace("Z", "+00:00")) \
                        .astimezone(timezone(timedelta(hours=8))) \
                        .strftime("%Y.%m.%d %H:%M:%S")

                    safe_desc = description.replace("\n", "<br>")
                    thumbnail_url_maxres = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
                    thumbnail_url_sd = f"https://i.ytimg.com/vi/{video_id}/sddefault.jpg"
                    st.markdown(
                        f"""
                        <div style="
                            display: flex;
                            max-height: 200px;
                            gap: 8px;
                            padding-right: 8px;
                            border-radius: 6px;
                            margin: 0px 0px 1rem;
                        ">
                            <img src="{thumbnail_url_maxres}" style="
                                max-height: 200px;
                                max-width: 50%;
                                width: auto;
                                object-fit: contain;
                            ">
                            <img src="{thumbnail_url_sd}" style="
                                max-height: 200px;
                                max-width: 50%;
                                width: auto;
                                object-fit: contain;
                            ">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(f"""<p style="border: 1px solid currentColor; padding: 0.5rem; border-radius: 6px;">{clean_url}</p>""", unsafe_allow_html=True)
                    st.markdown(f"""<p style="border: 1px solid currentColor; padding: 0.5rem; border-radius: 6px;">{channelTitle}</p>""", unsafe_allow_html=True)
                    st.markdown(f"""<p style="border: 1px solid currentColor; padding: 0.5rem; border-radius: 6px;">{publishedAt}</p>""", unsafe_allow_html=True)
                    st.markdown(f"""<p style="border: 1px solid currentColor; padding: 0.5rem; border-radius: 6px;">{title}</p>""", unsafe_allow_html=True)
                    st.markdown(f"""<p style="border: 1px solid currentColor; padding: 0.5rem; border-radius: 6px; ">{safe_desc}</p>""", unsafe_allow_html=True)
            
            with open(video_file, "rb") as file:
                st.download_button(
                    label=t("Download"),
                    data=file,
                    file_name=os.path.basename(video_file),
                )

            if st.button(t("Delete and Reselect"), key="delete_video_button"):
                os.remove(video_file)
                if os.path.exists(OUTPUT_DIR):
                    shutil.rmtree(OUTPUT_DIR)
                sleep(1)
                st.rerun()
            return True
        except:
            col1, col2 = st.columns([3, 1])
            with col1:
                url = st.text_input(t("Enter YouTube link:"))
            with col2:
                res_dict = {
                    "360p": "360",
                    "1080p": "1080",
                    "Best": "best"
                }
                target_res = config.for_user(username).ytb_resolution
                res_options = list(res_dict.keys())
                default_idx = list(res_dict.values()).index(target_res) if target_res in res_dict.values() else 0
                res_display = st.selectbox(t("Resolution"), options=res_options, index=default_idx)
                res = res_dict[res_display]
            if st.button(t("Download Video"), key="download_button", width='stretch'):
                if url:
                    if url.startswith("https://youtu.be/"):
                        video_id = url.split("/")[-1].split("?")[0]
                        url = f"https://www.youtube.com/watch?v={video_id}"
                    elif "youtube.com/shorts/" in url:
                        video_id = url.split("/shorts/")[-1].split("?")[0]
                        url = f"https://www.youtube.com/shorts/{video_id}"
                    output_dir = os.path.join("users", username, "output")
                    os.makedirs(output_dir, exist_ok=True)
                    url_file_path = os.path.join(output_dir, "url.txt")
                    with open(url_file_path, "w") as f:
                        f.write(url)
                    with st.spinner("Downloading video..."):
                        download_video_ytdlp(url, resolution=res, username=username)
                    st.rerun()

            uploaded_file = st.file_uploader(
                t("Or upload video"),
                type=config.for_user(username).allowed_video_formats + config.for_user(username).allowed_audio_formats,
            )
            if uploaded_file:
                if os.path.exists(OUTPUT_DIR):
                    shutil.rmtree(OUTPUT_DIR)
                os.makedirs(OUTPUT_DIR, exist_ok=True)
                
                raw_name = uploaded_file.name.replace(' ', '_')
                name, ext = os.path.splitext(raw_name)
                clean_name = re.sub(r'[^\w\-_\.]', '', name) + ext.lower()
                    
                with open(os.path.join(OUTPUT_DIR, clean_name), "wb") as f:
                    f.write(uploaded_file.getbuffer())

                if ext.lower() in config.for_user(username).allowed_audio_formats:
                    convert_audio_to_video(os.path.join(OUTPUT_DIR, clean_name))
                st.rerun()
            else:
                return False

def convert_audio_to_video(audio_file: str) -> str:
    username = st.session_state.get('username')
    OUTPUT_DIR = os.path.join("users", username, "output")
    output_video = os.path.join(OUTPUT_DIR, 'black_screen.mp4')
    if not os.path.exists(output_video):
        print("🎵➡️🎬 Converting audio to video with FFmpeg ......")
        ffmpeg_cmd = ['ffmpeg', '-y', '-f', 'lavfi', '-i', 'color=c=black:s=640x360', '-i', audio_file, '-shortest', '-c:v', 'libx264', '-c:a', 'aac', '-pix_fmt', 'yuv420p', output_video]
        subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        print(f"🎵➡️🎬 Converted <{audio_file}> to <{output_video}> with FFmpeg\n")
        # delete audio file
        os.remove(audio_file)
    return output_video
