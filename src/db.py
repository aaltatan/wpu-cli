from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(url="sqlite:///app.db", echo=True)


def get_db():
    Session = sessionmaker(bind=engine)
    try:
        db = Session()
        return db
    finally:
        db.close()


def init_db():
    from .models import Base, Setting, Tax, TaxBracket

    Base.metadata.create_all(engine, [Setting, Tax, TaxBracket])
