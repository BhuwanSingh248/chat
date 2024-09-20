from typing import List
from pydantic import BaseModel


class Message(BaseModel):
    sender:str 
    recipient: str
    content: str


class BroadcastMessage(BaseModel):
    sender:str
    content: str

class StoreMessages(BaseModel):
    sender: str
    message: str

    