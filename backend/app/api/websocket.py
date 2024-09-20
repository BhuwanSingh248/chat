from fastapi import APIRouter, WebSocket
from typing import Dict, List
import json

from ..db import Message, BroadcastMessage, StoreMessages
from .private import get_user_messages, send_private_message
from .broadcast import broadcast

router = APIRouter()


active_connection:Dict[str,  WebSocket] = {}
user_messages:Dict[str, List[StoreMessages]] = {}
@router.websocket("/{user_id}/")
async  def chat(user_id: str, websocket: WebSocket):
    await websocket.accept()  # accept the websocket connection
    active_connection[user_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.load(data)
            if "recipient" in  message_data:
                message = Message(
                    sender = user_id,
                    recipient= message_data['recipient'],
                    content= message_data['message']
                )
                await send_private_message(message)

            elif "broadcast" in message_data:
                broadcast_message = BroadcastMessage(
                    sender=user_id,
                    content= message_data['message']
                )
                await broadcast(broadcast_message)
        
    except Exception as e:
        print(f"Error: {e}")

    finally:
        del active_connection[user_id]

