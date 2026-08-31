import hashlib, tempfile, uuid
from pathlib import Path
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
from .config import get_settings
from .inference import LABELS, get_inference_service
from .schemas import LoginRequest, PredictionResponse, ScreeningCreate, ScreeningResponse, SignupRequest, TokenResponse

settings=get_settings(); app=FastAPI(title="DrishtiAI API",version="0.1.0",description="Decision-support API. Demo inference is not a medical device or diagnosis.")
app.add_middleware(CORSMiddleware,allow_origins=settings.origins,allow_credentials=True,allow_methods=["GET","POST"],allow_headers=["Authorization","Content-Type"])
DEMO_USER=uuid.UUID("11111111-1111-4111-8111-111111111111"); store:dict[uuid.UUID,dict]={}

@app.get("/health")
async def health(): return {"status":"ok","inference_provider":settings.inference_provider,"medical_use":False}
@app.post("/auth/signup",response_model=TokenResponse,status_code=status.HTTP_201_CREATED)
async def signup(body:SignupRequest): return TokenResponse(access_token="demo-token-not-for-production")
@app.post("/auth/login",response_model=TokenResponse)
async def login(body:LoginRequest): return TokenResponse(access_token="demo-token-not-for-production")
@app.post("/screenings",response_model=ScreeningResponse,status_code=status.HTTP_201_CREATED)
async def create_screening(body:ScreeningCreate):
    if not body.consent_confirmed: raise HTTPException(422,"Consent confirmation is required")
    sid=uuid.uuid4(); from datetime import datetime,timezone; created=datetime.now(timezone.utc); store[sid]={"id":sid,"status":"created","created_at":created,"owner":DEMO_USER}; return ScreeningResponse(id=sid,status="created",created_at=created)
@app.post("/screenings/{screening_id}/image")
async def upload_image(screening_id:uuid.UUID,file:UploadFile=File(...)):
    item=store.get(screening_id)
    if not item: raise HTTPException(404,"Screening not found")
    if file.content_type not in {"image/jpeg","image/png"}: raise HTTPException(415,"Only JPG and PNG images are accepted")
    data=await file.read(settings.max_upload_mb*1024*1024+1)
    if len(data)>settings.max_upload_mb*1024*1024: raise HTTPException(413,"Image exceeds the upload limit")
    try:
        import io
        with Image.open(io.BytesIO(data)) as img: img.verify()
    except (UnidentifiedImageError,OSError): raise HTTPException(422,"File is not a valid image")
    path=Path(tempfile.gettempdir())/f"drishti-{screening_id}.{file.content_type.split('/')[-1]}"; path.write_bytes(data); item.update(status="image_uploaded",image_path=path)
    return {"status":"accepted","checksum_sha256":hashlib.sha256(data).hexdigest()}
@app.post("/screenings/{screening_id}/analyze",response_model=PredictionResponse)
async def analyze(screening_id:uuid.UUID):
    item=store.get(screening_id)
    if not item: raise HTTPException(404,"Screening not found")
    if "image_path" not in item: raise HTTPException(409,"Upload a validated image before analysis")
    result=await get_inference_service(settings.inference_provider,settings.model_path).predict(item["image_path"]); item["status"]="complete"
    risk=["Low","Monitor","Elevated","High","Urgent"][result.predicted_class]
    return PredictionResponse(screening_id=screening_id,is_demo=result.is_demo,predicted_class=result.predicted_class,label=LABELS[result.predicted_class],confidence=max(result.probabilities),probabilities=result.probabilities,risk_level=risk,explanation_method=result.method,explanation_summary=result.summary,recommendation="Arrange review by a qualified eye-care professional. Urgent symptoms require prompt clinical evaluation.",disclaimer="Screening decision support only; not a definitive medical diagnosis.")
@app.get("/screenings")
async def list_screenings(): return list(store.values())
@app.get("/screenings/{screening_id}")
async def get_screening(screening_id:uuid.UUID):
    if screening_id not in store: raise HTTPException(404,"Screening not found")
    return store[screening_id]

