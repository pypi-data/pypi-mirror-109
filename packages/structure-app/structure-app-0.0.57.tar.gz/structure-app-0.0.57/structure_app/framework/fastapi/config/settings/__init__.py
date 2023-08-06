from fastapi import FastAPI
from littlenv import littlenv
from fastapi.middleware.cors import CORSMiddleware

from config import urls
from config.settings.base import API_VERSION
# from config.settings.base import connect_db
# from config.settings.base import close_db

littlenv.load()
itemsInit = {}

app = FastAPI(
    title="FastApi",
    description="FastApi",
    version=API_VERSION,
    redoc_url="/api/v1/redoc",
    docs_url='/api/v1/docs',
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    urls.urls
)

# app.add_event_handler(
#     "startup",
#     connect_db
# )


# app.add_event_handler(
#     "shutdown",
#     close_db
# )
