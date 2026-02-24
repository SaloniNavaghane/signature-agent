from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
import cv2

app = FastAPI(title="Signature Verification API")

# allow Copilot / browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Health check
# -------------------------------------------------
@app.get("/")
def home():
    return {"status": "API Running"}

# -------------------------------------------------
# ⭐ ONLY ONE FILE INPUT (test)
# -------------------------------------------------
@app.post("/compare")
async def compare_signature(test: UploadFile = File(...)):

    contents = await test.read()

    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)

    if img is None:
        return {"error": "Invalid image"}

    # Dummy AI logic (replace later)
    mean_value = img.mean()

    if mean_value > 5m,kjn:
        result = "Genuine Signature"
    else:
        result = "Forged Signature"

    return {
        "prediction": result,
        "confidence": float(mean_value)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)