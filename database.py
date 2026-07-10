from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///spots.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


Base = declarative_base()


class Spot(Base):

    __tablename__ = "spots"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    description = Column(String)

    latitude = Column(Float)

    longitude = Column(Float)

    category = Column(String)

    calmness = Column(Integer)

    image = Column(String, nullable=True)


Base.metadata.create_all(bind=engine)


SessionLocal = sessionmaker(bind=engine)