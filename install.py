import json
import os
import re
import sys
import platform
import subprocess
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

ascii_logo = r"""
 _   _            __     ___     _            _     _
| \ | | ___  ___ \ \   / (_) __| | ___  ___ | |   (_)_ __   __ _  ___
|  \| |/ _ \/ _ \ \ \ / /| |/ _` |/ _ \/ _ \| |   | | '_ \ / _` |/ _ \
| |\  |  __/ (_)   \ V / | | (_| |  __/ (_) | |___| | | | | (_| | (_) |
|_| \_|\___|\___/   \_/  |_|\__,_|\___|\___/|_____|_|_| |_|\__, |\___/
                                                            |___/
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSLATIONS_DIR = os.path.join(BASE_DIR, "translations")
DEFAULT_CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

DISPLAY_LANGUAGES = {
    "🇬🇧 English": "en",
    "🇨🇳 简体中文": "zh-CN",
    "🇭🇰 繁体中文": "zh-HK",
    "🇯🇵 日本語": "ja",
    "🇪🇸 Español": "es",
    "🇷🇺 Русский": "ru",
    "🇫🇷 Français": "fr",
}

_TRANSLATION_CACHE = {}
_ACTIVE_LANGUAGE = None


def _load_default_display_language():
    default_language = "en"
    if not os.path.exists(DEFAULT_CONFIG_PATH):
        return default_language

    try:
        with open(DEFAULT_CONFIG_PATH, "r", encoding="utf-8") as config_file:
            for line in config_file:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if stripped.startswith("display_language:"):
                    value = stripped.split(":", 1)[1].strip().strip("'\"")
                    return value or default_language
    except Exception:
        return default_language

    return default_language


def set_install_language(language):
    global _ACTIVE_LANGUAGE
    _ACTIVE_LANGUAGE = language or "en"


def load_translations(language):
    lang = language or "en"
    if lang in _TRANSLATION_CACHE:
        return _TRANSLATION_CACHE[lang]

    file_path = os.path.join(TRANSLATIONS_DIR, f"{lang}.json")
    if not os.path.exists(file_path):
        _TRANSLATION_CACHE[lang] = {}
        return _TRANSLATION_CACHE[lang]

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            _TRANSLATION_CACHE[lang] = json.load(file)
    except Exception:
        _TRANSLATION_CACHE[lang] = {}
    return _TRANSLATION_CACHE[lang]


def t(key):
    active_language = _ACTIVE_LANGUAGE or _load_default_display_language()
    translations = load_translations(active_language)
    translation = translations.get(key)
    if translation is None:
        print(f"Warning: Translation not found for key '{key}' in language '{active_language}'")
        return key
    return translation

def install_package(*packages):
    subprocess.check_call([sys.executable, "-m", "pip", "install", *packages])

def check_nvidia_gpu():
    install_package("nvidia-ml-py")
    import pynvml
    try:
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        if device_count > 0:
            print(t("Detected NVIDIA GPU(s)"))
            for i in range(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                name = pynvml.nvmlDeviceGetName(handle)
                print(f"GPU {i}: {name}")
            return True
        else:
            print(t("No NVIDIA GPU detected"))
            return False
    except pynvml.NVMLError:
        print(t("No NVIDIA GPU detected or NVIDIA drivers not properly installed"))
        return False
    finally:
        pynvml.nvmlShutdown()

def _parse_version(version_str):
    match = re.search(r"\d+(?:\.\d+)*", version_str or "")
    if not match:
        return None
    parts = [int(p) for p in match.group(0).split(".")]
    while len(parts) < 2:
        parts.append(0)
    return tuple(parts[:2])

def detect_cuda_version():
    try:
        result = subprocess.run(
            ["nvidia-smi"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        match = re.search(r"CUDA Version:\s*([0-9]+(?:\.[0-9]+)?)", result.stdout)
        if match:
            return match.group(1)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    try:
        result = subprocess.run(
            ["nvcc", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        match = re.search(r"release\s+([0-9]+(?:\.[0-9]+)?)", result.stdout + result.stderr)
        if match:
            return match.group(1)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return None

def check_ffmpeg():
    from rich.console import Console
    from rich.panel import Panel
    console = Console()

    try:
        # Check if ffmpeg is installed
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        console.print(Panel(t("✅ FFmpeg is already installed"), style="green"))
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        system = platform.system()
        install_cmd = ""
        
        if system == "Windows":
            install_cmd = "choco install ffmpeg"
            extra_note = t("Install Chocolatey first (https://chocolatey.org/)")
        elif system == "Darwin":
            install_cmd = "brew install ffmpeg"
            extra_note = t("Install Homebrew first (https://brew.sh/)")
        elif system == "Linux":
            install_cmd = "sudo apt install ffmpeg  # Ubuntu/Debian\nsudo yum install ffmpeg  # CentOS/RHEL"
            extra_note = t("Use your distribution's package manager")
        
        console.print(Panel.fit(
            t("❌ FFmpeg not found\n\n") +
            f"{t('🛠️ Install using:')}\n[bold cyan]{install_cmd}[/bold cyan]\n\n" +
            f"{t('💡 Note:')}\n{extra_note}\n\n" +
            f"{t('🔄 After installing FFmpeg, please run this installer again:')}\n[bold cyan]python install.py[/bold cyan]",
            style="red"
        ))
        raise SystemExit(t("FFmpeg is required. Please install it and run the installer again."))

def main():
    install_package("requests", "rich", "ruamel.yaml", "InquirerPy")
    from rich.console import Console
    from rich.panel import Panel
    from rich.box import DOUBLE
    from InquirerPy import inquirer

    console = Console()
    
    width = max(len(line) for line in ascii_logo.splitlines()) + 4
    welcome_panel = Panel(
        ascii_logo,
        width=width,
        box=DOUBLE,
        title="[bold green]🌏[/bold green]",
        border_style="bright_blue"
    )
    console.print(welcome_panel)

    language_labels = {value: label for label, value in DISPLAY_LANGUAGES.items()}
    default_language = _load_default_display_language()
    default_choice = language_labels.get(default_language, "🇬🇧 English")

    selected_language = DISPLAY_LANGUAGES[inquirer.select(
        message="Select language / 选择语言 / 選擇語言 / 言語を選択 / Seleccionar idioma / Sélectionner la langue / Выберите язык:",
        choices=list(DISPLAY_LANGUAGES.keys()),
        default=default_choice
    ).execute()]
    set_install_language(selected_language)

    console.print(Panel.fit(t("🚀 Starting Installation"), style="bold magenta"))

    # Configure mirrors
    # add a check to ask user if they want to configure mirrors
    if inquirer.confirm(
        message=t("Do you need to auto-configure PyPI mirrors? (Recommended if you have difficulty accessing pypi.org)"),
        default=True
    ).execute():
        from core.pypi_autochoose import main as choose_mirror
        choose_mirror()

    # Detect system and GPU
    has_gpu = platform.system() != 'Darwin' and check_nvidia_gpu()
    if has_gpu:
        cuda_version = detect_cuda_version()
        cuda_tuple = _parse_version(cuda_version)
        cuda_tag = "cu129" if cuda_tuple and cuda_tuple >= (13, 0) else "cu128"
        console.print(Panel(
            f"{cuda_version or 'unknown'} {cuda_tag}",
            style="cyan"
        ))
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "torch==2.8.0",
            "torchvision==0.23.0",
            "torchaudio==2.8.0",
            "--index-url",
            f"https://download.pytorch.org/whl/{cuda_tag}"
        ])
    else:
        system_name = "🍎 MacOS" if platform.system() == 'Darwin' else "💻 No NVIDIA GPU"
        console.print(Panel(t(f"{system_name} detected, installing CPU version of PyTorch... Note: it might be slow during whisperX transcription."), style="cyan"))
        subprocess.check_call([sys.executable, "-m", "pip", "install", "torch==2.8.0", "torchvision==0.23.0", "torchaudio==2.8.0"])

    def install_requirements():
        try:
            subprocess.check_call([
                sys.executable, 
                "-m", 
                "pip", 
                "install", 
                "-r", 
                "requirements.txt"
            ], env={**os.environ, "PIP_NO_CACHE_DIR": "0", "PYTHONIOENCODING": "utf-8"})
        except subprocess.CalledProcessError as e:
            console.print(Panel(t("❌ Failed to install requirements:") + str(e), style="red"))

    def install_noto_font():
        # Detect Linux distribution type
        if os.path.exists('/etc/debian_version'):
            # Debian/Ubuntu systems
            cmd = ['sudo', 'apt-get', 'install', '-y', 'fonts-noto']
            pkg_manager = "apt-get"
        elif os.path.exists('/etc/redhat-release'):
            # RHEL/CentOS/Fedora systems
            cmd = ['sudo', 'yum', 'install', '-y', 'google-noto*']
            pkg_manager = "yum"
        else:
            console.print("Warning: Unrecognized Linux distribution, please install Noto fonts manually", style="yellow")
            return
            
        try:
            subprocess.run(cmd, check=True)
            console.print(f"✅ Successfully installed Noto fonts using {pkg_manager}", style="green")
        except subprocess.CalledProcessError:
            console.print("❌ Failed to install Noto fonts, please install manually", style="red")

    if platform.system() == 'Linux':
        install_noto_font()
    
    console.print(Panel(t("Installing requirements using `pip install -r requirements.txt`"), style="cyan"))
    install_requirements()
    check_ffmpeg()
    
    # First panel with installation complete and startup command
    panel1_text = (
        t("Installation completed") + "\n\n" +
        t("Now I will run this command to start the application:") + "\n" +
        "[bold]streamlit run st.py[/bold]\n" +
        t("Note: First startup may take up to 1 minute")
    )
    console.print(Panel(panel1_text, style="bold green"))

    # Second panel with troubleshooting tips
    panel2_text = (
        t("If the application fails to start:") + "\n" +
        "1. " + t("Check your network connection") + "\n" +
        "2. " + t("Re-run the installer: [bold]python install.py[/bold]")
    )
    console.print(Panel(panel2_text, style="yellow"))

    # start the application
    subprocess.Popen(["streamlit", "run", "st.py"])

if __name__ == "__main__":
    main()
