from fastapi import WebSocket, APIRouter
from random import randint
from src.utils.whisper_utils import transcribe_audio


router = APIRouter(
    prefix="/ws",
    tags=["Websocket"],
    responses={404: {"description": "Not found"}},
)


@router.websocket("/transcriptor")
async def websocket_audio_transcriptor(websocket: WebSocket):
    await websocket.accept()
    full_transcript = ""
    try:
        while True:
            data = await websocket.receive_bytes()
            print(f"Received {len(data)} bytes", flush=True)

            with open("debug_audio.webm", "wb") as f:
                f.write(data)

            text_segment = transcribe_audio(data)
            print(f"Segment transcription: {text_segment}", flush=True)

            full_transcript += text_segment
            await websocket.send_json({"transcription": full_transcript.strip()})
    except Exception as e:
        print(e, flush=True)
        pass


@router.get("/zig")
async def zig():
    return {"zag"}
