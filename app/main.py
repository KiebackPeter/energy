from app.core.logger import log

log.info("Loading fastapi")

from socket import gethostname, gethostbyname   
from fastapi import FastAPI
from fastapi.middleware import cors, httpsredirect

from app.api.routers import api_router

api = FastAPI(
    title="Kieback&Peter",
    version="1.1",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "tryItOutEnabled": True,
        "persistAuthorization": True,
    },
)

origins = [
    "http://localhost:3000",
]

api.add_middleware(
    cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api.add_middleware(httpsredirect.HTTPSRedirectMiddleware)
api.include_router(api_router)

hostname=gethostname()
IPAddr=gethostbyname(hostname)

log.info("Host: %s@%s", hostname, IPAddr)
