"""Create the database tables"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, Integer, String, Numeric, BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

ENGINE = create_engine("sqlite:///ticker.db")
BASE = declarative_base()

class Ticker(BASE):
    """Stores tickers"""
    __tablename__ = "ticker"
    id = Column(Integer, primary_key=True) # pylint: disable=C0103
    ticker = Column(String)
    description = Column(String)
    security = Column(String)

    def __init__(self, ticker, security, description):
        self.description = description
        self.ticker = ticker
        self.security = security

class Quote(BASE):
    """Stores quotes"""
    __tablename__ = "quote"
    id = Column(Integer, primary_key=True) # pylint: disable=C0103
    date = Column(Date)
    high = Column(Numeric)
    low = Column(Numeric)
    _open = Column(Numeric)
    close = Column(Numeric)
    volume = Column(BigInteger)
    ticker_id = Column(Integer, ForeignKey("ticker.id"))
    ticker = relationship(Ticker, backref=backref('quotes', uselist=True, cascade='delete,all'))

    def __init__(self, ticker_id, date, high, low, _open, close, volume):
        self.date = date
        self.high = high
        self.low = low
        self._open = _open
        self.close = close
        self.volume = volume
        self.ticker_id = ticker_id

BASE.metadata.create_all(ENGINE)
