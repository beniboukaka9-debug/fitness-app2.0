"""Main application factory"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database.db import init_db
from app.api import users, activities, workouts

settings = get_settings()

def create_app():
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="Fitness App API",
        description="AI-powered fitness tracking and workout generation",
        version="2.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(users.router)
    app.include_router(activities.router)
    app.include_router(workouts.router)
    
    # Initialize database
    @app.on_event("startup")
    def startup_event():
        """Initialize database on startup"""
        init_db()
        print("✅ Database initialized")
    
    @app.get("/health")
    def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "app": "Fitness App API",
            "version": "2.0.0"
        }
    
    return app

app = create_app()
