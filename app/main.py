# app/main.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os

app = FastAPI(title="Minimal Fastapi Example", docs_url="/docs")

app.mount("/public", StaticFiles(directory="public"), name="public")

templates = Jinja2Templates(directory="app/templates")

photoList = []
for filename in os.listdir('public/photos'):
    if filename.endswith(".jpg"):
        photoList.append(os.path.join('public','photos', filename))
    else:
        continue

print(photoList)

@app.get("/", include_in_schema=True)
async def root(request: Request):
    return templates.TemplateResponse(request, "home.html", context={"photoList":photoList})

if __name__ == "__main__":
    if "JUPYTERHUB_SERVICE_PREFIX" in os.environ.keys():
        BINDER_URL=f"{os.environ.get('JUPYTERHUB_SERVICE_PREFIX')}proxy/8000/"
        uvicorn.run(app, host="localhost", port=8000, root_path=BINDER_URL)
    else:
        uvicorn.run(app, host="localhost", port=8000)
