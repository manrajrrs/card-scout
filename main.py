from fastapi import FastAPI
from fastapi import UploadFile
from identify import identify_card

app = FastAPI()

@app.get("/health")

def health():
    return {"status": "ok"}

@app.post("/identify")

async def identify(file: UploadFile):
    b = await file.read()
    return identify_card(b)