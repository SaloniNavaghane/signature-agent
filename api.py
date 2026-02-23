from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
import tempfile
import os

app = FastAPI(
    title="Signature API",
    servers=[
        {
            "url": "https://signature-agent-production.up.railway.app"
        }
    ]
)

orb = cv2.ORB_create(nfeatures=2000)

GENUINE_FOLDER = "data/genuine"

def get_orb_features(image):
    image = cv2.resize(image,(400,200))
    kp, des = orb.detectAndCompute(image,None)
    return des

def match_score(des1, des2):

    if des1 is None or des2 is None:
        return 0

    bf = cv2.BFMatcher(cv2.NORM_HAMMING)

    matches = bf.knnMatch(des1,des2,k=2)

    good = []

    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append(m)

    return len(good)

@app.post("/compare")
async def compare_signature(test: UploadFile = File(...)):

    # save test image
    contents = await test.read()
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(contents)
        path = tmp.name

    test_img = cv2.imread(path,0)
    test_des = get_orb_features(test_img)

    scores = []

    # ⭐ compare with ALL genuine signatures
    for file in os.listdir(GENUINE_FOLDER):

        g_img = cv2.imread(f"{GENUINE_FOLDER}/{file}",0)
        g_des = get_orb_features(g_img)

        s = match_score(g_des,test_des)
        scores.append(s)

    avg_score = np.mean(scores)

    # ⭐ REALISTIC THRESHOLD
    if avg_score > 5:
        result = "Genuine"
    else:
        result = "Forged"

    return {
        "result": result,
        "avg_score": float(avg_score)
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)