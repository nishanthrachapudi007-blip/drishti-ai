import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, JSON, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase): pass
def now(): return datetime.now(timezone.utc)

class User(Base):
    __tablename__="users"; id:Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4); email:Mapped[str]=mapped_column(String(320),unique=True,index=True); password_hash:Mapped[str]=mapped_column(String(255)); full_name:Mapped[str]=mapped_column(String(120)); is_active:Mapped[bool]=mapped_column(Boolean,default=True); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class Screening(Base):
    __tablename__="screenings"; id:Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4); user_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),index=True); patient_reference:Mapped[str|None]=mapped_column(String(120)); status:Mapped[str]=mapped_column(String(32),default="created",index=True); consent_confirmed:Mapped[bool]=mapped_column(Boolean); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,index=True); updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,onupdate=now); images:Mapped[list["Image"]]=relationship(cascade="all, delete-orphan"); prediction:Mapped["Prediction|None"]=relationship(cascade="all, delete-orphan")
class Image(Base):
    __tablename__="images"; id:Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4); screening_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("screenings.id",ondelete="CASCADE"),index=True); storage_key:Mapped[str]=mapped_column(String(512),unique=True); content_type:Mapped[str]=mapped_column(String(50)); size_bytes:Mapped[int]=mapped_column(Integer); width:Mapped[int|None]=mapped_column(Integer); height:Mapped[int|None]=mapped_column(Integer); checksum_sha256:Mapped[str]=mapped_column(String(64)); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class Prediction(Base):
    __tablename__="predictions"; id:Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4); screening_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("screenings.id",ondelete="CASCADE"),unique=True); model_version:Mapped[str]=mapped_column(String(100)); is_demo:Mapped[bool]=mapped_column(Boolean,default=True); predicted_class:Mapped[int]=mapped_column(Integer); confidence:Mapped[float]=mapped_column(Float); probabilities:Mapped[list]=mapped_column(JSON); risk_level:Mapped[str]=mapped_column(String(32)); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now); explanation:Mapped["Explanation|None"]=relationship(cascade="all, delete-orphan")
class Explanation(Base):
    __tablename__="explanations"; id:Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4); prediction_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("predictions.id",ondelete="CASCADE"),unique=True); method:Mapped[str]=mapped_column(String(64)); artifact_key:Mapped[str|None]=mapped_column(String(512)); summary:Mapped[str]=mapped_column(Text); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class ScreeningHistory(Base):
    __tablename__="screening_history"; id:Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4); screening_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("screenings.id",ondelete="CASCADE"),index=True); event_type:Mapped[str]=mapped_column(String(64)); actor_id:Mapped[uuid.UUID|None]=mapped_column(ForeignKey("users.id",ondelete="SET NULL")); metadata_json:Mapped[dict]=mapped_column(JSON,default=dict); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,index=True)
Index("ix_screening_user_created",Screening.user_id,Screening.created_at.desc())

