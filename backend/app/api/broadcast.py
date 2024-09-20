from fastapi import APIRouter,  Depends, HTTPException
from ..db import BroadcastMessage, StoreMessages
router = APIRouter()



@router.post("/")
async def  broadcast(message: BroadcastMessage):
    from .websocket import active_connection, user_messages
    print(active_connection)
    for user, connection in active_connection.items():
        print("in their")
        user_messages.get(user).append(StoreMessages(
            sender=message.sender,
            message=message.content
        ))
        await connection.send_json(message)
    
    return {
        "status": "sent"
    }
