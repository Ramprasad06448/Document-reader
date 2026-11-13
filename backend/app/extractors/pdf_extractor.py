"""PDF extractor supporting native digital text and OCR fallback."""
import io
import pymupdf
from PIL import Image
from .image_extractor import ImageExtractor


class PDFExtractor:
    """Extracts text from digital and scanned PDFs using PyMuPDF and Tesseract OCR."""

    MIN_TEXT_PER_PAGE_THRESHOLD = 30  # Chars threshold to detect scanned page

    @classmethod
    def extract(cls, file_bytes: bytes) -> dict:
        """
        Parses a PDF document from bytes.
        Uses native text extraction, falling back to OCR on individual pages when necessary.
        """
        try:
            doc = pymupdf.open(stream=file_bytes, filetype="pdf")
        except Exception as e:
            raise ValueError(f"Failed to parse PDF document: {str(e)}")

        page_count = len(doc)
        if page_count == 0:
            doc.close()
            return {
                "extracted_text": "",
                "page_count": 0,
                "char_count": 0,
                "word_count": 0,
                "extraction_method": "empty_pdf",
            }

        extracted_pages = []
        digital_pages = 0
        ocr_pages = 0

        for page_idx in range(page_count):
            page = doc[page_idx]
            page_text = page.get_text("text").strip()

            # If selectable digital text is sufficient, use it
            if len(page_text) >= cls.MIN_TEXT_PER_PAGE_THRESHOLD:
                extracted_pages.append(page_text)
                digital_pages += 1
            else:
                # Scanned or image-based page: render to pixmap and run OCR
                try:
                    pix = page.get_pixmap(dpi=200)
                    img_data = pix.tobytes("png")
                    img = Image.open(io.BytesIO(img_data))
                    ocr_text = ImageExtractor.extract_from_image(img)
                    if ocr_text:
                        extracted_pages.append(ocr_text)
                    elif page_text:
                        extracted_pages.append(page_text)
                    else:
                        extracted_pages.append("")
                    ocr_pages += 1
                except Exception:
                    # Fallback to whatever digital text was there
                    extracted_pages.append(page_text)
                    digital_pages += 1

        doc.close()

        # Combine text across pages
        if page_count > 1:
            formatted_text = "\n\n".join(
                f"--- Page {i + 1} ---\n{text}" if text else f"--- Page {i + 1} --- (Empty)"
                for i, text in enumerate(extracted_pages)
            )
        else:
            formatted_text = extracted_pages[0] if extracted_pages else ""

        # Normalize line endings
        normalized_text = formatted_text.replace("\r\n", "\n").replace("\r", "\n").strip()

        # Categorize extraction method
        if ocr_pages > 0 and digital_pages > 0:
            method = "hybrid_pdf_ocr"
        elif ocr_pages > 0:
            method = "ocr_pdf"
        else:
            method = "digital_pdf"

        return {
            "extracted_text": normalized_text,
            "page_count": page_count,
            "digital_pages": digital_pages,
            "ocr_pages": ocr_pages,
            "char_count": len(normalized_text),
            "word_count": len(normalized_text.split()),
            "extraction_method": method,
        }
