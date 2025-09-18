import qrcode
import uuid
import os
from qrcode.image.pil import PilImage

def create(data: str, save_dir: str = "static/images") -> str:
    # Make sure the directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Unique filename
    filename = f"qr_{uuid.uuid4().hex}.png"
    path = os.path.join(save_dir, filename)

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Save as PIL image
    img = qr.make_image(image_factory=PilImage, fill_color="black", back_color="white")
    img.save(path)

    return path
