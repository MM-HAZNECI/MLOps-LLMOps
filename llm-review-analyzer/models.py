from datetime import datetime, timezone
from typing import Optional, Literal
from sqlmodel import SQLModel, Field

class RawProductReview(SQLModel):
    user:str = Field(...,description="The username or identifier of the reviewer")
    product:str = Field(...,description="The name of the product being reviewed")
    review : str = Field(..., description="The full text content of the review")

    class Config : 
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user": "john_doe",
                "product": "Wireless Headphones XYZ",
                "review": "Amazing product! 5 stars. Quick delivery and great quality, but quite pricey.",
            }
        }

class ProductReview(SQLModel):
    rating: int = Field(description="The rating of the product (1-5)", ge=1, le=5)
    sentiment: Literal["positive", "negative", "neutral", "mixed"] = Field(
        description="Overall sentiment of the review."
    )
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in this analysis (0-1)")
    language: str = Field(description="ISO 639-1 language code", min_length=2, max_length=2)
    key_points: list[str] = Field(description="Key points from the review.")


class ProductReviewRate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_info: str = Field(description="User information or identifier")
    review: str = Field(description="The original review text")
    product: str = Field(index=True, description="Product name or identifier")
    rate: Optional[int] = Field(default=None, description="Rating 1-5")
    sentiment: Optional[str] = Field(default=None, index=True)
    confidence: Optional[float] = Field(default=None)
    language: Optional[str] = Field(default=None, index=True)
    key_points: Optional[str] = Field(default=None, description="Key points as JSON string")
