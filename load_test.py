import requests
import time
import random

URL = "http://localhost:8000/predict"

def generate_random_flat():
    return {
        "user_id": random.randint(1, 10000),
        "features": {
            "total_area": round(random.uniform(20.0, 150.0), 1),
            "kitchen_area": round(random.uniform(5.0, 25.0), 1),
            "rooms": random.randint(1, 5),
            "floor": random.randint(1, 25),
            "living_area": round(random.uniform(10.0, 80.0), 1),
            "is_apartment": random.choice([0, 1]),
            "build_year": random.randint(1950, 2023),
            "floors_total": random.randint(5, 30)
        }
    }

print("Начинаем симуляцию нагрузки")
while True:
    try:
        payload = generate_random_flat()
        response = requests.post(URL, json=payload)
        if response.status_code == 200:
            pred = response.json()["prediction"]
            print(f"Успешно: user_id={payload['user_id']}, цена={pred:.2f} руб.")
        else:
            print(f"Ошибка: {response.status_code}")
    except Exception as e:
        print(f"Сервис недоступен: {e}")
    
    time.sleep(0.5) # Пауза между запросами, чтобы не перегружать систему