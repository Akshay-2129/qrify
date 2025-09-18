import qrcode
import uuid
import os
from PIL import Image, ImageDraw, ImageColor

def create(data: str, save_dir: str = "static/images", fg_color="#000000", bg_color="#ffffff", logo_path: str = None) -> str:
    """
    Generates a QR code with custom colors and optional logo in the center.
    :param data: URL or text for QR code
    :param save_dir: Directory to save QR code
    :param fg_color: Foreground color (dots)
    :param bg_color: Background color
    :param logo_path: Path to logo image
    :return: path to saved QR code image
    """
    os.makedirs(save_dir, exist_ok=True)

    filename = f"qr_{uuid.uuid4().hex}.png"
    path = os.path.join(save_dir, filename)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High to allow logo in center
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fg_color, back_color=bg_color).convert('RGB')

    # Add subtle gradient (optional)
    gradient = Image.new('RGB', img.size, color=bg_color)
    draw = ImageDraw.Draw(gradient)
    width, height = img.size
    for y in range(height):
        ratio = y / height
        r1, g1, b1 = ImageColor.getrgb(bg_color)
        r2, g2, b2 = ImageColor.getrgb(fg_color)
        r = int(r1*(1-ratio) + r2*ratio)
        g = int(g1*(1-ratio) + g2*ratio)
        b = int(b1*(1-ratio) + b2*ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    img = Image.blend(gradient, img, alpha=0.5)

    # If logo is provided
    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")

        # Resize logo to 20% of QR code size
        qr_width, qr_height = img.size
        factor = 4  # logo occupies roughly 1/4 of QR
        logo_size = qr_width // factor
        logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)

        # Calculate position and paste
        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        img.paste(logo, pos, mask=logo)

    img.save(path)
    return path
