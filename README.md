# 動画自動要約プロジェクト

このプロジェクトは、指定されたフォルダ内の動画ファイルを自動的に処理し、文字起こしと要約を生成する一連のスクリプトです。

## 概要

動画から音声を抽出し、その音声をテキストに変換（文字起こし）し、最後にAI（Google Gemini）を使ってテキストの要約を生成します。

処理フローは以下の通りです。
1.  `original` フォルダ内の動画ファイルから音声を抽出 → `output` フォルダ
2.  `output` フォルダ内の音声ファイルを文字起こし → `transcribed` フォルダ
3.  `transcribed` フォルダ内のテキストファイルを要約 → `summeries` フォルダ

## 必要なもの

- Python 3.9 以降
- [FFmpeg](https://ffmpeg.org/): 音声抽出のために必要です。システムにインストールし、パスが通っている必要があります。
- Google APIキー: テキスト要約のために[Google AI Studio](https://aistudio.google.com/app/apikey)で取得したAPIキーが必要です。

## セットアップ

1.  **リポジトリをクローンします**
    ```bash
    git clone <このリポジトリのURL>
    cd <リポジトリ名>
    ```

2.  **Pythonの仮想環境を作成し、有効化します**
    ```bash
    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **必要なライブラリをインストールします**
    `requirements.txt` を使って、必要なPythonライブラリをインストールします。
    ```bash
    pip install -r requirements.txt
    ```
    *(注: `requirements.txt`がない場合は、以下のコマンドで個別にインストールしてください)*
    ```bash
    pip install openai-whisper google-generativeai
    ```

4.  **FFmpegをインストールします**
    -   **macOS (Homebrewを使用):**
        ```bash
        brew install ffmpeg
        ```
    -   **Windows (ChocolateyやScoopを使用):**
        ```bash
        # Chocolatey
        choco install ffmpeg
        # Scoop
        scoop install ffmpeg
        ```
    -   または、[公式サイト](https://ffmpeg.org/download.html)からダウンロードしてインストールし、実行ファイルへのパスをシステムの環境変数に追加してください。

5.  **Google APIキーを設定します**
    取得したAPIキーを環境変数 `GOOGLE_API_KEY` に設定します。
    ```bash
    # macOS / Linux
    export GOOGLE_API_KEY='ここにあなたのAPIキーを入力'

    # Windows (コマンドプロンプト)
    set GOOGLE_API_KEY="ここにあなたのAPIキーを入力"

    # Windows (PowerShell)
    $env:GOOGLE_API_KEY="ここにあなたのAPIキーを入力"
    ```
    この設定はターミナルセッションごとに必要です。恒久的に設定するには、シェルの設定ファイル（`.bashrc`, `.zshrc`など）に追記してください。

## 使い方

1.  **動画ファイルを配置します**
    処理したい動画ファイル（`.mp4`, `.mov`など）を `original` フォルダにコピーします。

2.  **メインスクリプトを実行します**
    以下のコマンドを実行すると、音声抽出、文字起こし、要約の一連の処理が自動的に開始されます。
    ```bash
    python main.py
    ```

3.  **結果を確認します**
    -   文字起こしされたテキストは `transcribed` フォルダに `(元のファイル名).txt` として保存されます。
    -   要約されたテキストは `summeries` フォルダに `(元のファイル名)_summary_short.txt`（短縮版）と `(元のファイル名)_summary_long.txt`（詳細版）として保存されます。

## 各フォルダの役割

-   `./original/`: 処理対象の動画ファイルを置く場所。
-   `./output/`: 動画から抽出された音声ファイル（`.mp3`）が保存される場所。
-   `./transcribed/`: 音声から文字起こしされたテキストファイル（`.txt`）が保存される場所。
-   `./summeries/`: 要約されたテキストファイル（`.txt`）が保存される場所。

## 各スクリプトの詳細

-   `main.py`: 全ての処理を順番に実行するメインスクリプト。
-   `extract_audio.py`: `original` フォルダの動画から音声を抽出し、`output` フォルダに保存します。
-   `transcribe_folder.py`: `output` フォルダの音声ファイルをWhisperで文字起こしし、`transcribed` フォルダに保存します。
-   `summarize_texts_gemini.py`: `transcribed` フォルダのテキストをGemini APIで要約し、`summeries` フォルダに保存します。
