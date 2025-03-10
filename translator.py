from googletrans import Translator

translator = Translator()
text_to_translate = "you are stupid"
translation = translator.translate(text_to_translate, dest='zh-tw')

print(f"原文: {text_to_translate}")
print(f"翻譯: {translation.text}")