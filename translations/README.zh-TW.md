<div align="center">

<img src="/docs/logo.webp" alt="NeoVideoLingo Logo" height="140">

# 連接世界每一幀

<a href="https://trendshift.io/repositories/12200" target="_blank"><img src="https://trendshift.io/api/badge/repositories/12200" alt="Huanshere%2FVideoLingo | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[**English**](/translations/README.en.md)｜[**简体中文**](/README.md)｜[**繁體中文**](/translations/README.zh-TW.md)｜[**日本語**](/translations/README.ja.md)｜[**Español**](/translations/README.es.md)｜[**Русский**](/translations/README.ru.md)｜[**Français**](/translations/README.fr.md)

</div>

基於 [Huanshere/VideoLingo](https://github.com/Huanshere/VideoLingo) 的二次開發版本。  
原版完整功能和文檔請見 [原倉庫](https://github.com/Huanshere/VideoLingo)。

## 簡介
NeoVideoLingo：一站式高質量視頻本地化工具

🎥 智能處理：集成 yt-dlp 下載 WhisperX / Parakeet 識別，通過 NLP 算法精確進行字幕分割。

📝 完美翻譯：採用"直譯-反思-意譯"三步流程，結合自定義術語庫，拒絕機翻感。

✅ 視覺體驗：嚴格執行 Netflix 字幕標準，確保每一句都是單行展示，閱讀無壓力。

🗣️ 語音合成：即將上線 indextts2.0 支持。

🚀 便捷操作：Streamlit 界面一鍵啟動，全程日誌記錄，支持隨時中斷恢復。

## 語言支持
輸入語言支持：

🇨🇳 中文 | 🇺🇸 英語 | 🇷🇺 俄語 | 🇫🇷 法語 | 🇩🇪 德語 | 🇮🇹 義大利語 | 🇪🇸 西班牙語 | 🇯🇵 日語 | 🇧🇬 保加利亞語 | 🇭🇷 克羅埃西亞語 | 🇨🇿 捷克語 | 🇩🇰 丹麥語 | 🇳🇱 荷蘭語 | 🇪🇪 愛沙尼亞語 | 🇫🇮 芬蘭語 | 🇬🇷 希臘語 | 🇭🇺 匈牙利語 | 🇱🇻 拉脫維亞語 | 🇱🇹 立陶宛語 | 🇲🇹 馬爾他語 | 🇵🇱 波蘭語 | 🇵🇹 葡萄牙語 | 🇷🇴 羅馬尼亞語 | 🇸🇰 斯洛伐克語 | 🇸🇮 斯洛維尼亞語 | 🇸🇪 瑞典語 | 🇺🇦 烏克蘭語 | 🇭🇰 粤語 | 🇸🇦 阿拉伯語 | 🇮🇩 印尼語 | 🇰🇷 韓語 | 🇹🇭 泰語 | 🇻🇳 越南語 | 🇹🇷 土耳其語 | 🇮🇳 印地語 | 🇲🇾 馬來語 | 🇵🇭 菲律賓語 | 🇮🇷 波斯語 | 🇲🇰 馬其頓語

支持的方言：
安徽、東北、福建、甘肅、貴州、河北、河南、湖北、湖南、江西、寧夏、山東、陝西、山西、四川、天津、雲南、浙江、粵語（香港口音）、粵語（廣東口音）、吳語、閩南語

## Qwen3ASR 安裝教程
根據官方教程：

「為了讓我們的 qwen-asr Python 包更容易使用，我們提供了一個預建構的 Docker 鏡像：qwenllm/qwen3-asr。您只需要安裝 GPU 驅動程式並下載模型文件即可運行代碼。請按照 NVIDIA 容器工具包的安裝指南操作，以確保 Docker 可以訪問您的 GPU。如果您在中國大陸並且無法連接到 Docker Hub，您可以使用鏡像緩存來加速鏡像拉取。」

在 Windows 上，安裝 Docker，創建 .ps1 文件或直接輸入到 PowerShell：

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
如果遇到網絡問題，可以嘗試使用

docker.1ms.run/qwenllm/qwen3-asr

在成功下載並啟動容器後，不會自動開啟轉錄服務，查看本項目的

\core\all_whisper_methods\qwenasrvl.py

```
#vim /usr/local/bin/qwenasrvl
#chmod +x /usr/local/bin/qwenasrvl
#qwenasrvl
```
按提示把文件寫入並給予权限，最後運行。使用 vllm 框架，運行在容器的 80 端口上（主機的 8700 端口）。

## 最近更新
2026年3月
- 更新跳過翻譯功能
- 更新依賴
- 修復多執行緒報錯
- 修復 WhisperX
- 移除字串中多餘的 `f` 前綴
- 更新安裝腳本
- 替換 NVML 依賴

2026年2月
- 使用 Pydantic
- 刪除付費 TTS
- 優化翻譯及自動翻譯工具 增加重置到第一步按鈕
- 更新新的語言轉錄方式 Qwen3ASR
（Qwen3-ASR-1.7B + Qwen3-ForcedAligner-0.6B）
https://github.com/QwenLM/Qwen3-ASR

2026年1月
- 更新依賴 - 包括之前導致報錯的舊版 av
- 優化自動安裝依賴腳本
- 更新新版 Streamlit 寬度/圖標寬度設定方法
- 增加獲取可用模型的功能
- 自動維護翻譯文件
- 修改按鈕字體顏色
- 側邊欄 RoFormer 開關
- 更新到最新版 WhisperX
- 用 BS-RoFormer 替代 Demucs

2025年12月
- 隱藏 YouTube 下載進度條
- 修復路徑錯誤

2025年11月
- 修復路徑錯誤
- 修復冒號分割錯誤
- 修復封面圖
- 啟用無頭模式

2025年10月
- 修復對齊失敗問題
- 支持 Parakeet 轉錄
**https://github.com/lost0427/parakeet-api-vl**

2025年9月
- 修復歸檔到 history
- WhisperX 參數設置更新
- 強提示詞更新
- 封面圖代理
- 展示標準和最大封面圖
- 修復 metadata 背景顏色問題
- 處理 youtube shorts
- Windows 服務腳本
- 自定義 vad 參數
- 發佈時間轉換
- 圖片和文字樣式修改
- 下載視頻按鈕
- youtu.be 支持
- 清洗 YouTube 連結
- 更新選項翻譯
- 顯示 YouTube 視頻信息開關
- 可選下載 h264 (mp4) 開關
- 顯示 YouTube 視頻信息和封面圖
- 禁止同時運行多個 WhisperX
- 禁止同時運行多個 demucs 導致報錯
- 多用戶認證示例配置文件
- 添加用戶登錄系統，初步完成多用戶支持

## 注意

配音部分 即將適配 Indextts2.0

## 安裝方法

```
conda create -n videolingo python==3.11.13
conda activate videolingo
python ./install.py
```

### 新增使用者方法

1. 複製一份 `auth.yaml.example` 為 `auth.yaml`，並在 `auth.yaml` 中填寫使用者名稱與密碼。
2. 建立 `\users\使用者名稱` 資料夾。
3. 在 `\users\使用者名稱` 下放置一份 `config.yaml`，並建立 `output` 資料夾。