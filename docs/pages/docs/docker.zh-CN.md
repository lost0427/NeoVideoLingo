# Docker / Podman 部署

当前镜像直接打包本地工作树中的代码，使用 Python 3.11、PyTorch 2.8 和 CUDA 12.8。镜像中包含 FFmpeg、OpenCV/SoundFile 所需动态库及 Noto 多语言字体；模型、用户配置和处理结果保存在挂载目录中。

## 准备工作

- Docker 24+ 或 Podman 4.6+
- NVIDIA 显卡驱动需支持 CUDA 12.8
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- 建议至少预留 20 GB 磁盘空间；模型会在首次使用时下载

Podman 使用 CDI 访问 NVIDIA GPU。安装 NVIDIA Container Toolkit 后生成 CDI 配置：

```bash
sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml
nvidia-ctk cdi list
```

先准备登录配置，不要把真实凭据构建进镜像：

```bash
cp auth.yaml.example auth.yaml
# 编辑 auth.yaml，设置用户、密码以及非空的 cookie.name/cookie.key
```

## 在 GitHub 上构建镜像

仓库中的 `.github/workflows/container-image.yml` 会使用 GitHub Hosted Runner 构建镜像并推送到 GitHub Container Registry（GHCR），本地无需执行构建：

- 推送 `v1.0.0` 这类 Git 标签时构建并发布：`v1.0.0` 与 `latest`（同一次构建）
- 推送到 `main` 不会构建
- 在 GitHub Actions 页面执行 `workflow_dispatch`：可手动触发（无 `v*` 标签时不会生成版本 tag）

镜像地址会自动使用小写仓库名：

```text
ghcr.io/<owner>/<repository>:latest
```

当前仓库对应 `ghcr.io/lost0427/neovideolingo:latest`。

构建完成后直接拉取：

```bash
podman pull ghcr.io/<owner>/<repository>:latest
# 或
docker pull ghcr.io/<owner>/<repository>:latest
```

工作流使用仓库自带的 `GITHUB_TOKEN` 推送镜像，已经声明 `packages: write` 权限。首次发布后，可在 GitHub 的 Packages 设置中调整镜像可见性。基础 PyTorch 镜像当前只提供 `linux/amd64`，工作流也固定构建该平台。

## 本地构建

在项目根目录选择一种容器引擎执行：

```bash
# Podman。Docker 镜像格式会保留 Dockerfile 中的健康检查配置。
podman build --format docker -t videolingo:local .

# Docker
docker build -t videolingo:local .
```

依赖层只会在 `requirements.txt` 变化时重新安装。镜像默认使用 `pytorch/pytorch:2.8.0-cuda12.8-cudnn9-runtime`，也可以在构建时覆盖基础镜像：

```bash
podman build --format docker \
  --build-arg PYTORCH_IMAGE=pytorch/pytorch:2.8.0-cuda12.8-cudnn9-runtime \
  -t videolingo:local .
```

## 运行

推荐用命名卷保存模型与用户数据。Podman 使用 CDI 设备名：

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

Docker 使用 `--gpus all`：

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

浏览器访问 `http://localhost:8501`。查看启动状态和日志：

```bash
podman ps --filter name=videolingo
podman logs -f videolingo

# Docker 用户使用 docker ps / docker logs
docker ps --filter name=videolingo
docker logs -f videolingo
```

容器内置健康检查，请求地址为 `/_stcore/health`。

## 挂载已有模型

如果模型已位于宿主机目录中，将运行命令里的两个命名卷替换为绑定挂载：

```bash
-v /path/to/models:/app/_model_cache
-v /path/to/users:/app/users
```

挂载目录需要允许容器用户写入。镜像内应用用户默认 UID/GID 为 `10001:10001`，构建时可通过 `APP_UID` 和 `APP_GID` 调整：

```bash
podman build --format docker \
  --build-arg APP_UID=$(id -u) \
  --build-arg APP_GID=$(id -g) \
  -t videolingo:local .
```

## 更新

拉取项目更新后重新构建并替换容器。命名卷中的模型、用户配置与处理结果会保留：

```bash
git pull
podman build --format docker -t videolingo:local .
podman rm -f videolingo
# 再次执行上面的 podman run 命令；Docker 用户替换命令名即可
```

## 说明

- 镜像只包含运行时 CUDA/cuDNN，不包含编译工具链。
- 构建过程会校验解释器必须为 Python 3.11。
- 本地 `auth.yaml`、`users/`、`_model_cache/` 和输出目录均由 `.dockerignore` 排除。
- spaCy 语言模型会在首次使用相应语言时下载到容器的可写运行目录。重建容器后可能重新下载；若需要完全持久化，可预先安装模型或另外挂载 `/app/.runtime_packages`。
- 使用远程 Parakeet/QwenASR 服务时，配置中的 `127.0.0.1` 指向容器自身，应填写容器可访问的服务地址。

