"""
Main FastAPI application for AI Insurance Assistant.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import get_settings
from app.api.routes import router
from app.services.database_service import db_service
from app.services.vector_service import vector_store_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("Starting AI Insurance Assistant...")
    settings = get_settings()

    # Initialize database
    await db_service.init_db()
    print("✓ Database initialized")

    # Initialize vector store
    vector_store_service.initialize_knowledge_base()
    print("✓ Knowledge base initialized")

    print(f"✓ {settings.app_name} v{settings.app_version} ready!")
    print(f"\n📡 API Endpoint: http://localhost:{settings.port}/api/v1")
    print(f"📚 API Docs: http://localhost:{settings.port}/docs")
    print(f"\n🌐 Web Interface: http://localhost:{settings.port}")
    print(f"   Open your browser and start chatting!")

    yield

    # Shutdown
    print("Shutting down...")
    await db_service.close()
    print("✓ Cleanup complete")


# Create FastAPI app
settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered insurance assistant chatbot",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["Chat"])

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Serve the main web interface."""
    return FileResponse("static/index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host=settings.host, port=settings.port, reload=settings.debug
    )
