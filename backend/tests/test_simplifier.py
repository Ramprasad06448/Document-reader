import pytest
import io
import sys
import os

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.services.simplifier import SimplifierService


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_simplify_missing_payload(client):
    """Calling POST /api/simplify with no payload returns HTTP 400."""
    response = client.post("/api/simplify", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "No text provided" in data["message"]


def test_simplify_empty_text(client):
    """Calling POST /api/simplify with empty string returns HTTP 400."""
    response = client.post("/api/simplify", json={"text": "   "})
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"


def test_simplify_json_text_success(client):
    """Calling POST /api/simplify with complex legal text returns structured plain language."""
    sample_legal_text = (
        "In the event that the Tenant fails to pay rent prior to the fifth day of the month, "
        "the Landlord shall have the right to terminate the agreement. "
        "The Tenant agrees to indemnify and hold harmless the Landlord from all liabilities, "
        "and any dispute shall be resolved through binding arbitration."
    )
    response = client.post("/api/simplify", json={"text": sample_legal_text})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "simplified_text" in data
    assert "summary" in data
    assert "terminology" in data
    assert "metrics" in data
    assert "ai_provider" in data

    # Verify phrase simplification ("In the event that" -> "if", "prior to" -> "before")
    simplified = data["simplified_text"].lower()
    assert "if the tenant" in simplified or "before" in simplified

    # Verify terminology detection
    terms = [item["term"].lower() for item in data["terminology"]]
    assert "indemnify" in terms or "arbitration" in terms

    # Verify metrics
    metrics = data["metrics"]
    assert metrics["original_words"] > 0
    assert metrics["simplified_words"] > 0


def test_simplify_file_upload(client):
    """Direct file upload to /api/simplify extracts and simplifies in one step."""
    content = b"The company shall not be held liable in the case of force majeure or acts of God."
    data = {
        "file": (io.BytesIO(content), "policy.txt")
    }
    response = client.post("/api/simplify", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    res_data = response.get_json()
    assert res_data["status"] == "success"
    assert "document_metadata" in res_data
    assert res_data["document_metadata"]["filename"] == "policy.txt"
    assert len(res_data["terminology"]) > 0
    assert any(t["term"].lower() == "force majeure" for t in res_data["terminology"])


def test_rule_based_fallback_service():
    """Direct unit test on the rule-based simplification engine."""
    dense_text = (
        "Heretofore, the parties utilized multiple covenants. "
        "Notwithstanding anything to the contrary, liquidated damages shall apply upon default."
    )
    result = SimplifierService.rule_based_simplify(dense_text)
    assert "summary" in result
    assert "simplified_text" in result
    assert "terminology" in result
    assert len(result["terminology"]) >= 1

    # Check terms detected
    term_names = [t["term"].lower() for t in result["terminology"]]
    assert any(t in term_names for t in ["liquidated damages", "default", "covenant", "heretofore"])
