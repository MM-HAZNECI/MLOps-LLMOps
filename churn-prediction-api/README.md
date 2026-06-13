# Churn Prediction API

Scikit-learn ML Pipeline + FastAPI + Docker ile müşteri churn tahminleme projesi

## Tech Stack
- FastAPI
- Scikit-learn (Pipeline)
- Docker
- joblib

## Model
- Dataset: Churn Modelling (10,000 satır)
- Algorithm: RandomForestClassifier
- Accuracy: %86.80
- Target: Exited (0 = kalıyor, 1 = ayrılıyor)
- Features: CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary

## Kurulum

### 1. Modeli eğit
```bash
python train_model.py
```

### 2. Docker image oluştur
```bash
docker image build -t churn-prediction:1.0 .
```

### 3. Container başlat
```bash
docker run -d --name churn-api -p 8502:8502 churn-prediction:1.0
```

### 4. Swagger UI

## API Endpoints

### GET /
```bash
curl http://localhost:8502/
```

### POST /predict
```bash
curl -X POST 'http://localhost:8502/predict' \
  -H 'Content-Type: application/json' \
  -d '{
  "CreditScore": 619,
  "Geography": "France",
  "Gender": "Female",
  "Age": 42,
  "Tenure": 2,
  "Balance": 0,
  "NumOfProducts": 1,
  "HasCrCard": 1,
  "IsActiveMember": 1,
  "EstimatedSalary": 101348.88
}'
```

### Örnek Alınan Yanıt
```json
{
  "prediction": 0,
  "result": "Customer will STAY",
  "probability": {
    "stay": 0.79,
    "exit": 0.21
  }
}
```

## Container Yönetimi

### Container durumu
```bash
docker ps
```

### Container durdur
```bash
docker stop churn-api
```

### Container sil
```bash
docker rm churn-api
```

### Image sil
```bash
docker image rm churn-prediction:1.0
```