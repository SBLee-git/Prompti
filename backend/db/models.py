from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from backend.db.database import Base
import enum

# 사용자 유형 ENUM
class UserType(str, enum.Enum):
    company = "company"
    individual = "individual"

# 사용자 모델
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    user_type = Column(Enum(UserType), nullable=False)  # company / individual
    created_at = Column(DateTime(timezone=True), server_default=func.now())
