"""Document extraction factory and coordinator."""
import os
from werkzeug.utils import secure_filename
from .text_extractor import TextExtractor
from .image_extractor import ImageExtractor
from .pdf_extractor import PDFExtractor

ALLOWED_EXTENSIONS = {
    "pdf": "application/pdf",
    "txt": "text/plain",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class DocumentExtractorFactory:
    """Dispatches extraction requests to appropriate format extractors."""

    @classmethod
    def get_file_extension(cls, filename: str) -> str:
        """Extracts and lowercases the file extension without dot."""
        if "." not in filename:
            return ""
        return filename.rsplit(".", 1)[1].lower()

    @classmethod
    def is_allowed_file(cls, filename: str) -> bool:
        """Validates if file has an authorized extension."""
        ext = cls.get_file_extension(filename)
        return ext in ALLOWED_EXTENSIONS

    @classmethod
    def process_file(cls, filename: str, file_bytes: bytes) -> dict:
        """
        Validates and routes the file bytes to the appropriate extractor.
        """
        if not filename or not filename.strip():
            raise ValueError("Filename cannot be empty")

        clean_filename = secure_filename(filename) or "document"
        ext = cls.get_file_extension(clean_filename)

        if not ext or ext not in ALLOWED_EXTENSIONS:
            allowed_list = ", ".join(f".{e}" for e in sorted(ALLOWED_EXTENSIONS.keys()))
            raise ValueError(f"Unsupported file format '.{ext}'. Supported formats are: {allowed_list}")

        if len(file_bytes) == 0:
            raise ValueError("Uploaded file is empty (0 bytes)")

        if len(file_bytes) > MAX_FILE_SIZE:
            max_mb = MAX_FILE_SIZE / (1024 * 1024)
            raise ValueError(f"File size exceeds maximum allowed limit of {max_mb:.0f} MB")

        # Route by extension
        if ext == "txt":
            result = TextExtractor.extract(file_bytes)
        elif ext in ("png", "jpg", "jpeg"):
            result = ImageExtractor.extract(file_bytes)
        elif ext == "pdf":
            result = PDFExtractor.extract(file_bytes)
        else:
            raise ValueError(f"Extractor for format '.{ext}' is not registered")

        # Enrich with common metadata
        result["filename"] = clean_filename
        result["file_extension"] = ext
        result["file_size_bytes"] = len(file_bytes)
        result["file_size_formatted"] = (
            f"{len(file_bytes) / 1024:.1f} KB"
            if len(file_bytes) < 1024 * 1024
            else f"{len(file_bytes) / (1024 * 1024):.2f} MB"
        )
        result["status"] = "success"

        return result
