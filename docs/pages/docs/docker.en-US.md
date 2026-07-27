# Docker / Podman Deployment

The image packages the checked-out source tree and uses Python 3.11, PyTorch 2.8, and CUDA 12.8. It includes FFmpeg, the shared libraries required by OpenCV and SoundFile, and multilingual Noto fonts. Models, per-user configuration, and generated files are kept in mounts.

## Prerequisites

- Docker 24+ or Podman 4.6+
- An NVIDIA driver that supports CUDA 12.8
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- At least 20 GB of free disk space is recommended; models are downloaded on first use

Podman accesses NVIDIA GPUs through CDI. Generate the CDI configuration after installing NVIDIA Container Toolkit:

```bash
sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml
nvidia-ctk cdi list
```

Prepare the login configuration without baking credentials into the image:

```bash
cp auth.yaml.example auth.yaml
# Edit users/passwords and set non-empty cookie.name and cookie.key values.
```

## Build on GitHub

`.github/workflows/container-image.yml` builds the image on a GitHub Hosted Runner and publishes it to GitHub Container Registry (GHCR), so no local build is required:

- Pushing a Git tag such as `v1.0.0` builds and publishes `v1.0.0` and `latest` (same build)
- Pushes to `main` do not build
- `workflow_dispatch` can start a manual run from the GitHub Actions page (no version tag without a `v*` ref)

The registry path automatically uses the lowercase repository name:

```text
ghcr.io/<owner>/<repository>:latest
```

For this repository, the resulting path is `ghcr.io/lost0427/neovideolingo:latest`.

Pull the image after the workflow completes:

```bash
podman pull ghcr.io/<owner>/<repository>:latest
# or
docker pull ghcr.io/<owner>/<repository>:latest
```

The workflow pushes with the repository-provided `GITHUB_TOKEN` and declares `packages: write`. Package visibility can be changed in GitHub Packages settings after the first publication. The upstream PyTorch image currently provides `linux/amd64`, so the workflow builds that platform only.

## Local Build

Choose a container engine from the project root:

```bash
# Podman. Docker image format preserves the Dockerfile health check metadata.
podman build --format docker -t videolingo:local .

# Docker
docker build -t videolingo:local .
```

The dependency layer is rebuilt only when `requirements.txt` changes. The default base image is `pytorch/pytorch:2.8.0-cuda12.8-cudnn9-runtime`; it can be overridden at build time:

```bash
podman build --format docker \
  --build-arg PYTORCH_IMAGE=pytorch/pytorch:2.8.0-cuda12.8-cudnn9-runtime \
  -t videolingo:local .
```

## Run

Named volumes are recommended for model and user data. Podman uses the CDI device name:

```bash
podman volume create videolingo-models
podman volume create videolingo-users

podman run -d \
  --name videolingo \
  --restart=unless-stopped \
  --device nvidia.com/gpu=all \
  --shm-size=2g \
  -p 8501:8501 \
  -v videolingo-models:/app/_model_cache \
  -v videolingo-users:/app/users \
  -v "$(pwd)/auth.yaml:/app/auth.yaml:ro" \
  videolingo:local
```

Docker uses `--gpus all`:

```bash
docker volume create videolingo-models
docker volume create videolingo-users

docker run -d \
  --name videolingo \
  --restart unless-stopped \
  --gpus all \
  --shm-size=2g \
  -p 8501:8501 \
  -v videolingo-models:/app/_model_cache \
  -v videolingo-users:/app/users \
  -v "$(pwd)/auth.yaml:/app/auth.yaml:ro" \
  videolingo:local
```

Open `http://localhost:8501`. Inspect status and logs with:

```bash
podman ps --filter name=videolingo
podman logs -f videolingo

# Docker users can use docker ps / docker logs.
docker ps --filter name=videolingo
docker logs -f videolingo
```

The image includes a health check against `/_stcore/health`.

## Mount Existing Models

When models already exist on the host, replace the two named-volume arguments in the run command with bind mounts:

```bash
-v /path/to/models:/app/_model_cache
-v /path/to/users:/app/users
```

The mounted directories must be writable by the container user. Its default UID/GID is `10001:10001`; match the host user at build time when needed:

```bash
podman build --format docker \
  --build-arg APP_UID=$(id -u) \
  --build-arg APP_GID=$(id -g) \
  -t videolingo:local .
```

## Update

Rebuild and replace the container after pulling source updates. Named volumes preserve models, user configuration, and generated files:

```bash
git pull
podman build --format docker -t videolingo:local .
podman rm -f videolingo
# Run the podman run command above again; Docker users can replace the command name.
```

## Notes

- The image contains CUDA/cuDNN runtime libraries rather than the compiler toolchain.
- The build verifies that the interpreter is Python 3.11.
- Local `auth.yaml`, `users/`, `_model_cache/`, and output directories are excluded by `.dockerignore`.
- spaCy language models are downloaded into a writable runtime package directory when first used. Recreating the container may download them again; preinstall them or mount `/app/.runtime_packages` to persist them.
- When using remote Parakeet/QwenASR services, `127.0.0.1` in application configuration refers to the container itself. Use an address reachable from the container.

