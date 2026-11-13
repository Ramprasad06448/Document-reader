import threading
import time
import urllib.request
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import create_app

app = create_app()
server = threading.Thread(
    target=lambda: app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False),
    daemon=True,
)
server.start()
time.sleep(1.5)

sample_clause = (
    "In the event that either party breaches this agreement, the non-breaching party "
    "shall have the right to terminate the contract and seek liquidated damages. "
    "Notwithstanding anything to the contrary, the parties agree to binding arbitration."
)

payload = json.dumps({"text": sample_clause, "level": "plain_language"}).encode("utf-8")
req = urllib.request.Request(
    "http://127.0.0.1:5000/api/simplify",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST",
)

with urllib.request.urlopen(req) as resp:
    print("LIVE_STATUS:", resp.status)
    data = json.loads(resp.read().decode("utf-8"))
    print("STATUS_FIELD:", data.get("status"))
    print("SUMMARY:", data.get("summary"))
    print("SIMPLIFIED_SAMPLE:", data.get("simplified_text")[:80])
    print("TERMS_FOUND:", [t["term"] for t in data.get("terminology", [])])
    print("METRICS:", data.get("metrics"))
