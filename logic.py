import qrcode
import uuid
import os
from PIL import Image, ImageDraw, ImageColor

def create(data: str,
           save_dir: str = "static/images",
           fg_color: str = "#000000",
           bg_color: str = "#ffffff",
           logo_path: str = None) -> str:
    """
    Generates a high-quality QR code with optional subtle gradient and center logo.
    Gradient is applied lightly to maintain scannability.
    """

    os.makedirs(save_dir, exist_ok=True)
    filename = f"qr_{uuid.uuid4().hex}.png"
    path = os.path.join(save_dir, filename)

    # Step 1: Create basic QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High: allows logo
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fg_color, back_color=bg_color).convert('RGB')

    # Step 2: Apply subtle vertical gradient
    width, height = img.size
    gradient = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(gradient)
    r1, g1, b1 = ImageColor.getrgb(bg_color)
    r2, g2, b2 = ImageColor.getrgb(fg_color)
    for y in range(height):
        ratio = y / height
        # Apply only 30% intensity for gradient to keep QR readable
        r = int(r1*(1-ratio*0.3) + r2*(ratio*0.3))
        g = int(g1*(1-ratio*0.3) + g2*(ratio*0.3))
        b = int(b1*(1-ratio*0.3) + b2*(ratio*0.3))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    img = Image.blend(img, gradient, alpha=0.3)  # subtle blend

    # Step 3: Add logo (if exists)
    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        qr_width, qr_height = img.size
        logo_size = qr_width // 4  # logo occupies 25%
        logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)

        # Create a white circle behind logo for readability
        mask_bg = Image.new("RGBA", (logo_size, logo_size), (255, 255, 255, 255))
        draw_bg = ImageDraw.Draw(mask_bg)
        draw_bg.ellipse((0, 0, logo_size, logo_size), fill=(255, 255, 255, 230))
        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

        img.paste(mask_bg, pos, mask_bg)
        img.paste(logo, pos, mask=logo)

    # Step 4: Save final image
    img.save(path)
    return path
