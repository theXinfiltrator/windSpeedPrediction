from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import joblib
import warnings

warnings.filterwarnings("ignore")

app = FastAPI()

regressor = joblib.load("app/regressor.joblib")

templates = Jinja2Templates(directory="app/static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submitform", response_class=HTMLResponse)
async def predict(request: Request, LAT: float = Form(...), LON: float = Form(...), YEAR: float = Form(...), DOY: float = Form(...), T2M: float = Form(...), TS: float = Form(...), QV2M: float = Form(...), RH2M: float = Form(...), PRECTOTCORR: float = Form(...), PS: float = Form(...), WS10M: float = Form(...), WD10M: float = Form(...), WD50M: float = Form(...)):
    prediction = regressor.predict([[LAT, LON, YEAR, DOY, T2M, TS, QV2M, RH2M, PRECTOTCORR, PS, WS10M, WD10M, WD50M]])
    rounded_prediction = round(prediction[0], 2)
    return templates.TemplateResponse("index.html", {"request": request, "prediction": rounded_prediction})
