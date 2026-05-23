import os
import json
from fastapi import APIRouter, Depends
from sqlmodel import Session
from openai import OpenAI
from dotenv import load_dotenv
from models import RawProductReview, ProductReview, ProductReviewRate
from database import get_db

load_dotenv()

router = APIRouter()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODELS = [
    "google/gemma-4-31b-it:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "nousresearch/hermes-3-llama-3.1-405b:free",
]

@router.post("/llm/chat", response_model=ProductReviewRate)
async def predict_llm(input: RawProductReview, session: Session = Depends(get_db)):
    
    content = None
    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a product review analyzer. Analyze the given review and return ONLY a JSON object with these fields:
                        - rating: integer 1-5
                        - sentiment: one of "positive", "negative", "neutral", "mixed"
                        - confidence: float 0.0-1.0
                        - language: ISO 639-1 code (e.g. "en", "tr")
                        - key_points: list of strings, lowercase, 1-3 words each
                        Return ONLY the JSON, no extra text."""
                    },
                    {
                        "role": "user",
                        "content": f"Product: {input.product}\nReview: {input.review}"
                    }
                ]
            )
            content = response.choices[0].message.content.strip()
            break
        except Exception:
            continue

    if content is None:
        raise Exception("All models failed")

    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()

    parsed = json.loads(content)
    parsed_review = ProductReview(**parsed)

    db_record = ProductReviewRate(
        user_info=input.user,
        review=input.review,
        product=input.product,
        rate=parsed_review.rating,
        sentiment=parsed_review.sentiment,
        confidence=parsed_review.confidence,
        language=parsed_review.language,
        key_points=json.dumps(parsed_review.key_points)
    )

    session.add(db_record)
    session.commit()
    session.refresh(db_record)

    return db_record