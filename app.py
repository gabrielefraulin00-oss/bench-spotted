from fastapi.templating import Jinja2Templates
from fastapi import Request, Form, UploadFile, File, FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from database import SessionLocal, Spot
import shutil
import os
import uuid

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@app.get("/add", response_class=HTMLResponse)
def add_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="add_spot.html",
        context={"request": request}
    )


@app.post("/add")
def save_spot(
    name: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    calmness: int = Form(...),
    latitude: float = Form(46.06),
    longitude: float = Form(13.23),
    image: UploadFile = File(None)
):

    print("====== ADD SPOT STARTED ======")
    print(name, image.filename if image else "NO IMAGE")

    db = SessionLocal()

    image_path = None

    # Only try to save if a real file was actually selected
    if image and image.filename:

        os.makedirs(
            "static/uploads",
            exist_ok=True
        )

        # Prefix with a uuid so two uploads with the same filename
        # (e.g. "photo.jpg") never overwrite each other
        unique_name = f"{uuid.uuid4().hex}_{image.filename}"

        image_path = "static/uploads/" + unique_name

        with open(image_path, "wb") as buffer:

            shutil.copyfileobj(
                image.file,
                buffer
            )

    new_spot = Spot(

        name=name,
        description=description,
        category=category,
        calmness=calmness,
        latitude=latitude,
        longitude=longitude,
        image=image_path

    )

    db.add(new_spot)

    try:

        db.commit()
        print("DATABASE OK")

    except Exception as e:

        print("DATABASE ERROR:", e)
        db.rollback()

    finally:

        db.close()

    return RedirectResponse("/", status_code=303)


@app.get("/api/spots")
def api_spots():

    db = SessionLocal()

    spots = db.query(Spot).all()

    result = []

    for spot in spots:

        result.append({

            "id": spot.id,
            "name": spot.name,
            "description": spot.description,
            "latitude": spot.latitude,
            "longitude": spot.longitude,
            "category": spot.category,
            "calmness": spot.calmness,
            "image": spot.image

        })

    db.close()

    return result