<div align="center">

<img src="/docs/logo.png" alt="VideoLingoロゴ" height="140">

# 世界中のすべてのフレームをつなぐ

<a href="https://trendshift.io/repositories/12200" target="_blank"><img src="https://trendshift.io/api/badge/repositories/12200" alt="Huanshere%2FVideoLingo | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[**English**](/translations/README.en.md)｜[**简体中文**](/README.md)｜[**繁體中文**](/translations/README.zh-TW.md)｜[**日本語**](/translations/README.ja.md)｜[**Español**](/translations/README.es.md)｜[**Русский**](/translations/README.ru.md)｜[**Français**](/translations/README.fr.md)

</div>

[Huanshere/VideoLingo](https://github.com/Huanshere/VideoLingo) をベースにした二次開発バージョンです。  
元のバージョンの完全な機能とドキュメントについては、[元リポジトリ](https://github.com/Huanshere/VideoLingo) をご覧ください。

## 紹介
VideoLingo はワンステップで動画翻訳・ローカライズ・吹き替えを実現するツールで、Netflixレベルの高品質字幕をワンクリックで生成できます。硬直した機械翻訳や複数行の字幕を排除し、高品質な音声合成による吹き替えも可能で、世界中の知識が言語の壁を超えて共有できるようにします。

主な特徴と機能：

🎥 yt-dlpを使用してYouTubeリンクから動画をダウンロード

🎙️ WhisperXを使用した単語単位および低ハルシネーションの字幕認識

📝 NLPとAIを使用した字幕分割

📚 カスタム + AI生成用語集で翻訳の一貫性を確保

🔄 直訳→検討→意訳の3段階で映画級の翻訳品質を実現

✅ Netflix基準で1行の長さをチェックし、絶対に2行字幕にはなりません

🗣️ GPT-SoVITS、Azure、OpenAIなど複数の吹き替え方式に対応

🚀 ワンクリック起動、streamlit上でワンクリックで出力

🌍 多言語対応のstreamlit UI

📝 各工程の詳細ログを記録し、いつでも中断・再開可能

同様のプロジェクトとの比較での優位性：複数行字幕なし、最高の翻訳品質、シームレスな吹き替え体験

## 言語サポート
入力言語サポート：

🇨🇳 中国語 | 🇺🇸 英語 | 🇷🇺 ロシア語 | 🇫🇷 フランス語 | 🇩🇪 ドイツ語 | 🇮🇹 イタリア語 | 🇪🇸 スペイン語 | 🇯🇵 日本語 | 🇧🇬 ブルガリア語 | 🇭🇷 クロアチア語 | 🇨🇿 チェコ語 | 🇩🇰 デンマーク語 | 🇳🇱 オランダ語 | 🇪🇪 エストニア語 | 🇫🇮 フィンランド語 | 🇬🇷 ギリシャ語 | 🇭🇺 ハンガリー語 | 🇱🇻 ラトビア語 | 🇱🇹 リトアニア語 | 🇲🇹 マルタ語 | 🇵🇱 ポーランド語 | 🇵🇹 ポルトガル語 | 🇷🇴 ルーマニア語 | 🇸🇰 スロバキア語 | 🇸🇮 スロベニア語 | 🇸🇪 スウェーデン語 | 🇺🇦 ウクライナ語

## 最近の更新

2026年1月
- 依存関係を更新 - 以前エラーが発生していた古いavを含む
- 依存関係自動インストールスクリプトを最適化
- 新しいStreamlitの幅/アイコン幅設定方法を更新
- 利用可能なモデルを取得する機能を追加
- 翻訳ファイルを自動メンテナンス
- ボタンのフォント色を変更
- サイドバー RoFormer スイッチ
- 最新バージョンのWhisperXに更新
- BS-RoFormerでDemucsを置き換え

2025年12月
- YouTubeダウンロードプログレスバーを非表示
- パスエラーを修正

2025年11月
- パスエラーを修正
- コロン分割エラーを修正
- カバーアートを修正
- ヘッドレスモードを有効化

2025年10月
- アラインメント失敗の問題を修正
- Parakeet転写をサポート
**https://github.com/lost0427/parakeet-api-vl**

2025年9月
- historyへのアーカイブを修正
- WhisperXパラメータ設定を更新
- 強いプロンプトワードを更新
- カバーアートプロキシ
- 標準と最大カバーアートを表示
- metadataの背景色の問題を修正
- youtube shortsを処理
- Windowsサービススクリプト
- カスタムvadパラメータ
- 公開日時変換
- 画像とテキストスタイルの変更
- ビデオダウンロードボタン
- youtu.be対応
- YouTubeリンクをクリーンアップ
- オプション翻訳を更新
- YouTubeビデオ情報表示スイッチ
- h264 (mp4) のオプショナルダウンロードスイッチ
- YouTubeビデオ情報とカバーアートを表示
- 複数のWhisperXの同時実行を禁止
- 複数のdemucsが同時に実行されてエラーになることを防止
- マルチユーザ認証サンプル設定ファイル
- ユーザーログインシステムを追加し、マルチユーザー対応を初期完了

## 注意

このリポジトリは吹き替え部分は保守していません

## インストール方法

```
conda create -n videolingo python==3.11.13
conda activate videolingo
python ./install.py
```