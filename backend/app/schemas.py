from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=120)
class LoginRequest(BaseModel): email: EmailStr; password: str
class TokenResponse(BaseModel): access_token: str; token_type: str = "bearer"
class ScreeningCreate(BaseModel): patient_reference: str | None = Field(default=None, max_length=120); consent_confirmed: bool
class ScreeningResponse(BaseModel): id: UUID; status: str; created_at: datetime
class PredictionResponse(BaseModel):
    screening_id: UUID; is_demo: bool = True; predicted_class: int; label: str
    confidence: float = Field(ge=0, le=1); probabilities: list[float]; risk_level: str
    explanation_method: str; explanation_summary: str; recommendation: str; disclaimer: str

