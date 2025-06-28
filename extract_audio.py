import os
import subprocess

# --- 設定項目 ---
# 動画ファイルが保存されているディレクトリのパス
VIDEO_DIR = r"./original" 
# 抽出した音声を保存するディレクトリのパス
AUDIO_DIR = r"./output"
# 抽出する音声のフォーマット (例: "mp3", "wav", "aac")
OUTPUT_FORMAT = "mp3"
# 対象とする動画の拡張子 (小文字で指定)
VIDEO_EXTENSIONS = ('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv')
# -----------------

def extract_audio():
    """
    指定されたディレクトリ内のすべての動画ファイルから音声を抽出する
    """
    # 出力ディレクトリが存在しない場合は作成する
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)
        print(f"作成されたディレクトリ: {AUDIO_DIR}")

    # 入力ディレクトリ内のファイルをループ処理
    for filename in os.listdir(VIDEO_DIR):
        # 指定された拡張子を持つファイルのみを対象とする
        if filename.lower().endswith(VIDEO_EXTENSIONS):
            # 入力ファイルと出力ファイルのフルパスを作成
            video_path = os.path.join(VIDEO_DIR, filename)
            
            # ファイル名から拡張子を除いた部分を取得
            base_filename = os.path.splitext(filename)[0]
            audio_path = os.path.join(AUDIO_DIR, f"{base_filename}.{OUTPUT_FORMAT}")

            print(f"'{filename}' から音声を抽出中...")

            # FFmpegのコマンドをリスト形式で作成
            command = [
                'ffmpeg',
                '-i', video_path,
                '-vn',  # ビデオを無効にする
                '-acodec', 'libmp3lame', # MP3の場合、高品質なエンコーダを指定 (任意)
                '-q:a', '2', # 音質を指定 (MP3の場合 0=最高, 9=最低)
                '-y', # 確認なしで上書き
                audio_path
            ]
            
            # WAVで高音質にしたい場合は、以下のようなコマンドにする
            # if OUTPUT_FORMAT == 'wav':
            #     command = ['ffmpeg', '-i', video_path, '-vn', '-y', audio_path]

            try:
                # FFmpegコマンドを実行
                subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"-> 成功: '{os.path.basename(audio_path)}' が保存されました。")
            except subprocess.CalledProcessError as e:
                print(f"-> エラー: {filename} の処理に失敗しました。")
                print(f"   FFmpegエラー: {e.stderr.decode('utf-8')}")

if __name__ == "__main__":
    extract_audio()
    print("\nすべての処理が完了しました。")
