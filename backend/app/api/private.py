from fastapi import APIRouter, HTTPException
from ..db import Message, StoreMessages


router = APIRouter()

@router.post("/send/private")
def send_private_message(message:Message):
    from .websocket import active_connection, user_messages
    recipient_ws = active_connection.get(message.recipient)
    stored_message = StoreMessages(
            sender=message.sender,
            message=message.content
        )
    
    user_messages.setdefault(message.recipient,[]).append(stored_message)

    if  recipient_ws:
        recipient_ws.send_json({"type": "message", "content": message.content})
    
    return {"status":"sent"}


@router.get("/message/{user_id}")
def get_user_messages(user_id: str):
    from .websocket import active_connection, user_messages
    if  user_id in user_messages:
        return user_messages[user_id]
    raise  HTTPException(status_code=404, detail="User not found")  # 404 Not Found

