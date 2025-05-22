import os
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
    priority: int = 0,
    url: str | None = None,
    url_title: str | None = None
) -> None:
    payload = {
        "token": API_TOKEN,
        "user": USER_KEY,
        "message": message,
        "title": title,
        "priority": priority,
    }
    
    # Add optional URL parameters if provided
    if url:
        payload["url"] = url
    if url_title:
        payload["url_title"] = url_title

    print(f"USER_KEY {USER_KEY}")
    print(f"API_URL {API_URL}")
    
    resp = requests.post(API_URL, data=payload)
    resp.raise_for_status()
