# app/main.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os

app = FastAPI(title="Minimal Fastapi Example", docs_url="/docs")

# The static dir is for file that should be accessed directly (ex: css, js, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# The template dir is for frontend file that can have parameters
templates = Jinja2Templates(directory="app/templates")

# Definition of the starting page (through templating)
@app.get("/")
async def root(request: Request):
    # Listing the images in the static/photos directory to give as parameter to the template
    photoList = []
    for filename in os.listdir('static/photos'):
        if filename.endswith(".jpg"):
            photoList.append(os.path.join('static','photos', filename))
        else:
            continue
    return templates.TemplateResponse(request, "home.html", context={"photoList":photoList})

# Running the actual app
if __name__ == "__main__":
    # Managing the binder specificity
    if "JUPYTERHUB_SERVICE_PREFIX" in os.environ.keys():
        BINDER_URL=f"{os.environ.get('JUPYTERHUB_SERVICE_PREFIX')}proxy/8000/"
        uvicorn.run(app, host="localhost", port=8000, root_path=BINDER_URL)
    else:
        uvicorn.run(app, host="localhost", port=8000)
