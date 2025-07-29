import uvicorn
from fastapi import FastAPI, Depends
from app.api.endpoints.v1.users import router, get_current_user
from app.api.endpoints.v1.cars import router as car_router

app = FastAPI()

app.include_router(router)
app.include_router(car_router)

@app.get("/protected")
def protected(user: str = Depends(get_current_user)):
    return {"hello": user}

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)