from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from configs.config import DATABASE_URL

from datetime import datetime


Base = declarative_base()

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)
    location = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    
    def __repr__(self):
        return f"""<Order(order_id={self.order_id}, status='{self.status}',
                 location='{self.location}')>"""
    
    def to_dict(self):
        return {
            'order_id': self.order_id,
            'status': self.status,
            'location': self.location,
            'created_at': self.created_at.isoformat()
        }
    

Base.metadata.create_all(engine)
