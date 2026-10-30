import joblib
import pandas as pd
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from dotenv import load_dotenv
from prometheus_fastapi_instrumentator import Instrumentator
# Добавляем метрики подсчёта запросов и распределения цен
from prometheus_client import Counter, Histogram

# Загружаем переменные окружения из файла .env
load_dotenv()

app = FastAPI(title="Real Estate Price Predictor")

# Создание кастомных метрик
PREDICTION_COUNT = Counter(
    'model_prediction_total', 
    'Общее количество сделанных предсказаний'
)
PREDICTION_PRICE_HISTOGRAM = Histogram(
    'model_prediction_price_rubles', 
    'Распределение предсказанных цен',
    buckets=[1_000_000, 5_000_000, 10_000_000, 20_000_000, 50_000_000, 100_000_000]
)

# Берем путь из .env
MODEL_PATH = os.getenv("MODEL_PATH", "/app/services/models/model.pkl")

try:
    model = joblib.load(MODEL_PATH)
    print(f"Модель успешно загружена из {MODEL_PATH}")
except Exception as e:
    model = None
    print(f"Ошибка загрузки модели: {e}")

# Описываем структуру входящего запроса
class PredictionRequest(BaseModel):
    user_id: int
    features: Dict[str, Any]  # Словарь с признаками квартиры

    # Добавляем пример для Swagger
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 12345,
                "features": {
                    "total_area": 55.0,
                    "kitchen_area": 10.0,
                    "rooms": 2,
                    "floor": 5,
                    "living_area": 30.0,
                    "is_apartment": 0,
                    "build_year": 2015,
                    "floors_total": 12
                }
            }
        }

class PredictionResponse(BaseModel):
    user_id: int
    prediction: float

@app.post("/predict", response_model=PredictionResponse)
def predict_price(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Модель не загружена на сервере")
    
    try:
        # Преобразуем входящий словарь в df
        df = pd.DataFrame([request.features])
        
        # Порядок колонок задаём как при обучении
        expected_features = [
            'total_area', 'kitchen_area', 'rooms', 'floor', 
            'living_area', 'is_apartment', 'build_year', 'floors_total'
        ]
        df = df[expected_features]
        
        # Делаем предсказание
        prediction = model.predict(df)[0]

        # Обновление метрик
        PREDICTION_COUNT.inc() # +1 к счетчику запросов
        PREDICTION_PRICE_HISTOGRAM.observe(float(prediction)) # Записываем предсказанную цену
        
        return PredictionResponse(
            user_id=request.user_id,
            prediction=float(prediction)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка предсказания: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "ML Service is running. Go to /docs for API documentation."}

# Инициализация экспортера метрик Prometheus
Instrumentator().instrument(app).expose(app)