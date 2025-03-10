from googletrans import Translator

def translate_text(text, source_language, target_language):
  """
  翻譯指定的文字，從來源語言到目標語言。

  參數:
    text: 要翻譯的文字。
    source_language: 來源語言的語言代碼 (例如，'zh-cn' 為簡體中文，'zh-tw' 為繁體中文)。
    target_language: 目標語言的語言代碼 (例如，'en' 為英文)。

  回傳值:
    翻譯後的文字，或在翻譯失敗時回傳 None。
  """

  try:
    translator = Translator()
    translation = translator.translate(text, src=source_language, dest=target_language)
    return translation.text

  except ImportError:
    print("錯誤: 'googletrans' 庫尚未安裝。")
    return None

  except Exception as e:
    print(f"翻譯過程中發生錯誤: {e}")
    return None

if __name__ == "__main__":
  while True:
    try:
      direction = input("請選擇翻譯方向 (1: 中文 -> 英文, 2: 英文 -> 中文 please paste chinese if you can't type'): ")

      if direction == '1':
        source_lang = 'zh-tw'  # 假設輸入的是繁體中文，可根據需要更改
        target_lang = 'en'
      elif direction == '2':
        source_lang = 'en'
        target_lang = 'zh-tw'  # 假設輸出為繁體中文，可根據需要更改
      else:
        print("無效的選擇，請輸入 1 或 2。")
        continue

      text = input("請輸入要翻譯的文字: ")
      translated_text = translate_text(text, source_lang, target_lang)

      if translated_text:
        print(f"翻譯結果: {translated_text}")
      else:
        print("翻譯失敗。")

    except KeyboardInterrupt:
      print("\n程式結束...")
      break