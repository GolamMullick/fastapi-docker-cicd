from sqlalchemy import Column, Integer, String, Float
from database import Base

class Flat(Base):
    __tablename__ = "flats"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    suburb = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String)
