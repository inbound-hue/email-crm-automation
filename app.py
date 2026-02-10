import os
from dotenv import load_dotenv
import whisper


print(" Loading Whisper model (this may take a minute)...")
model = whisper.load_model("base")

audio_path = r"C:\Users\HP\Downloads\PythonProject\.venv\Horbach.ogg"

print(" Transcribing audio locally... please wait.")
result = model.transcribe(audio_path, language="de")
text = result["text"].strip()

print("\n Transcribed text (German):\n")
print(text)

# === 2. Summarization (free + local) ===
print("\n Summarizing locally... please wait.\n")

from transformers import pipeline

# Load a small summarization model (English)
summarizer_en = pipeline("summarization", model="facebook/bart-large-cnn")

# Translate German → English first (for English summary)
translator_to_en = pipeline("translation", model="Helsinki-NLP/opus-mt-de-en")
translator_to_de = pipeline("translation", model="Helsinki-NLP/opus-mt-en-de")

# Step 1: Translate German text to English
english_text = translator_to_en(text)[0]["translation_text"]

# Step 2: Summarize the English text
english_summary = summarizer_en(english_text, max_length=130, min_length=40, do_sample=False)[0]["summary_text"]

# Step 3: Translate English summary back to German
german_summary = translator_to_de(english_summary)[0]["translation_text"]

print(" Summary in English:\n", english_summary)
print("\n🇩🇪 Zusammenfassung auf Deutsch:\n", german_summary)

# === 3. Optional: Save to file ===
output_path = r"C:\Users\HP\Downloads\PythonProject\.venv\summary.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("=== Transcribed Text (German) ===\n")
    f.write(text + "\n\n")
    f.write("=== Summary (English) ===\n")
    f.write(english_summary + "\n\n")
    f.write("=== Zusammenfassung (Deutsch) ===\n")
    f.write(german_summary + "\n")

print(f"\n Summaries saved to: {output_path}")



