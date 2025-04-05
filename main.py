import os
import requests
import time
import fitz  # PyMuPDF - pdf reader

API_KEY = os.environ.get("CHAM_AI_API_KEY")
BASE_URL = "https://client.camb.ai/apis"
HEADERS = {"headers": {"x-api-key": API_KEY}}

doc = fitz.open('pdf.pdf')
text = "\n".join(page.get_text() for page in doc)
doc.close()


tts_payload = {
    "text": text,
    "voice_id": 20303,  # Voice ID from already extracted list of voices
    "language": 1,  # English
    "age": 30,
    "gender": 1,  # Male
}

res = requests.post(f"{BASE_URL}/tts", json=tts_payload, **HEADERS)
task_id = res.json()["task_id"]
print(f"Task ID: {task_id}")

while True:
    res = requests.get(f"{BASE_URL}/tts/{task_id}", **HEADERS)
    status = res.json()["status"]
    print(f"Polling: {status}")
    time.sleep(1.5)
    if status == "SUCCESS":
        run_id = res.json()["run_id"]
        break

print(f"Run ID: {run_id}")
res = requests.get(f"{BASE_URL}/tts-result/{run_id}", **HEADERS, stream=True)
with open("tts_output.wav", "wb") as f:
    for chunk in res.iter_content(chunk_size=1024):
        f.write(chunk)
print("Done!")