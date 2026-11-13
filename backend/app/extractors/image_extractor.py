"""Image OCR extractor using Tesseract OCR and Pillow."""
import os
import io
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract


def get_tesseract_cmd() -> str:
    """Resolves the Tesseract binary path."""
    env_path = os.getenv("TESSERACT_CMD")
    if env_path and os.path.isfile(env_path):
        return env_path
    
    default_win_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.isfile(default_win_path):
        return default_win_path

    # Fallback to PATH
    return "tesseract"


# Configure pytesseract binary
pytesseract.pytesseract.tesseract_cmd = get_tesseract_cmd()


class ImageExtractor:
    """Performs Optical Character Recognition on PNG/JPG images."""

    @staticmethod
    def preprocess_image(image: Image.Image) -> Image.Image:
        """Applies basic contrast enhancement and grayscale conversion."""
        # Convert RGBA / P to RGB
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Grayscale
        gray = image.convert("L")

        # Contrast enhancement
        enhancer = ImageEnhance.Contrast(gray)
        enhanced = enhancer.enhance(1.8)

        return enhanced

    @classmethod
    def extract_from_image(cls, pil_image: Image.Image) -> str:
        """Runs pytesseract OCR on a PIL Image."""
        # Try raw image first
        text = pytesseract.image_to_string(pil_image)
        if not text or len(text.strip()) < 5:
            # Try preprocessed image
            processed = cls.preprocess_image(pil_image)
            text = pytesseract.image_to_string(processed)
        return text.strip()

    @classmethod
    def extract(cls, file_bytes: bytes) -> dict:
        """
        Loads image from bytes and extracts textual content via OCR.
        """
        try:
            image = Image.open(io.BytesIO(file_bytes))
        except Exception as e:
            raise ValueError(f"Invalid or corrupted image file: {str(e)}")

        raw_text = cls.extract_from_image(image)
        normalized_text = raw_text.replace("\r\n", "\n").replace("\r", "\n").strip()

        return {
            "extracted_text": normalized_text,
            "page_count": 1,
            "char_count": len(normalized_text),
            "word_count": len(normalized_text.split()),
            "extraction_method": "ocr_image",
            "image_size": f"{image.width}x{image.height}",
            "image_format": image.format or "UNKNOWN",
        }
