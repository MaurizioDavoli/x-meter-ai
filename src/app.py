from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from src.routers.transcriptor import router as websocket_router


app = FastAPI()
templates = Jinja2Templates(directory="src/views")

app.include_router(websocket_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def get_audio(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/zig")
async def zig():
    return {"zag"}
