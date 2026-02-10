
import os
import whisper


_MODEL = None

def get_model(size: str = "base"):
    global _MODEL
    if _MODEL is None:
        print(f"Loading Whisper model: {size} ...")
        _MODEL = whisper.load_model(size)
    return _MODEL

def transcribe_file(audio_path: str, model_size: str = "base") -> str:
    model = get_model(model_size)
    print(f" Transcribing: {audio_path}")
    result = model.transcribe(audio_path)
    return result.get("text", "").strip()
