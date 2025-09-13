import qrcode
import uuid
import os

def create(data: str, save_dir: str = "static") -> str:


    os.makedirs("static/images", exist_ok=True)
    
    filename = f"qr_{uuid.uuid4().hex}.png"
    path = os.path.join("static/images", filename)
    
    qr = qrcode.make(data)
    qr.save(path)
    
    return path
