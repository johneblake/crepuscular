"""Create the database tables"""
import datetime
from decimal import Decimal
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, Integer, String, Numeric, BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

base = declarative_base() # pylint: disable=C0103

class Ticker(base):
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

class Quote(base):
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
        try:
            self.date = datetime.datetime.strptime(date, "%Y-%m-%d")
        except: # pylint: disable=W0702
            self.date = datetime.datetime.now()
        try:
            self.high = Decimal(high)
        except: # pylint: disable=W0702
            self.high = 0
        try:
            self.low = Decimal(low)
        except: # pylint: disable=W0702
            self.low = 0
        try:
            self._open = Decimal(_open)
        except: # pylint: disable=W0702
            self._open = 0
        try:
            self.close = Decimal(close)
        except: # pylint: disable=W0702
            self.close = 0
        try:
            self.volume = int(Decimal(volume))
        except: # pylint: disable=W0702
            self.volume = 0
        self.ticker_id = ticker_id
