import os
import time
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from models import CustomerRequest, RequestClassification, ClassificationResult
from db_operations import create_db_and_tables, save_customer_request, save_classification

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0)
structured_llm = llm.with_structured_output(ClassificationResult)

def classify_request_with_ai(requst_text:str):
    prompt = f"""
    Sen profesyonel bir müşteri hizmetleri asistanısın.
    Aşağıdaki müşteri talebini analiz et ve sonucu sana verilen formatta döndür.

    Kategoriler : techincal, billign, sales,feedback
    Öncelikler: low,medium,high,urgent

    Müşteri Mesajı: {requst_text}
    """

    try : 
        result = structured_llm.invoke(prompt)
        return result
    except Exception as e:
        print(f"AI İşleme HAtası {e}")
        return None
    

# Tabloları oluşturalım 
create_db_and_tables()

#Csv dosyasını okuyalım 
df = pd.read_csv("data/sample_requests.csv")
print(f"Toplam {len(df)} talep bulundu. İşleme başlıyor...\n")

#Satır satır işlemleri yapalım 
for _,row in df.iterrows():
    print(f"İşleniyor: {row['ticket_id']}")

    try:
        customer_request = CustomerRequest(
            ticket_id=row["ticket_id"],
            customer_id=row["customer_id"],
            channel=row["channel"],
            request_text=row["request_text"],
            created_at=datetime.fromisoformat(row["timestamp"])
        )

        save_customer_request(customer_request)
        print(f"Tablo customer_request'e kaydedildi....")

        result = classify_request_with_ai(row["request_text"])

        if result is None:
            print(f"{row['ticket_id']} sınıflandırılamadı,atlanıyor")
            continue

        #Sonucu request_classification tablosuna kaydet
        classification = RequestClassification(
            ticket_id=row["ticket_id"],
            category=result.category,
            priority=result.priority,
            tags=result.tags,
            estimated_resolution_time=result.estimated_resolution_time,
            confidence=result.confidence,
            processed_at=datetime.now()
        )
        save_classification(classification)
        print(f" {row['ticket_id']} request_classifications tablosuna kaydedildi.")

        time.sleep(1)

    except Exception as e:
        print(f" {row['ticket_id']} işlenirken hata: {e}")
        continue

