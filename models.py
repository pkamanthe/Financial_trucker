from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    
    financial_records = relationship("FinancialRecord", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"

class FinancialRecord(Base):
    __tablename__ = 'financial_records'
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    
    user = relationship("User", back_populates="financial_records")

    def __repr__(self):
        return f"FinancialRecord(id={self.id}, amount={self.amount}, type='{self.type}', date={self.date}, user_id={self.user_id})"
