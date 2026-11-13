"""Plain text document extractor."""
import io


class TextExtractor:
    """Extracts text content from plain text (.txt) files."""

    @staticmethod
    def extract(file_bytes: bytes) -> dict:
        """
        Decodes bytes into a normalized string.
        Attempts UTF-8 first, then Latin-1 and CP1252 fallbacks.
        """
        encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
        text = None

        for enc in encodings:
            try:
                text = file_bytes.decode(enc)
                break
            except UnicodeDecodeError:
                continue

        if text is None:
            text = file_bytes.decode("utf-8", errors="replace")

        # Normalize line endings
        normalized_text = text.replace("\r\n", "\n").replace("\r", "\n").strip()

        return {
            "extracted_text": normalized_text,
            "page_count": 1,
            "char_count": len(normalized_text),
            "word_count": len(normalized_text.split()),
            "extraction_method": "plain_text",
        }
