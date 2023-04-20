from sqlalchemy import Column, TEXT, INT, BIGINT, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NEWSROOM_USER(Base):
    __tablename__ = "NEWSROOM_USER"

    user_id = Column(BIGINT, nullable=False, autoincrement=True, primary_key=True)
    company_id = Column(TEXT, nullable=False)
    def getID(self):
        return self.user_id

class SCRAPE_KEYWORD(Base):
    __tablename__ = 'SCRAPE_KEYWORD'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    keyword = Column(TEXT, nullable=False)
    newsroom_user = Column(BIGINT, ForeignKey('NEWSROOM_USER.user_id'), nullable=False)

    def getID(self):
        return self.id


class SCRAPED_NEWS(Base):
    __tablename__ = 'SCRAPED_NEWS'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    title = Column(TEXT, nullable=False)
    summary = Column(TEXT, nullable=False)
    broadcaster = Column(TEXT, nullable=False)
    url = Column(TEXT, nullable=False)
    created_at = Column(DateTime, nullable=False)
    keyword = Column(BIGINT, ForeignKey('SCRAPE_KEYWORD.id'), nullable=False)
    # keyword = relationship(SCRAPE_KEYWORD)
    user = Column(BIGINT, ForeignKey('NEWSROOM_USER.user_id'), nullable=False)
    # user = relationship('NEWSROOM_USER')

    def __repr__(self):
        return f"<SCRAPED_NEWS(id='{self.id}', title='{self.title}', summary='{self.summary}', broadcaster='{self.broadcaster}', created_at='{self.created_at}', keyword='{self.keyword.keyword}', user='{self.user.company_id}')>"
    
    def getID(self):
        return self.id