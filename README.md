# DocuEase – AI-Powered Document Simplification System

DocuEase is an intelligent web application designed to help ordinary citizens, students, patients, and professionals understand complex, dense documents (contracts, medical records, financial disclosures, and academic papers) by converting technical jargon into clear, plain language while strictly preserving original meaning.

---

## 📌 Project Overview
- **Phase 0 (Completed)**: System architecture, technical documentation (PRD & Architecture with Mermaid diagrams), backend health API, and responsive React landing page with document upload placeholder.
- **Phase 1 (Upcoming)**: Multi-format document ingestion (PDF, TXT, PNG, JPG) using PyMuPDF and Tesseract OCR.
- **Phase 2 (Upcoming)**: Gemini AI plain-language simplification, dual-pane comparative viewer, and automated terminology glossary.

---

## 🏗️ Technology Stack

| Component | Technology | Version / Notes |
| :--- | :--- | :--- |
| **Frontend** | React, Vite, JavaScript, Axios | React 19, Vite 6, clean responsive UI |
| **Backend** | Python, Flask, Flask-CORS | Flask 3.1, RESTful API |
| **Testing** | Pytest | Automated API test suite |
| **OCR Engine** | Tesseract OCR | Installed binary: `C:\Program Files\Tesseract-OCR\tesseract.exe` (v5.5.3) |
| **PDF Extraction**| PyMuPDF (`fitz`) | Digital PDF text extraction |
| **AI Engine** | Google Gemini API | Structured plain-language generation (Phase 2) |

---

## 📁 Repository Structure

```text
docuease/
├── frontend/                   # React + Vite frontend application
│   ├── src/
│   │   ├── components/         # Modular UI components (Navbar, UploadPlaceholder, Features)
│   │   ├── pages/              # View pages
│   │   ├── services/           # Axios API services (health check, backend integration)
│   │   ├── App.jsx             # Main application orchestrator
│   │   ├── main.jsx            # Entry point
│   │   └── index.css           # Modern design tokens & layout
│   ├── index.html              # HTML shell
│   ├── package.json            # Node dependencies & scripts
│   └── vite.config.js          # Vite config with backend API proxy
│
├── backend/                    # Python Flask backend
│   ├── app/                    # Future extraction & simplification modules
│   ├── tests/                  # Pytest test suite
│   │   └── test_health.py      # Health endpoint unit & integration tests
│   ├── app.py                  # Flask application entry point & /api/health
│   ├── requirements.txt        # Python package dependencies
│   └── .env.example            # Environment configuration template
│
├── docs/                       # Architecture & Product Documentation
│   ├── PRD.md                  # Comprehensive Product Requirements Document
│   └── ARCHITECTURE.md         # Full System Architecture & Mermaid Diagrams
│
├── .gitignore                  # Git ignore rules for Python, Node, and secrets
└── README.md                   # Project documentation & execution guide
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python**: 3.10 or later (tested on Python 3.13)
- **Node.js**: v18 or later (tested on Node v26) & npm
- **Tesseract OCR**: Installed at `C:\Program Files\Tesseract-OCR\tesseract.exe`
  *(Cloned repository reference preserved at `D:\Vibe\tesseract`)*

---

### 2. Backend Setup & Execution

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your environment variables:
   ```bash
   copy .env.example .env
   ```

5. Run the backend server:
   ```bash
   python app.py
   ```
   *The Flask API starts at `http://127.0.0.1:5000`.*

6. Verify the health check:
   ```bash
   curl http://127.0.0.1:5000/api/health
   ```
   **Expected Response:**
   ```json
   {
     "status": "success",
     "message": "DocuEase backend is running"
   }
   ```

7. Run automated backend tests:
   ```bash
   pytest tests/
   ```

---

### 3. Frontend Setup & Execution

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install npm dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The frontend will launch at `http://localhost:5173`.*

4. Build for production:
   ```bash
   npm run build
   ```

---

## 🔒 Security & Privacy Notice
- Never commit `.env` or sensitive API keys.
- All file handling in DocuEase is designed for ephemeral processing with no persistent storage of sensitive user documents without explicit permission.
