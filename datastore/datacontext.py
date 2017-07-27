from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import BASE, Ticker, Quote

class datacontext:
    engine = create_engine("sqlite:///ticker.db")
    BASE.metadata.bind = engine
    DBSession = sessionmaker.configure(bind=engine)
    session = DBSession()

    def add_tickers(self, tickers):
        self.session.add_all(tickers)
        self.session.commit()

    def add_quotes(self, quotes):
        """
        Add quotes to the database
        quotes is a dictionary of ticker symbols and quote data
        We will need to patch the ticker id's in quote
        """
        for key, quotelist in quotes:
            rs = self.session.query(Ticker).where("ticker={ticker}".format(ticker=key))
            for q in quotelist:
                q.ticker_id = rs.ticker_id
            self.session.add_all(quotelist)
        
        self.session.commit()
