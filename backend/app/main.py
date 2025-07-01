"""
Main FastAPI application for Error Log Analytics
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.core.config import settings
from app.api import upload, analyze, errors

# Create FastAPI application
app = FastAPI(
    title="Error Log Analytics API",
    description="Advanced analysis of AMS error logs (Visual Objects & .NET)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(analyze.router, prefix="/api", tags=["analyze"])
app.include_router(errors.router, prefix="/api", tags=["errors"])

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Error Log Analytics API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}