from dotenv import load_dotenv
from src.constants import ENV_FILE_PATH

load_dotenv(dotenv_path=ENV_FILE_PATH, verbose=False)

import os
import logging
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.settings import init_settings
from app.api.routers.chat import chat_router
from src.routers.management.config import config_router
from src.routers.management.files import files_router
from src.routers.management.tools import tools_router
from src.routers.management.loader import loader_router
from src.models.model_config import ModelConfig
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)
init_settings()

environment = os.getenv("ENVIRONMENT")
if environment == "dev":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add chat router from create_llama/backend
app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])
app.include_router(config_router, prefix="/api/management/config")
app.include_router(tools_router, prefix="/api/management/tools", tags=["Agent"])
app.include_router(files_router, prefix="/api/management/files", tags=["Knowledge"])
app.include_router(loader_router, prefix="/api/management/loader", tags=["Knowledge"])

# Mount the data files to serve the file viewer
app.mount(
    "/api/files/data",
    StaticFiles(directory="data", check_dir=False),
)

# Mount the output files from tools
app.mount(
    "/api/files/tool-output",
    StaticFiles(directory="tool-output", check_dir=False),
)

# Mount the frontend static files
app.mount(
    "",
    StaticFiles(directory="static", check_dir=False, html=True),
)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=3000, loop="asyncio", reload=(environment == "dev"))
