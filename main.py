from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import logging
import os
from pathlib import Path

from api.routes import router as onboarding_router
from api.hyrox_routes import router as hyrox_router
from config.database import init_db, close_db
from services.error_logger import error_logger

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
    
    # Initialise database connection pool
    try:
        init_db()
        logger.info("Database connection pool initialised")
    except Exception as e:
        logger.warning(f"Database initialisation failed (non-fatal): {e}")
    
    yield
    
    # Shutdown
    await close_db()
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

# Configure CORS — restrict origins per environment
_cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware (lightweight)
@app.middleware("http")
async def log_requests(request, call_next):
    """Log requests for debugging."""
    if request.method == "OPTIONS":
        return await call_next(request)
    
    response = await call_next(request)
    
    # Only log non-200 responses
    if response.status_code >= 400:
        logger.warning(f"{request.method} {request.url.path} -> {response.status_code}")
    
    return response


# Include routers
app.include_router(onboarding_router)
app.include_router(hyrox_router)


@app.get("/")
async def root():
    """Root endpoint with application information."""
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "description": APP_DESCRIPTION,
        "status": "running",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": APP_NAME,
        "version": APP_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
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


# Error handlers - all errors logged centrally via error_logger
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    errors = exc.errors()
    
    # Log to central error store
    trace_id = error_logger.log_validation_error(
        validation_errors=[f"{'.'.join(str(l) for l in e['loc'])}: {e['msg']}" for e in errors],
        request_data={"path": str(request.url.path), "method": request.method},
    )
    
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "VALIDATION_ERROR", "message": "Invalid request data", "trace_id": trace_id}},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    msg = exc.detail if isinstance(exc.detail, str) else exc.detail.get("message", "Request failed")
    
    # Log 4xx/5xx to central store
    if exc.status_code >= 400:
        trace_id = error_logger.log_error(
            error_code=f"HTTP_{exc.status_code}",
            error_message=msg,
            error_details={"path": str(request.url.path), "detail": exc.detail},
        )
    else:
        trace_id = None
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": f"HTTP_{exc.status_code}", "message": msg, "trace_id": trace_id}},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    trace_id = error_logger.log_error(
        error_code="INTERNAL_ERROR",
        error_message="Unexpected server error",
        error_details={"exception": str(exc), "type": type(exc).__name__},
        context={"path": str(request.url.path), "method": request.method},
    )
    
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_ERROR", "message": "Something went wrong", "trace_id": trace_id}},
    )


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