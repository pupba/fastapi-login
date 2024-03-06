import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# router
from routers import login

app = FastAPI()
app.include_router(login.router)

app.mount("/static", StaticFiles(directory='static'), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse, tags=['root'])
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name='index.html', context={"title": "Login"}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
