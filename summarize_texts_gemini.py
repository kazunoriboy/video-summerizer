import google.generativeai as genai
import os
from pathlib import Path
import time

# --- 設定項目 ---
# 1. 文字起こし済みテキストファイルが入っているフォルダ
INPUT_TEXT_FOLDER = "./transcribed"

# 2. 要約結果を保存するフォルダ
OUTPUT_SUMMARY_FOLDER = "./summeries"

# 3. Google Gemini APIモデル
#    高性能: "gemini-1.5-pro-latest"
#    高速・安価: "gemini-1.5-flash-latest"
MODEL_NAME = "gemini-2.5-flash-lite-preview-06-17"
# -----------------

def get_summary_from_gemini(model, text, target_length):
    """Gemini APIを呼び出して、指定した文字数で要約を生成する関数"""
    # Geminiへの指示は、役割と具体的な指示をまとめてプロンプトに含めます
    full_prompt = f"""あなたは、提供された文章を要約するのが得意な、プロの編集者です。
以下の文章を、日本語で{target_length}文字程度に要約してください。文章の主要なトピック、結論、重要なポイントを的確に捉え、自然で分かりやすい文章を作成してください。

---
{text}
"""
    try:
        response = model.generate_content(full_prompt)
        # セーフティ機能で応答がブロックされた場合のチェック
        if not response.parts:
            print("  [!] 応答がブロックされました。不適切な内容と判定された可能性があります。")
            return None
        return response.text.strip()
    except Exception as e:
        print(f"  [!] Gemini APIでエラーが発生しました: {e}")
        return None

def main():
    """指定フォルダ内のテキストファイルを読み込み、Geminiで2種類の要約を生成する"""
    # --- 1. 準備 ---
    # APIキーを環境変数から取得してGeminiを設定
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("環境変数 'GOOGLE_API_KEY' が設定されていません。")
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"Gemini APIの設定に失敗しました: {e}")
        return

    # モデルを初期化
    generation_config = genai.GenerationConfig(temperature=0.5)
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config=generation_config
    )

    input_folder = Path(INPUT_TEXT_FOLDER)
    output_folder = Path(OUTPUT_SUMMARY_FOLDER)

    if not input_folder.is_dir():
        print(f"エラー: 入力フォルダが見つかりません: {input_folder}")
        return

    output_folder.mkdir(parents=True, exist_ok=True)
    text_files = sorted([f for f in input_folder.glob("*.txt")])

    if not text_files:
        print(f"フォルダ '{input_folder}' 内に処理対象の.txtファイルが見つかりませんでした。")
        return

    total_files = len(text_files)
    print(f"合計 {total_files} 個のテキストファイルを処理します。使用モデル: {MODEL_NAME}")

    # --- 2. 各ファイルを順番に処理 ---
    for i, text_file_path in enumerate(text_files):
        print(f"\n--- ({i + 1}/{total_files}) 処理開始: {text_file_path.name} ---")

        with open(text_file_path, "r", encoding="utf-8") as f:
            original_text = f.read()

        if len(original_text.strip()) < 50: # 短すぎるテキストはスキップ
            print("  テキストが短すぎるため、要約をスキップします。")
            continue

        # --- 100文字程度の要約を生成 ---
        print("  > 100文字程度の要約を生成中...")
        summary_short = get_summary_from_gemini(model, original_text, 100)
        if summary_short:
            output_short_path = output_folder / f"{text_file_path.stem}_summary_short.txt"
            with open(output_short_path, "w", encoding="utf-8") as f:
                f.write(summary_short)
            print(f"  > 短い要約を保存しました: {output_short_path.name}")
        
        time.sleep(1) # APIへの連続リクエストを避けるための短い待機

        # --- 1200文字程度の要約を生成 ---
        print("  > 1200文字程度の要約を生成中...")
        summary_long = get_summary_from_gemini(model, original_text, 1200)
        if summary_long:
            output_long_path = output_folder / f"{text_file_path.stem}_summary_long.txt"
            with open(output_long_path, "w", encoding="utf-8") as f:
                f.write(summary_long)
            print(f"  > 長い要約を保存しました: {output_long_path.name}")

    print("\nすべての処理が完了しました。")


if __name__ == "__main__":
    main()
