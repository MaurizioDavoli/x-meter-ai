import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from pydub import AudioSegment
from io import BytesIO
import ffmpeg

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# model_id = "openai/whisper-small"
model_id = "openai/whisper-base"
# model_id = "litus-ai/whisper-small-ita"

torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

print(f"Downloading model {model_id}...", flush=True)
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)
print(f"Model {model_id} downloaded.", flush=True)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)


def _convert_webm_to_wav(webm_bytes):
    try:
        out, _ = (
            ffmpeg.input("pipe:0")
            .output("pipe:1", format="wav")
            .run(input=webm_bytes, capture_stdout=True, capture_stderr=True)
        )
        return out

    except ffmpeg.Error as e:
        print("-" * 10)
        print("FFmpeg error:", e.stderr.decode())
        print("-" * 10)
        return None
    except Exception as e:
        print("*" * 10)
        print(e)
        print("*" * 10)
        return None


def transcribe_audio(audio_bytes: bytes) -> str:
    print(f"Transcribing {len(audio_bytes)} bytes...", flush=True)
    wav_audio = _convert_webm_to_wav(audio_bytes)

    transcription = pipe(wav_audio, return_timestamps=False)

    print(f"Transcription: {transcription['text']}", flush=True)
    return transcription["text"]
