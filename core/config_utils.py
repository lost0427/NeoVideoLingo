from __future__ import annotations

from pathlib import Path
from typing import Any, get_args, get_origin
import threading

from pydantic import BaseModel, ConfigDict, Field
from ruamel.yaml import YAML

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = ROOT_DIR / "config.yaml"
USERS_DIR = ROOT_DIR / "users"

yaml = YAML()
yaml.preserve_quotes = True


class ConfigBaseModel(BaseModel):
    model_config = ConfigDict(extra="allow", validate_assignment=True)


class APIConfig(ConfigBaseModel):
    key: str = "YOUR_API_KEY"
    base_url: str = "https://api.302.ai/"
    model: str = "deepseek-coder"


class WhisperConfig(ConfigBaseModel):
    model: str = "large-v3"
    language: str = "en"
    detected_language: str = "en"
    runtime: str = "local"
    whisperX_302_api_key: str = "YOUR_302_API_KEY"
    vad_onset: float = 0.500
    vad_offset: float = 0.363


class SubtitleConfig(ConfigBaseModel):
    max_length: int = 75
    target_multiplier: float = 1.2


class EdgeTTSConfig(ConfigBaseModel):
    voice: str = "zh-CN-XiaoxiaoNeural"


class GPTSoVITSConfig(ConfigBaseModel):
    character: str = "Huanyuv2"
    refer_mode: int = 3


class SpeedFactorConfig(ConfigBaseModel):
    min: float = 1.0
    accept: float = 1.2
    max: float = 1.4


class AppConfig(ConfigBaseModel):
    version: str = "2.2.1"
    display_language: str = "zh-CN"
    api: APIConfig = Field(default_factory=APIConfig)
    target_language: str = "简体中文"
    roformer: bool = True
    h264: bool = False
    metadata: bool = True
    windsurf_prompt: bool = True
    transcription_method: str = "parakeet"
    parakeet_url: str = "http://127.0.0.1:5005"
    qwenasr_url: str = "http://127.0.0.1:8700"
    target_len: int = 1200
    whisper: WhisperConfig = Field(default_factory=WhisperConfig)
    burn_subtitles: bool = True
    ytb_resolution: str = "1080"
    subtitle: SubtitleConfig = Field(default_factory=SubtitleConfig)
    summary_length: int = 8000
    max_workers: int = 4
    max_split_length: int = 20
    reflect_translate: bool = True
    pause_before_translate: bool = False
    tts_method: str = "edge_tts"
    edge_tts: EdgeTTSConfig = Field(default_factory=EdgeTTSConfig)
    gpt_sovits: GPTSoVITSConfig = Field(default_factory=GPTSoVITSConfig)
    speed_factor: SpeedFactorConfig = Field(default_factory=SpeedFactorConfig)
    min_subtitle_duration: float = 2.5
    min_trim_duration: float = 3.5
    tolerance: float = 1.5
    dub_volume: float = 1.5
    model_dir: str = "./_model_cache"
    allowed_video_formats: list[str] = Field(default_factory=lambda: ["mp4", "mov", "avi", "mkv", "flv", "wmv", "webm"])
    allowed_audio_formats: list[str] = Field(default_factory=lambda: ["wav", "mp3", "flac", "m4a"])
    llm_support_json: list[str] = Field(default_factory=lambda: ["gpt-4o", "gpt-4o-mini", "gemini-2.0-flash-exp"])
    spacy_model_map: dict[str, str] = Field(
        default_factory=lambda: {
            "en": "en_core_web_sm",
            "ru": "ru_core_news_sm",
            "fr": "fr_core_news_sm",
            "ja": "ja_core_news_sm",
            "es": "es_core_news_sm",
            "de": "de_core_news_sm",
            "it": "it_core_news_sm",
            "zh": "zh_core_web_sm",
        }
    )
    language_split_with_space: list[str] = Field(default_factory=lambda: ["en", "es", "fr", "de", "it", "ru"])
    language_split_without_space: list[str] = Field(default_factory=lambda: ["zh", "ja"])


def get_user_config_path(username: str | None = None) -> Path:
    if username:
        user_config_path = USERS_DIR / username / "config.yaml"
        if user_config_path.exists():
            return user_config_path
    return DEFAULT_CONFIG_PATH


