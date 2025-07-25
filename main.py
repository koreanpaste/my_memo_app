from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from database import Base,engine
from controllers import router
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware,secret_key="your-secret-key")
templates = Jinja2Templates(directory="templates")

app.include_router(router)

Base.metadata.create_all(bind=engine)


