
from pathlib import Path
import joblib

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

app = FastAPI(title="Language Detection API")

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")

model = joblib.load(MODEL_DIR / "language_model.pkl")
cv = joblib.load(MODEL_DIR / "count_vectorizer.pkl")


class PredictionRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict_language(payload: PredictionRequest):
    text = payload.text.strip()

    if not text:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail="Please enter some text."
        )

    text_vector = cv.transform([text])

    if text_vector.nnz == 0:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=422,
            detail="No recognized features found. Try another sentence."
        )

    prediction = model.predict(text_vector)[0]

    return {
        "input_text": text,
        "predicted_language": str(prediction)
    }
