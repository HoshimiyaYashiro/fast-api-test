from fastapi import FastAPI
import uvicorn
import socketio

from models.user import User
from routers import users, auth
from config import config
from utils import jwt_helper

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


@sio.event
async def connect(sid, env):
    authorization = env.get('HTTP_AUTHORIZATION')
    credentials = jwt_helper.get_credentials_from_token(authorization.split(' ')[1])
    auth_user = User(**credentials.subject)
    await sio.save_session(sid, {'user': auth_user.email})
    print("New Client Connected to This id :" + " " + str(sid))
    await sio.emit("msg", "Welcome " + auth_user.email + " to the chat room")


@sio.on('msg')
async def client_side_receive_msg(sid, msg):
    print("Msg receive from " + str(sid) + "and msg is : ", str(msg))


@sio.event
async def disconnect(sid):
    print("Client Disconnected: " + " " + str(sid))


if __name__ == '__main__':
    uvicorn.run(app, host=config.settings.SERVER_HOST, port=config.settings.SERVER_PORT, log_config='log_conf.yaml')
