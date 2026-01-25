<div align="center">

<img src="/docs/logo.png" alt="VideoLingoロゴ" height="140">

# 世界中のすべてのフレームをつなぐ

<a href="https://trendshift.io/repositories/12200" target="_blank"><img src="https://trendshift.io/api/badge/repositories/12200" alt="Huanshere%2FVideoLingo | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[**English**](/translations/README.en.md)｜[**简体中文**](/README.md)｜[**繁體中文**](/translations/README.zh-TW.md)｜[**日本語**](/translations/README.ja.md)｜[**Español**](/translations/README.es.md)｜[**Русский**](/translations/README.ru.md)｜[**Français**](/translations/README.fr.md)

</div>

[Huanshere/VideoLingo](https://github.com/Huanshere/VideoLingo) をベースにした二次開発バージョンです。  
元のバージョンの完全な機能とドキュメントについては、[元リポジトリ](https://github.com/Huanshere/VideoLingo) をご覧ください。


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

2025年11月
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