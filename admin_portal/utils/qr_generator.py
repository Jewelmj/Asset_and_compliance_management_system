"""
QR code generation utilities.
"""
import qrcode
from io import BytesIO
from PIL import Image
from admin_portal.config import config


def generate_qr_code(data: str) -> Image:
    """
    Generate QR code image from data string.
    
    Args:
        data: String data to encode in QR code (typically asset ID)
    
    Returns:
        PIL Image object containing the QR code
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=config.QR_CODE_SIZE,
        border=config.QR_CODE_BORDER,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    return img


def qr_code_to_bytes(img: Image) -> bytes:
    """
    Convert PIL Image to bytes for download.
    
    Args:
        img: PIL Image object
    
    Returns:
        Bytes representation of the image
    """
    buf = BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()
