from fastapi import FastAPI
from routers import users, auth
import uvicorn
from config import config

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)

if __name__ == '__main__':
    uvicorn.run(app, host=config.settings.SERVER_HOST, port=config.settings.SERVER_PORT, log_config='log_conf.yaml')
