import pytest
import io
import sys
import os
from PIL import Image, ImageDraw
import pymupdf

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_missing_file_upload(client):
    """Uploading without a 'file' field returns HTTP 400."""
    response = client.post("/api/extract", data={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "No file part" in data["message"]


def test_empty_filename_upload(client):
    """Uploading with an empty filename returns HTTP 400."""
    data = {"file": (io.BytesIO(b"content"), "")}
    response = client.post("/api/extract", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    res_data = response.get_json()
    assert res_data["status"] == "error"


def test_unsupported_file_extension(client):
    """Uploading an unsupported file format (.exe, .zip) returns HTTP 400."""
    data = {"file": (io.BytesIO(b"binary data"), "test.exe")}
    response = client.post("/api/extract", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    res_data = response.get_json()
    assert res_data["status"] == "error"
    assert "Unsupported file format" in res_data["message"]


def test_empty_file_bytes(client):
    """Uploading an empty file (0 bytes) returns HTTP 400."""
    data = {"file": (io.BytesIO(b""), "empty.txt")}
    response = client.post("/api/extract", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    res_data = response.get_json()
    assert res_data["status"] == "error"
    assert "empty" in res_data["message"].lower()


def test_plain_text_extraction(client):
    """Test extracting text from a UTF-8 .txt document."""
    sample_text = "DocuEase simplifies complex legal, medical, and technical documents."
    data = {"file": (io.BytesIO(sample_text.encode("utf-8")), "sample.txt")}
    response = client.post("/api/extract", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    res_data = response.get_json()
    assert res_data["status"] == "success"
    assert res_data["file_extension"] == "txt"
    assert res_data["extraction_method"] == "plain_text"
    assert sample_text in res_data["extracted_text"]
    assert res_data["char_count"] == len(sample_text)
    assert res_data["word_count"] == len(sample_text.split())


def test_image_ocr_extraction(client):
    """Test extracting text from an image (.png) via Tesseract OCR."""
    # Create an in-memory test image with legible text
    img = Image.new("RGB", (400, 100), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((20, 35), "DocuEase Tesseract Verification", fill=(0, 0, 0))

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    data = {"file": (img_bytes, "ocr_test.png")}
    response = client.post("/api/extract", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    res_data = response.get_json()
    assert res_data["status"] == "success"
    assert res_data["file_extension"] == "png"
    assert res_data["extraction_method"] == "ocr_image"
    assert "DocuEase" in res_data["extracted_text"]
    assert "Tesseract" in res_data["extracted_text"]


def test_pdf_extraction(client):
    """Test extracting digital text from a PDF document using PyMuPDF."""
    doc = pymupdf.open()
    page = doc.new_page()
    page_text = "Standard Operating Procedure for Document Analysis and Text Extraction."
    page.insert_text((50, 72), page_text)

    pdf_bytes = io.BytesIO(doc.tobytes())
    doc.close()

    data = {"file": (pdf_bytes, "manual.pdf")}
    response = client.post("/api/extract", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    res_data = response.get_json()
    assert res_data["status"] == "success"
    assert res_data["file_extension"] == "pdf"
    assert res_data["page_count"] == 1
    assert "Standard Operating Procedure" in res_data["extracted_text"]
    assert res_data["extraction_method"] == "digital_pdf"
