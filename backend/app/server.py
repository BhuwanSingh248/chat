from fastapi import FastAPI

from .api import PrivateMessageRouter,BroadcastRouter, WebsocketRouter

app = FastAPI(debug=True)
app.include_router(PrivateMessageRouter,  prefix="/private")
app.include_router(BroadcastRouter,  prefix="/broadcast")
app.include_router(WebsocketRouter,  prefix="/ws")  # websocket router