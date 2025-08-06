import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.api.endpoints.v1.cars import router as car_router
from app.api.endpoints.v1.rentals import router as rental_router
from app.api.endpoints.v1.info import router as info_router
from app.api.endpoints.v1.users import router
from app.db.cars import cars
from app.services.user_services import get_user_page


app = FastAPI()

app.mount("/static", StaticFiles(directory=settings.STATIC_URL), name="static")
templates = Jinja2Templates(directory=settings.TEMPLATES_URL)

app.include_router(router)
app.include_router(car_router)
app.include_router(rental_router)
app.include_router(info_router)


@app.get("/", response_class=HTMLResponse)
def read_main(request: Request, user = Depends(get_user_page)):
    if not user:
        return templates.TemplateResponse(
            'index.html', {
                'request': request,
                'cities': cars.select_all_cities()
            }
        )
    return templates.TemplateResponse(
        'index.html', {
            'request': request,
            'cities': cars.select_all_cities(),
            'photo': user['user'].get('profile_icon')
        }
    )


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)