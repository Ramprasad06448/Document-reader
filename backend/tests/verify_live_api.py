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

boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
body_parts = [
    f"--{boundary}".encode("utf-8"),
    b'Content-Disposition: form-data; name="file"; filename="agreement.txt"',
    b"Content-Type: text/plain",
    b"",
    b"Section 4.1: Indemnification and Limitation of Liability clause.",
    f"--{boundary}--".encode("utf-8"),
    b"",
]
body = b"\r\n".join(body_parts)

req = urllib.request.Request(
    "http://127.0.0.1:5000/api/extract",
    data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
)

with urllib.request.urlopen(req) as resp:
    print("LIVE_STATUS:", resp.status)
    data = json.loads(resp.read().decode("utf-8"))
    print("LIVE_EXTRACTED_TEXT:", data.get("extracted_text"))
    print("LIVE_METHOD:", data.get("extraction_method"))
    print("LIVE_CHAR_COUNT:", data.get("char_count"))
