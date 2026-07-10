from database import SessionLocal, Spot


db = SessionLocal()


spot1 = Spot(
    name="First Bench Spotted location",
    description="A quiet place with a nice view",
    latitude=46.06,
    longitude=13.23,
    category="panorama",
    calmness=9
)


spot2 = Spot(
    name="River Relax Spot",
    description="A peaceful place near the water",
    latitude=46.07,
    longitude=13.24,
    category="nature",
    calmness=8
)


db.add(spot1)
db.add(spot2)

db.commit()

db.close()

print("Database created!")