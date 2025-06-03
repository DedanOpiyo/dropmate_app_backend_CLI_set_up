# app/debug.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import User, Shipment, Location, Service  ### not from app.models.base

if __name__ == '__main__':
    
    engine = create_engine('sqlite:///dropmate.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    print("Hello!!")

    import ipdb; ipdb.set_trace()