def _resolve_model_type(annotation: Any) -> type[BaseModel] | None:
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return annotation
    origin = get_origin(annotation)
    if origin is None:
        return None
    for arg in get_args(annotation):
        model_type = _resolve_model_type(arg)
        if model_type is not None:
            return model_type
    return None


def _collect_missing_config_fields(
    model_type: type[BaseModel],
    raw_data: Any,
    prefix: str = "",
) -> list[str]:
    data = raw_data if isinstance(raw_data, dict) else {}
    missing_fields: list[str] = []

    for field_name, field_info in model_type.model_fields.items():
        field_path = f"{prefix}.{field_name}" if prefix else field_name
        if field_name not in data:
            missing_fields.append(field_path)
            continue

        nested_model = _resolve_model_type(field_info.annotation)
        field_value = data[field_name]
        if nested_model and isinstance(field_value, dict):
            missing_fields.extend(
                _collect_missing_config_fields(nested_model, field_value, field_path)
            )

    return missing_fields


class ConfigManager:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._cache: dict[str, AppConfig] = {}

    @staticmethod
    def _cache_key(username: str | None = None) -> str:
        return username if username else "__default__"

    def _load_from_disk(self, username: str | None = None) -> AppConfig:
        config_path = get_user_config_path(username)
        with config_path.open("r", encoding="utf-8") as file:
            raw_data = yaml.load(file) or {}
        if username:
            user_config_path = USERS_DIR / username / "config.yaml"
            if user_config_path.exists():
                missing_fields = _collect_missing_config_fields(AppConfig, raw_data)
                for field_path in missing_fields:
                    print(
                        f"[CONFIG] user='{username}' missing '{field_path}', using default value."
                    )
        return AppConfig.model_validate(raw_data)

    def get(self, username: str | None = None, reload: bool = False) -> AppConfig:
        key = self._cache_key(username)
        with self._lock:
            if reload or key not in self._cache:
                self._cache[key] = self._load_from_disk(username)
            return self._cache[key]

    def save(self, username: str | None = None) -> None:
        key = self._cache_key(username)
        with self._lock:
            config_model = self.get(username)
            config_path = get_user_config_path(username)
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with config_path.open("w", encoding="utf-8") as file:
                yaml.dump(config_model.model_dump(mode="python", exclude_none=True), file)
            self._cache[key] = config_model

    def _walk_path(self, obj: Any, path_parts: list[str]) -> Any:
        current = obj
        for part in path_parts:
            if isinstance(current, BaseModel):
                current = getattr(current, part)
            elif isinstance(current, dict):
                current = current[part]
            else:
                raise KeyError(f"Cannot access '{part}' in config path")
        return current

    def get_path(self, path: str, username: str | None = None) -> Any:
        config_model = self.get(username)
        return self._walk_path(config_model, path.split("."))

    def set_path(self, path: str, value: Any, username: str | None = None) -> None:
        config_model = self.get(username)
        path_parts = path.split(".")
        parent = self._walk_path(config_model, path_parts[:-1]) if len(path_parts) > 1 else config_model
        key = path_parts[-1]
        if isinstance(parent, BaseModel):
            setattr(parent, key, value)
        elif isinstance(parent, dict):
            parent[key] = value
        else:
            raise KeyError(f"Cannot set '{path}' in config")
        self.save(username)


class ConfigAccessor:
    def __init__(self, manager: ConfigManager) -> None:
        object.__setattr__(self, "_manager", manager)

    def for_user(self, username: str | None = None) -> AppConfig:
        return self._manager.get(username)

    def reload(self, username: str | None = None) -> AppConfig:
        return self._manager.get(username, reload=True)

    def save(self, username: str | None = None) -> None:
        self._manager.save(username)

    def get_path(self, path: str, username: str | None = None) -> Any:
        return self._manager.get_path(path, username)

    def set_path(self, path: str, value: Any, username: str | None = None) -> None:
        self._manager.set_path(path, value, username)

    def __getattr__(self, item: str) -> Any:
        return getattr(self.for_user(), item)

    def __setattr__(self, key: str, value: Any) -> None:
        config_model = self.for_user()
        setattr(config_model, key, value)
        self.save()


config = ConfigAccessor(ConfigManager())


def get_joiner(language: str, username: str | None = None) -> str:
    active_config = config.for_user(username)
    if language in active_config.language_split_with_space:
        return " "
    if language in active_config.language_split_without_space:
        return ""
    raise ValueError(f"Unsupported language code: {language}")

