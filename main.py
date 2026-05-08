from fastapi import FastAPI, Form
import requests
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

SNOW_URL = os.getenv("SNOW_URL")
SNOW_USER = os.getenv("SNOW_USER")
SNOW_PASS = os.getenv("SNOW_PASS")

@app.post("/slack/command")
async def create_ticket(text: str = Form(...)):

    response = requests.post(
        f"{SNOW_URL}/api/now/table/incident",
        auth=(SNOW_USER, SNOW_PASS),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        json={
            "short_description": text,
            "category": "software"
        }
    )

    print("Status:", response.status_code)
    print("Response:", response.text)

    if response.status_code == 201:

        data = response.json()

        return {
            "response_type": "in_channel",
            "text": f"✅ Ticket {data['result']['number']} created"
        }

    else:
        return {
            "text": f"❌ Failed: {response.text}"
        }
