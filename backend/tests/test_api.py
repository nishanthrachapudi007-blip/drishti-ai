import io
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)
def test_health():
    r=client.get('/health'); assert r.status_code==200; assert r.json()['medical_use'] is False
def test_screening_requires_consent(): assert client.post('/screenings',json={'consent_confirmed':False}).status_code==422
def test_complete_demo_flow():
    made=client.post('/screenings',json={'consent_confirmed':True}); assert made.status_code==201; sid=made.json()['id']
    buf=io.BytesIO(); Image.new('RGB',(64,64),'#6d2825').save(buf,'JPEG')
    uploaded=client.post(f'/screenings/{sid}/image',files={'file':('retina.jpg',buf.getvalue(),'image/jpeg')}); assert uploaded.status_code==200
    result=client.post(f'/screenings/{sid}/analyze'); assert result.status_code==200; assert result.json()['is_demo'] is True; assert result.json()['predicted_class']==2

