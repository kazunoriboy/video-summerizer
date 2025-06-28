import whisper
import os
from pathlib import Path # ファイルパスの操作を簡単にするライブラリ

# --- 設定項目 ---
# 1. 音声ファイルがまとめて入っているフォルダのパスを指定してください
AUDIO_FOLDER_PATH = "./output"  # 例: "/Users/yourname/Desktop/audio_files"

# 2. 結果のテキストファイルを保存するフォルダのパスを指定してください
#    このフォルダは、存在しない場合に自動で作成されます
OUTPUT_FOLDER_PATH = "./transcribed" # 例: "/Users/yourname/Desktop/transcribed_results"

# 3. 使用するモデルサイズ ("tiny", "base", "small", "medium", "large")
MODEL_SIZE = "large"

# 4. 処理対象とするファイルの拡張子 (必要に応じて追加・削除してください)
SUPPORTED_EXTENSIONS = ('.mp3', '.m4a', '.wav', '.mp4', '.mov')
# -----------------


def main():
    """
    指定されたフォルダ内の音声ファイルを一括で文字起こしするメインの関数
    """
    # --- 1. 準備 ---
    audio_folder = Path(AUDIO_FOLDER_PATH)
    output_folder = Path(OUTPUT_FOLDER_PATH)

    # 入力フォルダの存在を確認
    if not audio_folder.is_dir():
        print(f"エラー: 指定された音声フォルダが見つかりません: {audio_folder}")
        return

    # 出力フォルダを作成 (存在しない場合)
    output_folder.mkdir(parents=True, exist_ok=True)

    # 処理対象のファイルをリストアップ
    audio_files = [f for f in audio_folder.iterdir() if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]

    if not audio_files:
        print(f"フォルダ '{audio_folder}' 内に処理対象の音声ファイルが見つかりませんでした。")
        return

    total_files = len(audio_files)
    print(f"合計 {total_files} 個の音声ファイルを処理します。")

    # --- 2. モデルのロード (ループの外で一度だけ行い、時間を節約) ---
    print(f"\nモデル '{MODEL_SIZE}' をロード中...")
    try:
        model = whisper.load_model(MODEL_SIZE)
        print("モデルのロードが完了しました。")
    except Exception as e:
        print(f"モデルのロード中にエラーが発生しました: {e}")
        return

    # --- 3. 各ファイルを順番に処理 ---
    for i, audio_file_path in enumerate(audio_files):
        print(f"\n--- ({i + 1}/{total_files}) 処理開始: {audio_file_path.name} ---")

        # 出力ファイルパスを生成 (例: meeting.mp3 -> meeting.txt)
        output_file_name = audio_file_path.stem + ".txt"
        output_file_path = output_folder / output_file_name

        # もし既に出力ファイルが存在する場合は、処理をスキップ
        if output_file_path.exists():
            print(f"結果ファイルが既に存在するため、スキップします: {output_file_path.name}")
            continue

        # 文字起こしを実行
        try:
            print("文字起こしを実行中...")
            result = model.transcribe(str(audio_file_path), language="ja", fp16=False)
            transcribed_text = result["text"]

            # 結果をUTF-8形式でテキストファイルに保存
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(transcribed_text)
            print(f"結果を '{output_file_path}' に保存しました。")

        except Exception as e:
            # エラーが発生しても処理を止めず、次のファイルに進む
            print(f"エラー: ファイル '{audio_file_path.name}' の処理中にエラーが発生しました。")
            print(f"詳細: {e}")
            continue

    print("\nすべての処理が完了しました。")


if __name__ == "__main__":
    main()
