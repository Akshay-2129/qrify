from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from logic import create

app = FastAPI()

# Templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Home page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Generate QR
@app.post("/generate", response_class=HTMLResponse)
async def generate(request: Request, link: str = Form(...)):
    qr_path = create(link)

    # Convert path for HTML use
    qr_path_for_html = "/" + qr_path.replace("\\", "/")

    return templates.TemplateResponse(
        "result.html",
        {"request": request, "qr_path": qr_path_for_html}
    )
