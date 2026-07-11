from fastapi.templating import Jinja2Templates
from fastapi import Request, Form, UploadFile, File, FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from database import (
    SessionLocal,
    Spot,
    Rating,
    Comment
)

import shutil
import os
import uuid


app = FastAPI()


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


templates = Jinja2Templates(
    directory="templates"
)



@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )



@app.get("/add", response_class=HTMLResponse)
def add_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="add_spot.html",
        context={
            "request": request
        }
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

    db = SessionLocal()

    image_path = None


    if image and image.filename:

        os.makedirs(
            "static/uploads",
            exist_ok=True
        )


        unique_name = (
            f"{uuid.uuid4().hex}_{image.filename}"
        )


        image_path = (
            "static/uploads/"
            + unique_name
        )


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

    db.commit()

    db.close()


    return RedirectResponse(
        "/",
        status_code=303
    )



@app.get("/api/spots")
def api_spots():

    db = SessionLocal()


    spots = db.query(Spot).all()


    result = []


    for spot in spots:


        average = 0


        if len(spot.ratings) > 0:

            average = round(
                sum(
                    r.stars
                    for r in spot.ratings
                )
                /
                len(spot.ratings),
                1
            )



        result.append({

            "id": spot.id,

            "name": spot.name,

            "description": spot.description,

            "latitude": spot.latitude,

            "longitude": spot.longitude,

            "category": spot.category,

            "calmness": spot.calmness,

            "image": spot.image,

            "rating": average,

            "comments": [
                {
                    "text": c.text,
                    "date": c.created_at
                }
                for c in spot.comments
            ]

        })


    db.close()


    return result




# ============================
# DELETE SPOT
# ============================


@app.delete("/delete_spot/{spot_id}")
def delete_spot(
    spot_id: int
):

    db = SessionLocal()


    spot = (
        db.query(Spot)
        .filter(
            Spot.id == spot_id
        )
        .first()
    )


    if not spot:

        db.close()

        return {
            "success": False
        }



    # Remove image file

    if spot.image:

        if os.path.exists(
            spot.image
        ):

            os.remove(
                spot.image
            )



    db.delete(spot)

    db.commit()

    db.close()


    return {
        "success": True
    }




# ============================
# ADD RATING
# ============================


@app.post("/rate/{spot_id}")
def rate_spot(
    spot_id: int,
    stars: int = Form(...)
):

    db = SessionLocal()


    if stars < 1 or stars > 5:

        db.close()

        return {
            "error": "Invalid rating"
        }



    rating = Rating(

        spot_id=spot_id,

        stars=stars

    )


    db.add(rating)

    db.commit()

    db.close()


    return {
        "success": True
    }




# ============================
# ADD COMMENT
# ============================


@app.post("/comment/{spot_id}")
def add_comment(
    spot_id: int,
    text: str = Form(...)
):

    db = SessionLocal()


    comment = Comment(

        spot_id=spot_id,

        text=text

    )


    db.add(comment)

    db.commit()

    db.close()


    return {
        "success": True
    }