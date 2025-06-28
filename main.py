
import subprocess
import sys

def run_script(script_name):
    """指定されたPythonスクリプトを実行する"""
    try:
        print(f"--- {script_name} を実行中... ---")
        # Pythonの実行可能ファイルのパスをsys.executableから取得
        python_executable = sys.executable
        result = subprocess.run([python_executable, script_name], check=True, capture_output=True, text=True, encoding='utf-8')
        print(f"--- {script_name} の実行が完了しました。 ---")
        print("標準出力:")
        print(result.stdout)
    except FileNotFoundError:
        print(f"エラー: {script_name} が見つかりません。")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"エラー: {script_name} の実行中にエラーが発生しました。")
        print(f"リターンコード: {e.returncode}")
        print("標準出力:")
        print(e.stdout)
        print("標準エラー:")
        print(e.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        sys.exit(1)

def main():
    """メインの処理フロー"""
    print("動画の要約プロセスを開始します。")

    # 1. 音声抽出
    run_script("extract_audio.py")

    # 2. 文字起こし
    run_script("transcribe_folder.py")

    # 3. 要約
    run_script("summarize_texts_gemini.py")

    print("すべてのプロセスが完了しました。")

if __name__ == "__main__":
    main()
