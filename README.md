README.md
VS Code'da README.md oluştur, şunu yapıştır:
markdown# FastAPI CRUD API — Retail Customers

FastAPI + SQLModel + MySQL kullanılarak geliştirilmiş CRUD API.

## Proje Yapısı
odev5/
├── main.py
├── models.py
├── db.py
├── requirements.txt
├── .env
├── README.md
└── screenshots/


## 1. MySQL'i Başlat

```bash
docker run --rm -d \
  --name mysql \
  -e MYSQL_ROOT_PASSWORD=root123 \
  -e MYSQL_DATABASE=mlops \
  -e MYSQL_USER=mlops_user \
  -e MYSQL_PASSWORD=mlops_pass \
  -p 3306:3306 \
  mysql:8.0
```

## 2. Ortamı Kur ve Uygulamayı Çalıştır

```bash
uv venv .venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Swagger UI: http://localhost:8000/docs

## 3. Görevler ve curl Komutları

### Task 1 — İlk 10 müşteriyi ekle

```bash
curl -X 'POST' 'http://localhost:8000/customers' \
  -H 'Content-Type: application/json' \
  -d '{
  "customerFName": "Richard",
  "customerLName": "Hernandez",
  "customerEmail": "XXXXXXXXX",
  "customerPassword": "pass1234",
  "customerStreet": "6303 Heather Plaza",
  "customerCity": "Brownsville",
  "customerState": "TX",
  "customerZipcode": "78521"
}'
```

MySQL kontrolü:
```sql
SELECT customerId, customerFName, customerLName, customerPassword FROM customer;
```
→ 10 satır, customerPassword sütununda `$2b$12$...` hash'ler görünür.

### Task 2 — id=8 güncelle (Smith → Fox)

```bash
curl -X 'PUT' 'http://localhost:8000/customers/8' \
  -H 'Content-Type: application/json' \
  -d '{"customerLName": "Fox"}'
```

MySQL kontrolü:
```sql
SELECT customerId, customerFName, customerLName FROM customer WHERE customerId = 8;
```
→ customerLName = Fox görünür.

### Task 3 — id=4 sil (Mary Jones)

```bash
curl -X 'DELETE' 'http://localhost:8000/customers/4'
```

MySQL kontrolü:
```sql
SELECT customerId, customerFName, customerLName FROM customer;
```
→ id=4 satırı yoktur.

### Task 4 — Caguas'tan 3 müşteri listele

```bash
curl -X 'GET' 'http://localhost:8000/customers?city=Caguas&limit=3' \
  -H 'accept: application/json'
```

→ 3 müşteri döner, hepsi customerCity: "Caguas".

### Task 5 — Şifre hash kontrolü

Kayıt sırasında şifre hiçbir zaman düz metin olarak saklanmaz.
`passlib[bcrypt]` kullanılarak hash'lenir.
MySQL'de `customerPassword` sütununda `$2b$12$...` formatında hash görünür.

## 4. Teknik Detaylar

- **Framework**: FastAPI + Uvicorn
- **DB**: SQLModel + MySQL 8.0
- **Password Hashing**: passlib + bcrypt
- **Config**: .env dosyasından okunur, kaynak kodda şifre yoktur
- **Python**: 3.12