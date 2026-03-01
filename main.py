from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from pathlib import Path

from api.routes import router as onboarding_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Application metadata
APP_NAME = "Alloy AI Fitness System"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "AI-powered fitness program generation with hierarchical goal optimization"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    
    # Validate required configuration files exist
    config_dir = Path(__file__).parent / "config"
    required_files = ["program_config.yaml", "goal_normalization.yaml"]
    
    for file in required_files:
        file_path = config_dir / file
        if not file_path.exists():
            logger.warning(f"Configuration file not found: {file_path}")
            # Create default files if they don't exist
            create_default_config(file_path, file)
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {APP_NAME}")


def create_default_config(file_path: Path, config_type: str):
    """Create default configuration files if they don't exist."""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if config_type == "program_config.yaml":
            default_content = """# Alloy AI Fitness System - Program Configuration
session_constraints:
  warmup:
    compound: false
    spinal_compression: ["none", "low"]
    min_duration: 5
    max_duration: 15
    
  cooldown:
    compound: false
    spinal_compression: ["none", "low"]
    min_duration: 5
    max_duration: 15
    
  main_blocks:
    resistance_accessory:
      compound: true
      disciplines: ["strength", "hypertrophy"]
      min_duration: 20
      max_duration: 90
      
    resistance_circuits:
      compound: true
      disciplines: ["strength", "endurance"]
      min_duration: 15
      max_duration: 60
      
    hyrox_style:
      disciplines: ["endurance", "mixed"]
      min_duration: 20
      max_duration: 45
      
    mobility_only:
      compound: false
      disciplines: ["mobility"]
      min_duration: 15
      max_duration: 45
      
    cardio_only:
      disciplines: ["endurance"]
      min_duration: 20
      max_duration: 60

time_allocation:
  warmup: 0.15
  main: 0.70
  cooldown: 0.15
"""
        else:  # goal_normalization.yaml
            default_content = """# Alloy AI Fitness System - Goal Normalization Configuration
slider_normalization:
  primary:
    steepness: 6.0
    midpoint: 0.5
    influence_range: 0.8
    
  secondary_sliders:
    hypertrophy_fat_loss:
      base_weight: 0.5
      strength_influence: 0.3
      endurance_influence: -0.2
      steepness: 4.0
      midpoint: 0.5
      
    power_mobility:
      base_weight: 0.5
      strength_influence: 0.4
      endurance_influence: -0.3
      steepness: 5.0
      midpoint: 0.5

goal_hierarchy:
  primary_goal_weight: 0.6
  secondary_goal_weight: 0.4
  
session_probability_modifiers:
  strength_bias:
    resistance_accessory: 1.2
    resistance_circuits: 1.1
    hyrox_style: 0.8
    mobility_only: 0.7
    cardio_only: 0.6
    
  endurance_bias:
    resistance_accessory: 0.8
    resistance_circuits: 1.1
    hyrox_style: 1.3
    mobility_only: 0.9
    cardio_only: 1.4

validation:
  mathematical_constraints:
    min_normalized_value: 0.05
    max_normalized_value: 0.95
"""
        
        with open(file_path, 'w') as f:
            f.write(default_content)
        
        logger.info(f"Created default configuration file: {file_path}")
        
    except Exception as e:
        logger.error(f"Failed to create default config file {file_path}: {e}")


# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(onboarding_router)


@app.get("/")
async def root():
    """Root endpoint with application information."""
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "description": APP_DESCRIPTION,
        "status": "running",
        "timestamp": "2024-01-01T00:00:00Z"  # Will be replaced with actual timestamp
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": APP_NAME,
        "version": APP_VERSION,
        "timestamp": "2024-01-01T00:00:00Z"  # Will be replaced with actual timestamp
    }


@app.get("/api/info")
async def api_info():
    """API information endpoint."""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "description": APP_DESCRIPTION,
        "endpoints": {
            "onboarding": {
                "validate_sliders": "POST /api/onboarding/validate-sliders",
                "generate_program": "POST /api/onboarding/generate-program",
                "health": "GET /api/onboarding/health",
                "config_sliders": "GET /api/onboarding/config/sliders",
                "config_time_allocation": "GET /api/onboarding/config/time-allocation"
            },
            "system": {
                "health": "GET /health",
                "info": "GET /api/info"
            }
        },
        "features": [
            "Hierarchical goal slider normalization",
            "Deterministic program skeleton generation",
            "Session type optimization based on goals",
            "Time allocation with system delegation",
            "Multi-level training block structure"
        ]
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with standardized error format."""
    return {
        "error": {
            "code": getattr(exc, 'code', 'HTTP_ERROR'),
            "message": exc.detail if isinstance(exc.detail, str) else exc.detail.get("message", "HTTP error occurred"),
            "details": exc.detail if isinstance(exc.detail, dict) else None,
            "status_code": exc.status_code,
            "trace_id": f"error_{datetime.now().timestamp()}",
            "timestamp": "2024-01-01T00:00:00Z"  # Will be replaced with actual timestamp
        }
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions with standardized error format."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return {
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "details": str(exc),
            "status_code": 500,
            "trace_id": f"error_{datetime.now().timestamp()}",
            "timestamp": "2024-01-01T00:00:00Z"  # Will be replaced with actual timestamp
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )