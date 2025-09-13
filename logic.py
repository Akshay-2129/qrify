import qrcode
import uuid
import os
from qrcode.image.pil import PilImage  # <-- use PIL backend

def create(data: str, save_dir: str = "static") -> str:
    os.makedirs("static/images", exist_ok=True)
    
    filename = f"qr_{uuid.uuid4().hex}.png"
    path = os.path.join("static/images", filename)
    
    # Create QR code with PIL backend
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(image_factory=PilImage)
    img.save(path)  # now this works fine
    
    return path
