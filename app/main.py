# app/main.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os

app = FastAPI(title="Smoothie minimal test", docs_url="/docs")

app.mount("/public", StaticFiles(directory="public"), name="public")

templates = Jinja2Templates(directory="app/templates")

photoList = []
for filename in os.listdir('public/photos'):
    if filename.endswith(".jpg"):
        photoList.append(os.path.join('public','photos', filename))
    else:
        continue

print(photoList)

@app.get("/", include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse(request, "home.html", context={"photoList":photoList})

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
