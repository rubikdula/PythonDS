from sqlalchemy import Column, String, Integer, Float, Text
from .database import Base

class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(255), nullable=True)
    verdict = Column(String(255))
    confidence_score = Column(Float, nullable=False)