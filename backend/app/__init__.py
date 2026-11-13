import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

from .extractors import DocumentExtractorFactory

# Load environment variables
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    # Default configurations
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-docuease-secret-key"),
        TESSERACT_CMD=os.getenv("TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
        GEMINI_API_KEY=os.getenv("GEMINI_API_KEY", ""),
        MAX_CONTENT_LENGTH=10 * 1024 * 1024,  # 10 MB limit
    )

    if test_config:
        app.config.update(test_config)

    # Enable CORS for frontend interactions
    cors_origin = os.getenv("CORS_ORIGIN", "*")
    CORS(app, resources={r"/api/*": {"origins": cors_origin}})

    # Root route
    @app.route("/")
    def index():
        return jsonify({
            "name": "DocuEase API",
            "version": "1.0.0",
            "description": "AI-Powered Document Simplification System API",
            "endpoints": {
                "health": "/api/health",
                "extract": "/api/extract"
            }
        }), 200

    # Backend Health Check Endpoint
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "success",
            "message": "DocuEase backend is running"
        }), 200

    # Document Extraction Endpoint
    @app.route("/api/extract", methods=["POST"])
    def extract_document():
        if "file" not in request.files:
            return jsonify({
                "status": "error",
                "message": "No file part in the request. Please upload a file with key 'file'."
            }), 400

        file = request.files["file"]
        if not file or not file.filename or not file.filename.strip():
            return jsonify({
                "status": "error",
                "message": "No file selected for upload."
            }), 400

        try:
            file_bytes = file.read()
            result = DocumentExtractorFactory.process_file(file.filename, file_bytes)
            return jsonify(result), 200
        except ValueError as ve:
            return jsonify({
                "status": "error",
                "message": str(ve)
            }), 400
        except Exception as ex:
            return jsonify({
                "status": "error",
                "message": f"Unexpected error while extracting document: {str(ex)}"
            }), 500

    return app
