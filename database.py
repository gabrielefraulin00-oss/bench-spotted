from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
import os


DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:YOUR_PASSWORD@db.sqxlvbmjmjfjlyfhhozt.supabase.co:5432/postgres"
)


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "sslmode": "require"
    }
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


    ratings = relationship(
        "Rating",
        back_populates="spot",
        cascade="all, delete-orphan"
    )


    comments = relationship(
        "Comment",
        back_populates="spot",
        cascade="all, delete-orphan"
    )



class Rating(Base):

    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)

    spot_id = Column(
        Integer,
        ForeignKey("spots.id")
    )

    stars = Column(Integer)


    spot = relationship(
        "Spot",
        back_populates="ratings"
    )



class Comment(Base):

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)

    spot_id = Column(
        Integer,
        ForeignKey("spots.id")
    )

    text = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    spot = relationship(
        "Spot",
        back_populates="comments"
    )



Base.metadata.create_all(bind=engine)


SessionLocal = sessionmaker(
    bind=engine
)