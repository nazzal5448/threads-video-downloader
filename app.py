from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import asyncio
from typing import Optional
from starlette.status import HTTP_403_FORBIDDEN

from main import extract_url  

app = FastAPI()

# ALLOWING SELECTED DOMAINS
ALLOWED_ORIGINS = ["https://yourdomain.com"]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: HttpUrl

# SIMPLE BOT PROTECTION
def is_bot(user_agent: Optional[str]) -> bool:
    bot_keywords = ["bot", "crawl", "spider", "scrapy", "wget", "curl"]
    return any(bot in (user_agent or "").lower() for bot in bot_keywords)
@app.get("/")
def home():
    return {
        "message": "The App is running!"
    }

@app.post("/extract")
async def extract_video(request: Request, body: URLRequest):
    user_agent = request.headers.get("User-Agent", "")
    if is_bot(user_agent):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Bots are not allowed.")

    try:
        video_url = await extract_url(str(body.url))
        if not video_url:
            raise HTTPException(status_code=404, detail="Video URL not found.")
        return {"video_url": video_url}
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Request timed out.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
