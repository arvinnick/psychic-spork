import uvicorn
from fastapi import FastAPI

from app.config import settings
from app.logger import logger
from app.db.crud.crud import crud_router


app = FastAPI()
logger.info("Starting the application...")


app.include_router(crud_router)
logger.info("Added the crud router.")



if settings.DEBUG:
    logger.info("The app is running in debug mode.")
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)
        logger.info("The app is running as the main function.")
