# Voice-enabled Chatbot with Gemini AI and ElevenLabs

音声入出力に対応したAIチャットボットです。Gemini AIによる自然な会話と、ElevenLabsの高品質な音声合成・音声認識を組み合わせています。

## 特徴

- 音声入力とテキスト入力の両方に対応
- 自然な会話が可能なGemini AI統合
- ElevenLabsによる高品質な音声合成（TTS）
- 音声認識（STT）によるハンズフリー操作
- マルチ言語対応（日本語・英語など）

## 必要条件

- Python 3.8+
- ElevenLabs APIキー
- Google Gemini APIキー
- macOS（音声入出力用）

## セットアップ

1. リポジトリをクローン:
   ```bash
   git clone <repository-url>
   cd elevenlabs-demo
   ```

2. 仮想環境を作成して有効化:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windowsの場合は `venv\Scripts\activate`
   ```

3. 依存パッケージをインストール:
   ```bash
   pip install -r requirements.txt
   ```

4. 環境変数の設定:
   ```bash
   cp .env.example .env
   ```
   `.env` ファイルを編集して、APIキーを設定してください。

## 使い方

### 音声入力モードで起動
```bash
python chatbot.py --voice
```

### テキスト入力モードで起動
```bash
python chatbot.py
```

### 音声入力モードの操作
1. 起動すると「録音ボタンを押して話してください...」と表示されます
2. Enterキーを押すと5秒間の録音が開始されます
3. 話しかけると音声が認識され、AIが応答します
4. 終了するには Ctrl+C を押してください

## 設定

### 音声設定
`chatbot.py` の `text_to_speech` 関数内で以下のパラメータを調整できます：

- `stability`: 声の安定性（0-1、低いほど感情豊かに）
- `similarity_boost`: 声の類似度（0-1、高いほど一貫性のある声に）
- `style`: 話し方のスタイル（0-1、高いほど表現豊かに）
- `use_speaker_boost`: 声をよりクリアにする

### ボイス設定
`get_voice_id` 関数で使用するボイスIDを変更できます。

## トラブルシューティング

### 音声が再生されない場合
- システムの音声出力が有効になっているか確認してください
- `mpv` プレイヤーがインストールされている必要があります：
  ```bash
  brew install mpv
  ```

### 音声が認識されない場合
- マイクの接続を確認してください
- 静かな環境でお試しください
- もう少し大きな声ではっきりと話してみてください

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
