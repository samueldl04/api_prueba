import os
from fastapi import HTTPException
import httpx
import requests
from dotenv import load_dotenv

load_dotenv()

import os
import requests

USER_KEY = os.getenv("PUSHOVER_USER_KEY")
API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")
API_URL = "https://api.pushover.net/1/messages.json"

def send_pushover_notification(
    message: str,
    title: str = "Notificación FastAPI",
    sound: str = "echo",     # ← Pushover Echo (long)
    priority: int = 2,       # ← emergencia
    retry: int = 30,         # reintentos cada 30 s
    expire: int = 180,       # durante 180 s (3 min)
    url: str | None = None,
    url_title: str | None = None
) -> None:
    payload = {
        "token":    API_TOKEN,
        "user":     USER_KEY,
        "message":  message,
        "title":    title,
        "sound":    sound,
        "priority": priority,
    }
    if priority == 2:
        payload["retry"]  = retry
        payload["expire"] = expire

    if url:
        payload["url"]       = url
    if url_title:
        payload["url_title"] = url_title

    resp = requests.post(API_URL, data=payload)
    resp.raise_for_status()
    print("¡Notificación enviada!")

async def trigger_relay_sync(url):
    async with httpx.AsyncClient(timeout=5.0) as client:
        await client.get(url)