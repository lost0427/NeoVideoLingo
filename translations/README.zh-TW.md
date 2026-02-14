<div align="center">

<img src="/docs/logo.png" alt="VideoLingo Logo" height="140">

# 連接世界每一幀

<a href="https://trendshift.io/repositories/12200" target="_blank"><img src="https://trendshift.io/api/badge/repositories/12200" alt="Huanshere%2FVideoLingo | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[**English**](/translations/README.en.md)｜[**简体中文**](/README.md)｜[**繁體中文**](/translations/README.zh-TW.md)｜[**日本語**](/translations/README.ja.md)｜[**Español**](/translations/README.es.md)｜[**Русский**](/translations/README.ru.md)｜[**Français**](/translations/README.fr.md)

</div>

基於 [Huanshere/VideoLingo](https://github.com/Huanshere/VideoLingo) 的二次開發版本。  
原版完整功能和文檔請見 [原倉庫](https://github.com/Huanshere/VideoLingo)。


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