"""
Data Context Module
"""
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from datastore.tabledef import BASE, Ticker

class DataContext():
    """
    Access the ticker.db
    """
    def __init__(self):
        self.engine = create_engine("sqlite:///ticker.db")
        BASE.metadata.bind = self.engine
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()

    def create(self):
        self.BASE.metadata.create_all(self.engine);

    def add_tickers(self, tickers):
        """
        Add list of tickers to the ticker table
        """
        self.session.add_all(tickers)
        self.session.commit()

    def add_quotes(self, quotes):
        """
        Add quotes to the database
        quotes is a dictionary of ticker symbols and quote data
        We will need to patch the ticker id's in quote
        """
        for key, quotelist in quotes:
            records = self.session.query(Ticker).where("ticker={ticker}".format(ticker=key))
            for quote in quotelist:
                quote.ticker_id = records.ticker_id
            self.session.add_all(quotelist)

        self.session.commit()

    def get_etfs(self):
        """
        Grab all the etfs in the symbol table
        """
        records = self.session.query(Ticker).filter(Ticker.security=="etf")
        return [item.ticker for item in records]