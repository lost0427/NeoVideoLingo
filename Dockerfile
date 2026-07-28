# Keep this tag aligned with the torch/torchaudio versions used by install.py
# and required by WhisperX.
ARG PYTORCH_IMAGE=pytorch/pytorch:2.8.0-cuda12.8-cudnn9-runtime
FROM ${PYTORCH_IMAGE}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG APP_UID=10001
ARG APP_GID=10001

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true \
    XDG_CACHE_HOME=/app/_model_cache \
    HF_HOME=/app/_model_cache/huggingface \
    TORCH_HOME=/app/_model_cache/torch \
    NLTK_DATA=/app/_model_cache/nltk

# FFmpeg handles all media operations. The remaining runtime libraries support
# OpenCV, SoundFile, CTranslate2, multilingual subtitles, HTTPS, and signal
# forwarding. Compiler/CUDA development packages are intentionally omitted.
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        ffmpeg \
        fontconfig \
        fonts-noto-cjk \
        fonts-noto-color-emoji \
        fonts-noto-core \
        iputils-ping \
        libgl1 \
        libglib2.0-0 \
        libgomp1 \
        libsndfile1 \
        tini \
    && fc-cache -f \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependency installation is cached until requirements.txt changes.
COPY requirements.txt ./
RUN python -c "import sys; assert sys.version_info[:2] == (3, 11), sys.version" \
    && python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install -r requirements.txt \
    && python -m pip check \
    && python -c "import torch; assert torch.__version__.startswith('2.8.'); print('torch:', torch.__version__, 'cuda:', torch.version.cuda)"

# spaCy installs language models on demand. Redirect those runtime installs to
# an application-owned directory while keeping image dependencies immutable.
ENV PYTHONPATH=/app/.runtime_packages \
    PIP_TARGET=/app/.runtime_packages

RUN groupadd --gid "${APP_GID}" videolingo \
    && useradd --uid "${APP_UID}" --gid "${APP_GID}" --create-home --shell /usr/sbin/nologin videolingo

# Build from the checked-out source instead of cloning a second, possibly
# different repository revision during the image build.
COPY --chown=videolingo:videolingo . .

# auth.yaml is deliberately excluded from the build context so credentials are
# not baked into the image. The example keeps the container bootable and can be
# replaced with a read-only bind mount in deployment.
RUN cp auth.yaml.example auth.yaml \
    && mkdir -p .runtime_packages _model_cache users output history \
    && chown -R videolingo:videolingo \
        auth.yaml .runtime_packages _model_cache users output history

USER videolingo

EXPOSE 8501
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=90s --retries=3 \
    CMD curl --fail --silent --show-error http://127.0.0.1:8501/_stcore/health || exit 1

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["streamlit", "run", "st.py", "--server.port=8501", "--server.headless=true", "--browser.gatherUsageStats=false"]
