from fastapi import FastAPI
import uvicorn
import socketio
from routers import users, auth
from config import config

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
sio.instrument(auth={
    'type': 'basic',
    'username': 'admin',
    'password': 'admin'
})
socket_app = socketio.ASGIApp(sio)
app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.mount("/", socket_app)


@sio.on("connect")
async def connect(sid, env):
    print("New Client Connected to This id :"+" "+str(sid))
    await sio.emit("msg", "Welcome to the chat room")


@sio.on('msg')
async def client_side_receive_msg(sid, msg):
    print("Msg receive from " +str(sid) +"and msg is : ",str(msg))


@sio.on("disconnect")
async def disconnect(sid):
    print("Client Disconnected: "+" "+str(sid))

if __name__ == '__main__':
    uvicorn.run(app, host=config.settings.SERVER_HOST, port=config.settings.SERVER_PORT, log_config='log_conf.yaml')