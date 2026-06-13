import pandas as pd
import joblib
import os
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Veriyi indirelim ve kaydedlim
df = pd.read_csv("https://raw.githubusercontent.com/erkansirin78/datasets/refs/heads/master/Churn_Modelling.csv")
print("Dataset shape:", df.shape)
print(df.head())


#Feauterlar ve target değişkenlerinin ayrılması 
features = ["CreditScore", "Geography", "Gender", "Age", "Tenure",
            "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary"]
target = "Exited"

X = df[features]
y = df[target]

# 3. Train/test split adımları
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Kategorik kolonlar: Geography, Gender
# Sayısal kolonlar: geri kalanlar

categorical_features = ["Geography", "Gender"]
numerical_features = ["CreditScore", "Age", "Tenure", "Balance",
                      "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary"]

preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), numerical_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
])

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

# 5. Modeli eğitim kısmı
pipeline.fit(X_train, y_train)

#Model validasyon kısmı 
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

#Modeli kaydedlim 
os.makedirs("saved_models", exist_ok=True)
joblib.dump(pipeline, "saved_models/churn_pipeline.pkl")
print("Model saved to saved_models/churn_pipeline.pkl")