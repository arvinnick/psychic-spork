import uvicorn
from fastapi import FastAPI
from starlette.responses import HTMLResponse

from app.core.config import settings
from app.core.logger import logger
from app.routers.crud_router import crud_router

app = FastAPI()
logger.info("Starting the application...")

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("app/readme.html", "r") as f:
        content = f.read()
        return content


app.include_router(crud_router)
logger.info("Added the crud router.")



# if settings.DEBUG:
#     logger.info("The app is running in debug mode.")
#     if __name__ == "__main__":
#         uvicorn.run(app, host="0.0.0.0", port=8000)
#         logger.info("The app is running as the main function.")
