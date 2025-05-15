from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import qrcode
import io
import base64

app = FastAPI()

# Mount templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index_new.html", {"request": request})

@app.post("/generate")
async def generate_qr(data: str = Form(...)):
    try:
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Create an image from the QR Code
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert the image to base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return {"qr_code": img_str}
    except Exception as e:
        return {"error": str(e)} 