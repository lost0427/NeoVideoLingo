<div align="center">

<img src="/docs/logo.webp" alt="VideoLingo Logo" height="140">

# 连接世界每一帧

<a href="https://trendshift.io/repositories/12200" target="_blank"><img src="https://trendshift.io/api/badge/repositories/12200" alt="Huanshere%2FVideoLingo | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[**English**](/translations/README.en.md)｜[**简体中文**](/README.md)｜[**繁體中文**](/translations/README.zh-TW.md)｜[**日本語**](/translations/README.ja.md)｜[**Español**](/translations/README.es.md)｜[**Русский**](/translations/README.ru.md)｜[**Français**](/translations/README.fr.md)

</div>

基于 [Huanshere/VideoLingo](https://github.com/Huanshere/VideoLingo) 的二次开发版本。  
原版完整功能和文档请见 [原仓库](https://github.com/Huanshere/VideoLingo)。

## 简介
NeoVideoLingo：一站式高质量视频本地化工具

🎥 智能处理：集成 yt-dlp 下载 WhisperX / Parakeet 识别，通过 NLP 算法精确进行字幕分割。

📝 完美翻译：采用“直译-反思-意译”三步流程，结合自定义术语库，拒绝机翻感。

✅ 视觉体验：严格执行 Netflix 字幕标准，确保每一句都是单行展示，阅读无压力。

🗣️ 语音合成：即将上线 indextts2.0 支持。

🚀 便捷操作：Streamlit 界面一键启动，全程日志记录，支持随时中断恢复。

## 语言支持
输入语言支持：

🇨🇳 中文 | 🇺🇸 英语 | 🇷🇺 俄语 | 🇫🇷 法语 | 🇩🇪 德语 | 🇮🇹 意大利语 | 🇪🇸 西班牙语 | 🇯🇵 日语 | 🇧🇬 保加利亚语 | 🇭🇷 克罗地亚语 | 🇨🇿 捷克语 | 🇩🇰 丹麦语 | 🇳🇱 荷兰语 | 🇪🇪 爱沙尼亚语 | 🇫🇮 芬兰语 | 🇬🇷 希腊语 | 🇭🇺 匈牙利语 | 🇱🇻 拉脱维亚语 | 🇱🇹 立陶宛语 | 🇲🇹 马耳他语 | 🇵🇱 波兰语 | 🇵🇹 葡萄牙语 | 🇷🇴 罗马尼亚语 | 🇸🇰 斯洛伐克语 | 🇸🇮 斯洛文尼亚语 | 🇸🇪 瑞典语 | 🇺🇦 乌克兰语

## 最近更新

2026年1月
- 更新依赖 - 包括之前导致报错的旧版av
- 优化自动安装依赖脚本
- 更新新版Streamlit宽度/图标宽度设定方法
- 增加获取可用模型的功能
- 自动维护翻译文件
- 修改按钮字体颜色
- 侧边栏 RoFormer 开关
- 更新到最新版 WhisperX
- 用 BS-RoFormer 替代 Demucs

2025年12月
- 隐藏YouTube下载进度条
- 修复路径错误

2025年11月
- 修复路径错误
- 修复冒号分割错误
- 修复封面图
- 启用无头模式

2025年10月
- 修复对齐失败问题
- 支持Parakeet转录
**https://github.com/lost0427/parakeet-api-vl**

2025年9月
- 修复归档到history
- WhisperX 参数设置更新
- 强提示词更新
- 封面图代理
- 展示标准和最大封面图
- 修复metadata背景颜色问题
- 处理youtube shorts
- Windows服务脚本
- 自定义vad参数
- 发布时间转换
- 图片和文字样式修改
- 下载视频按钮
- youtu.be 支持
- 清洗YouTube链接
- 更新选项翻译
- 显示YouTube视频信息开关
- 可选下载 h264 (mp4) 开关
- 显示YouTube视频信息和封面图
- 禁止同时运行多个WhisperX
- 禁止同时运行多个demucs导致报错
- 多用户认证示例配置文件
- 添加用户登录系统，初步完成多用户支持

## 注意

本仓库并不维护配音部分

## 安装方法

```
conda create -n videolingo python==3.11.13
conda activate videolingo
python ./install.py
```