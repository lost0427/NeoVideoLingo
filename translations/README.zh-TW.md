<div align="center">

<img src="/docs/logo.png" alt="VideoLingo Logo" height="140">

# 連接世界每一幀

<a href="https://trendshift.io/repositories/12200" target="_blank"><img src="https://trendshift.io/api/badge/repositories/12200" alt="Huanshere%2FVideoLingo | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[**English**](/translations/README.en.md)｜[**简体中文**](/README.md)｜[**繁體中文**](/translations/README.zh-TW.md)｜[**日本語**](/translations/README.ja.md)｜[**Español**](/translations/README.es.md)｜[**Русский**](/translations/README.ru.md)｜[**Français**](/translations/README.fr.md)

</div>

基於 [Huanshere/VideoLingo](https://github.com/Huanshere/VideoLingo) 的二次開發版本。  
原版完整功能和文檔請見 [原倉庫](https://github.com/Huanshere/VideoLingo)。

## 簡介
VideoLingo 是一站式視頻翻譯本地化配音工具，能夠一鍵生成 Netflix 級別的高質量字幕，告別生硬機翻，告別多行字幕，還能加上高質量的克隆配音，讓全世界的知識能夠跨越語言的障礙共享。

主要特點和功能：

🎥 使用 yt-dlp 從 Youtube 鏈接下載視頻

🎙️ 使用 WhisperX 進行單詞級和低幻覺字幕識別

📝 使用 NLP 和 AI 進行字幕分割

📚 自定義 + AI 生成術語庫，保證翻譯連貫性

🔄 三步直譯、反思、意譯，實現影視級翻譯質量

✅ 按照 Netflix 標準檢查單行長度，絕無雙行字幕

🗣️ 支持 GPT-SoVITS、Azure、OpenAI 等多種配音方案

🚀 一鍵啟動，在 streamlit 中一鍵出片

🌍 多語言支持就緒的 streamlit UI

📝 詳細記錄每步操作日誌，支持隨時中斷和恢復進度

與同類項目相比的優勢：絕無多行字幕，最佳的翻譯質量，無縫的配音體驗

## 語言支持
輸入語言支持：

🇨🇳 中文 | 🇺🇸 英語 | 🇷🇺 俄語 | 🇫🇷 法語 | 🇩🇪 德語 | 🇮🇹 義大利語 | 🇪🇸 西班牙語 | 🇯🇵 日語 | 🇧🇬 保加利亞語 | 🇭🇷 克羅埃西亞語 | 🇨🇿 捷克語 | 🇩🇰 丹麥語 | 🇳🇱 荷蘭語 | 🇪🇪 愛沙尼亞語 | 🇫🇮 芬蘭語 | 🇬🇷 希臘語 | 🇭🇺 匈牙利語 | 🇱🇻 拉脫維亞語 | 🇱🇹 立陶宛語 | 🇲🇹 馬爾他語 | 🇵🇱 波蘭語 | 🇵🇹 葡萄牙語 | 🇷🇴 羅馬尼亞語 | 🇸🇰 斯洛伐克語 | 🇸🇮 斯洛維尼亞語 | 🇸🇪 瑞典語 | 🇺🇦 烏克蘭語

## 最近更新

2026年1月
- 更新依賴 - 包括之前導致報錯的舊版av
- 優化自動安裝依賴腳本
- 更新新版Streamlit寬度/圖標寬度設定方法
- 增加獲取可用模型的功能
- 自動維護翻譯文件
- 修改按鈕字體顏色
- 側邊欄 RoFormer 開關
- 更新到最新版 WhisperX
- 用 BS-RoFormer 替代 Demucs

2025年12月
- 隱藏YouTube下載進度條
- 修復路徑錯誤

2025年11月
- 修復路徑錯誤
- 修復冒號分割錯誤
- 修復封面圖
- 啟用無頭模式

2025年10月
- 修復對齊失敗問題
- 支持Parakeet轉錄
**https://github.com/lost0427/parakeet-api-vl**

2025年9月
- 修復歸檔到history
- WhisperX 參數設置更新
- 強提示詞更新
- 封面圖代理
- 展示標準和最大封面圖
- 修復metadata背景顏色問題
- 處理youtube shorts
- Windows服務腳本
- 自定義vad參數
- 發佈時間轉換
- 圖片和文字樣式修改
- 下載視頻按鈕
- youtu.be 支持
- 清洗YouTube鏈接
- 更新選項翻譯
- 顯示YouTube視頻信息開關
- 可選下載 h264 (mp4) 開關
- 顯示YouTube視頻信息和封面圖
- 禁止同時運行多個WhisperX
- 禁止同時運行多個demucs導致報錯
- 多用戶認證示例配置文件
- 添加用戶登錄系統，初步完成多用戶支持

## 注意

本倉庫並不維護配音部分

## 安裝方法

```
conda create -n videolingo python==3.11.13
conda activate videolingo
python ./install.py
```