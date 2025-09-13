import qrcode
import uuid
import os

def create(data: str, save_dir: str = "static/images") -> str:
    # Ensure directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # Generate a unique filename
    filename = f"qr_{uuid.uuid4().hex}.png"
    path = os.path.join(save_dir, filename)
    
    # Explicitly create a QRCode object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image and save it
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(path)
    
    return path
