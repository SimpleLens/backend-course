from fastapi import FastAPI
from hotels import router as hotels_router
import uvicorn

app = FastAPI()
app.include_router(hotels_router)


if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)
