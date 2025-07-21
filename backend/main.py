from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from config import Config
from database import db
from api import auth, generation, files

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    await db.connect()
    print("🚀 SmartSynth Backend started successfully!")
    yield
    # Shutdown
    await db.disconnect()
    print("👋 SmartSynth Backend shutdown complete!")

# Create FastAPI app
app = FastAPI(
    title=Config.PROJECT_NAME,
    description="SmartSynth - AI-Powered Synthetic Data Generation Platform",
    version=Config.VERSION,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=Config.API_V1_STR)
app.include_router(generation.router, prefix=Config.API_V1_STR)
app.include_router(files.router, prefix=Config.API_V1_STR)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": f"{Config.PROJECT_NAME} is running",
        "version": Config.VERSION
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {Config.PROJECT_NAME}",
        "version": Config.VERSION,
        "docs": "/docs",
        "health": "/health"
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"success": False, "message": "Endpoint not found", "error": str(exc)}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal server error", "error": str(exc)}
    )

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG
    ) 