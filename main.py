import uvicorn
from app.core.config import settings
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from app.core.security import verify_and_return_data
from app.api.endpoints.v1.cars import router as car_router
from app.api.endpoints.v1.users import router, get_current_user


app = FastAPI()

app.mount("/static", StaticFiles(directory=settings.STATIC_URL), name="static")
templates = Jinja2Templates(directory=settings.TEMPLATES_URL)

app.include_router(router)
app.include_router(car_router)


@app.get("/", response_class=HTMLResponse)
def read_main(request: Request):
    access_token = request.cookies.get("access_token")
    user = verify_and_return_data(access_token)

    if not user:
        return templates.TemplateResponse('index.html', {'request': request})

    # Sends user's profile photo path to the template for frontend display
    return templates.TemplateResponse('index.html', {'request': request, 'photo': user['photo']})


@app.get("/profile", response_class=HTMLResponse)
def profile_page(request: Request, user: str = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)