import qrcode
import uuid
import os
from qrcode.image.pil import PilImage

def create(data: str, save_dir: str = "static/images") -> str:
    os.makedirs(save_dir, exist_ok=True)
    
    filename = f"qr_{uuid.uuid4().hex}.png"
    path = os.path.join(save_dir, filename)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(image_factory=PilImage)
    img.save(path)
    
    return path
