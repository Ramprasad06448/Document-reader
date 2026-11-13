import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment configuration if present
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

    # Root route for basic verification
    @app.route("/")
    def index():
        return jsonify({
            "name": "DocuEase API",
            "version": "1.0.0",
            "description": "AI-Powered Document Simplification System API",
            "endpoints": {
                "health": "/api/health"
            }
        }), 200

    # Backend Health Check Endpoint
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "success",
            "message": "DocuEase backend is running"
        }), 200

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "0").lower() in ("true", "1", "yes")
    app.run(host="127.0.0.1", port=port, debug=debug, use_reloader=False)
