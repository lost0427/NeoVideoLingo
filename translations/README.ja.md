<div align="center">

<img src="/docs/logo.webp" alt="NeoVideoLingo Logo" height="140">

# 世界中のすべてのフレームをつなぐ

<a href="https://trendshift.io/repositories/12200" target="_blank"><img src="https://trendshift.io/api/badge/repositories/12200" alt="Huanshere%2FVideoLingo | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

[**English**](/translations/README.en.md)｜[**简体中文**](/README.md)｜[**繁體中文**](/translations/README.zh-TW.md)｜[**日本語**](/translations/README.ja.md)｜[**Español**](/translations/README.es.md)｜[**Русский**](/translations/README.ru.md)｜[**Français**](/translations/README.fr.md)

</div>

[Huanshere/VideoLingo](https://github.com/Huanshere/VideoLingo) をベースにした二次開発バージョンです。  
元のバージョンの完全な機能とドキュメントについては、[元リポジトリ](https://github.com/Huanshere/VideoLingo) をご覧ください。

## 紹介
NeoVideoLingo：ワンステップで高品質な動画ローカライズを行うツール

🎥 スマート処理：yt-dlp統合ダウンロード、WhisperX / Parakeet認識、NLPアルゴリズムにより正確な字幕分割を実現。

📝 完璧な翻訳：「直訳-検討-意訳」の3段階プロセスを採用し、カスタム用語集と組み合わせて機械翻訳のような違和感を排除。

✅ 視覚体験：Netflix字幕規格を厳守し、すべての文章を1行表示で読みやすくします。

🗣️ 音声合成：近日中にindextts2.0対応を追加予定。

🚀 操作性：Streamlitインターフェースでワンクリック起動、全工程のログ記録、途中停止・再開に対応。

## 言語サポート
入力言語サポート：

🇨🇳 中国語 | 🇺🇸 英語 | 🇷🇺 ロシア語 | 🇫🇷 フランス語 | 🇩🇪 ドイツ語 | 🇮🇹 イタリア語 | 🇪🇸 スペイン語 | 🇯🇵 日本語 | 🇧🇬 ブルガリア語 | 🇭🇷 クロアチア語 | 🇨🇿 チェコ語 | 🇩🇰 デンマーク語 | 🇳🇱 オランダ語 | 🇪🇪 エストニア語 | 🇫🇮 フィンランド語 | 🇬🇷 ギリシャ語 | 🇭🇺 ハンガリー語 | 🇱🇻 ラトビア語 | 🇱🇹 リトアニア語 | 🇲🇹 マルタ語 | 🇵🇱 ポーランド語 | 🇵🇹 ポルトガル語 | 🇷🇴 ルーマニア語 | 🇸🇰 スロバキア語 | 🇸🇮 スロベニア語 | 🇸🇪 スウェーデン語 | 🇺🇦 ウクライナ語 | 🇭🇰 広東語 | 🇸🇦 アラビア語 | 🇮🇩 インドネシア語 | 🇰🇷 韓国語 | 🇹🇭 タイ語 | 🇻🇳 ベトナム語 | 🇹🇷 トルコ語 | 🇮🇳 インド語 | 🇲🇾 マレー語 | 🇵🇭 フィリピン語 | 🇮🇷 ペルシア語 | 🇲🇰 マセドニア語

サポートされている方言：
安徽、東北、福建、甘粛、貴州、河北、河南、湖北、湖南、江西、寧夏、山東、陝西、山西、四川、天津、雲南、浙江、広東語（香港口音）、広東語（広東口音）、呉語、閩南語

## Qwen3ASR インストールガイド
公式チュートリアルに従ってください：

「私たちの qwen-asr Python パッケージをより簡単に使用するために、事前に構築された Docker イメージ：qwenllm/qwen3-asr を提供しています。GPU ドライバとモデルファイルをインストールするだけでコードを実行できます。Docker が GPU にアクセスできるようにするには、NVIDIA Container Toolkit のインストールガイドに従ってください。中国本土で Docker Hub に接続できない場合は、イメージキャッシュを使用してイメージの取得を高速化できます。」

Windows 上では Docker をインストールし、.ps1 ファイルを作成するか、PowerShell に直接入力してください：

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
ネットワーク問題が発生した場合は、以下の URL を試すことができます。

docker.1ms.run/qwenllm/qwen3-asr

コンテナのダウンロードと起動が成功した後、転写サービスは自動的に開始されません。このプロジェクトの

\core\all_whisper_methods\qwenasrvl.py

```
#vim /usr/local/bin/qwenasrvl
#chmod +x /usr/local/bin/qwenasrvl
#qwenasrvl
```
上記の指示に従ってファイルを書き込み、権限を与えて実行してください。vllmフレームワークを使用し、コンテナの80番ポート（ホストの8700番ポート）で実行されます。

## 最近の更新
2026年2月
- NVML依存関係の置換
- Pydantic の使用
- 有料 TTS の削除
- 翻訳および自動翻訳ツールの最適化、最初のステップに戻るボタンを追加
- 新しい言語転写方式 Qwen3ASR への更新
（Qwen3-ASR-1.7B + Qwen3-ForcedAligner-0.6B）
https://github.com/QwenLM/Qwen3-ASR

2026年1月
- 依存関係の更新 - 以前エラーが発生していた古いavを含む
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

ナレーション部分：間もなくIndex-TTS 2.0に対応予定です。

## インストール方法

```
conda create -n videolingo python==3.11.13
conda activate videolingo
python ./install.py
```

### ユーザー追加方法

1. `auth.yaml.example` を `auth.yaml` としてコピーし、`auth.yaml` にユーザー名とパスワードを入力します。
2. `\users\ユーザー名` フォルダーを作成します。
3. `\users\ユーザー名` の下に `config.yaml` を作成し、`output` フォルダーを作成します。