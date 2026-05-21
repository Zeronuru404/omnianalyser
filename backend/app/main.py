"""
OmniAnalyser — Universal AI Analysis Platform
FastAPI backend with MiMo multi-agent analysis pipeline
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from app.core.config import settings
from app.core.token_tracker import TokenTracker
from app.api.routes import router
from app.services.mimo_client import MiMoClient

load_dotenv()

token_tracker = TokenTracker()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔬 OmniAnalyser starting...")
    print(f"   Model: {settings.MIMO_MODEL}")
    print(f"   Token budget: {settings.DAILY_TOKEN_BUDGET:,}/day")
    yield
    print("🔬 OmniAnalyser shutting down...")
    await app.state.mimo_client.close()


app = FastAPI(
    title="OmniAnalyser",
    description="Universal AI Analysis Platform — Upload any file, get intelligent analysis powered by Xiaomi MiMo V2.5",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.token_tracker = token_tracker
app.state.mimo_client = MiMoClient(
    settings.MIMO_API_KEY, settings.MIMO_BASE_URL,
    settings.MIMO_MODEL, settings.MIMO_VL_MODEL,
)

app.include_router(router, prefix="/api")

# Serve frontend static files
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.isdir(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    async def serve_frontend():
        return FileResponse(os.path.join(frontend_dir, "index.html"))
