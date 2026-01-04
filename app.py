from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gtts import gTTS
import io

app = FastAPI(title="Malayalam TTS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TTSRequest(BaseModel):
    text: str
    lang: str = "ml"

@app.post("/tts")
async def text_to_speech(req: TTSRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text is empty")

    try:
        mp3_fp = io.BytesIO()
        tts = gTTS(text=req.text, lang=req.lang, slow=False)
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        return StreamingResponse(
            mp3_fp,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=tts.mp3"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
