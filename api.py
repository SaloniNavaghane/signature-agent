from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
import cv2

app = FastAPI(title="Signature Verification API")

# ✅ Allow Copilot / Browser / Streamlit calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# 🔥 HEALTH CHECK (Important for Railway)
# ----------------------------------------------------
@app.get("/")
def home():
    return {"status": "Signature API Running"}

# ----------------------------------------------------
# ⭐ MAIN ENDPOINT FOR COPILOT + STREAMLIT
# Accept BOTH:
#   file = Streamlit
#   test = Copilot Studio connector
# ----------------------------------------------------
@app.post("/compare")
async def compare_signature(
    request: Request,
    file: UploadFile = File(None),
    test: UploadFile = File(None)
):
    try:
        # ✅ Accept either input name
        uploaded = file if file is not None else test

        if uploaded is None:
            return {"error": "No file received"}

        # read image bytes
        contents = await uploaded.read()

        # ------------------------------------------------
        # 🔥 SIMPLE DEMO PREDICTION LOGIC
        # Replace this with your ML model later
        # ------------------------------------------------
        np_arr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)

        if img is None:
            return {"error": "Invalid image"}

        # Dummy logic just for demo
        mean_value = img.mean()

        if mean_value > 5:
            result = "Genuine Signature"
        else:
            result = "Forged Signature"

        return {
            "status": "success",
            "prediction": result,
            "confidence": float(mean_value)
        }

    except Exception as e:
        return {"error": str(e)}

# ----------------------------------------------------
# ⭐ LOCAL RUN
# ----------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)