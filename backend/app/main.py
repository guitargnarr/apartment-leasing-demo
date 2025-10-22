"""
FastAPI Main Application
Apartment Leasing Demo - Real-time Integration System
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
import logging

from . import models, schemas, crud, analytics, lead_scoring
from .database import engine, get_db, init_db
from .websocket_manager import manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Apartment Leasing API",
    description="Real-time apartment listing and leasing management system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
# Allow frontend to access API from different origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Initialize database on application startup
    """
    logger.info("Starting up Apartment Leasing API")
    init_db()
    logger.info("Database initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup on application shutdown
    """
    logger.info("Shutting down Apartment Leasing API")


# ============================================================================
# WebSocket Endpoint
# ============================================================================

@app.websocket("/ws/units")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time unit updates

    All connected clients receive instant notifications when:
    - Unit status changes (available → leased)
    - Price updates
    - New units added
    - Units deleted
    """
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and listen for client messages
            data = await websocket.receive_text()
            logger.info(f"Received WebSocket message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected from WebSocket")


# ============================================================================
# Unit Management Endpoints
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API health check
    """
    return {
        "message": "Apartment Leasing API",
        "status": "running",
        "active_connections": manager.get_connection_count(),
        "docs": "/docs"
    }


@app.get("/api/units", response_model=schemas.UnitListResponse, tags=["Units"])
async def get_units(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None, description="Filter by status: available, pending, leased"),
    bedrooms: Optional[int] = Query(None, ge=0, le=10),
    price_min: Optional[int] = Query(None, ge=0),
    price_max: Optional[int] = Query(None, ge=0),
    city: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get list of apartment units with optional filters

    **Filters:**
    - status: available, pending, leased
    - bedrooms: Number of bedrooms
    - price_min: Minimum price
    - price_max: Maximum price
    - city: City name

    **Pagination:**
    - skip: Number of records to skip
    - limit: Maximum records to return
    """
    units = crud.get_units(
        db,
        skip=skip,
        limit=limit,
        status=status,
        bedrooms=bedrooms,
        price_min=price_min,
        price_max=price_max,
        city=city
    )

    total = crud.get_units_count(
        db,
        status=status,
        bedrooms=bedrooms,
        price_min=price_min,
        price_max=price_max
    )

    return {
        "units": units,
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit
    }


@app.get("/api/units/{unit_id}", response_model=schemas.UnitResponse, tags=["Units"])
async def get_unit(unit_id: str, db: Session = Depends(get_db)):
    """
    Get specific unit by ID
    """
    unit = crud.get_unit(db, unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit


@app.post("/api/units", response_model=schemas.UnitResponse, status_code=201, tags=["Units"])
async def create_unit(unit: schemas.UnitCreate, db: Session = Depends(get_db)):
    """
    Create a new apartment unit (admin operation)
    """
    # Create unit
    db_unit = crud.create_unit(db, unit)

    # Calculate initial lead score
    market_data = lead_scoring.get_market_data(db)
    lead_score = lead_scoring.calculate_lead_score(db_unit, market_data)
    crud.update_lead_score(db, db_unit.id, lead_score)

    # Refresh to get updated score
    db.refresh(db_unit)

    # Broadcast new unit to all connected clients
    await manager.broadcast_unit_update(db_unit.to_dict())

    logger.info(f"Created new unit: {db_unit.id}")
    return db_unit


@app.patch("/api/units/{unit_id}", response_model=schemas.UnitResponse, tags=["Units"])
async def update_unit(
    unit_id: str,
    unit_update: schemas.UnitUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing unit

    **Key operation for leasing workflow:**
    - Change status (available → pending → leased)
    - Update price
    - Modify amenities

    **Real-time:** All connected clients notified instantly via WebSocket
    """
    db_unit = crud.update_unit(db, unit_id, unit_update)

    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    # Recalculate lead score if unit is still available
    if db_unit.status == models.UnitStatus.AVAILABLE:
        market_data = lead_scoring.get_market_data(db)
        new_score = lead_scoring.calculate_lead_score(db_unit, market_data)
        crud.update_lead_score(db, unit_id, new_score)
        db.refresh(db_unit)

    # Broadcast update to all connected clients
    await manager.broadcast_unit_update(db_unit.to_dict())

    logger.info(f"Updated unit: {unit_id}, new status: {db_unit.status}")
    return db_unit


@app.delete("/api/units/{unit_id}", status_code=204, tags=["Units"])
async def delete_unit(unit_id: str, db: Session = Depends(get_db)):
    """
    Delete a unit (admin operation)
    """
    success = crud.delete_unit(db, unit_id)

    if not success:
        raise HTTPException(status_code=404, detail="Unit not found")

    # Broadcast deletion to all connected clients
    await manager.broadcast_unit_deleted(unit_id)

    logger.info(f"Deleted unit: {unit_id}")
    return None


# ============================================================================
# Analytics Endpoints
# ============================================================================

@app.get("/api/analytics", response_model=schemas.AnalyticsResponse, tags=["Analytics"])
async def get_analytics(db: Session = Depends(get_db)):
    """
    Get comprehensive analytics dashboard data

    **Metrics:**
    - Unit counts by status
    - Average days to lease
    - Lease conversion rate
    - Average price
    - Most popular features
    - Price trends
    """
    analytics_data = analytics.get_dashboard_analytics(db)
    return analytics_data


@app.get("/api/analytics/trends", tags=["Analytics"])
async def get_trends(days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    """
    Get price trends over time
    """
    trends = analytics.get_price_trends(db, days=days)
    return {"trends": trends}


@app.get("/api/analytics/distribution", tags=["Analytics"])
async def get_distribution(db: Session = Depends(get_db)):
    """
    Get distribution metrics (bedrooms, status, city)
    """
    return {
        "bedroom_distribution": analytics.get_bedroom_distribution(db),
        "status_distribution": analytics.get_status_distribution(db),
        "city_distribution": analytics.get_city_distribution(db)
    }


@app.get("/api/analytics/performance", tags=["Analytics"])
async def get_performance_metrics(db: Session = Depends(get_db)):
    """
    Get key performance indicators (KPIs)
    """
    return analytics.get_performance_metrics(db)


# ============================================================================
# Lead Scoring Endpoints
# ============================================================================

@app.get("/api/leads/score/{unit_id}", response_model=schemas.LeadScoreResponse, tags=["Lead Scoring"])
async def get_lead_score(unit_id: str, db: Session = Depends(get_db)):
    """
    Get calculated lead score for specific unit with breakdown
    """
    unit = crud.get_unit(db, unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    market_data = lead_scoring.get_market_data(db)
    score_breakdown = lead_scoring.calculate_score_breakdown(unit, market_data)

    return {
        "unit_id": unit_id,
        "lead_score": score_breakdown['total_score'],
        "score_breakdown": score_breakdown
    }


@app.get("/api/leads/prioritized", response_model=List[schemas.UnitResponse], tags=["Lead Scoring"])
async def get_prioritized_units(
    limit: int = Query(50, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get units sorted by lead score (highest priority first)

    **Use case:** Auto-prioritize which units to promote/market first
    """
    units = crud.get_units(
        db,
        limit=limit,
        status="available"
    )

    # Already sorted by lead_score desc in CRUD function
    return units


@app.post("/api/leads/recalculate", tags=["Lead Scoring"])
async def recalculate_all_scores(db: Session = Depends(get_db)):
    """
    Recalculate lead scores for all available units

    **Use case:** Run this periodically (e.g., daily cron job) to update scores
    as market conditions change
    """
    updated_count = lead_scoring.recalculate_all_scores(db)

    logger.info(f"Recalculated lead scores for {updated_count} units")

    return {
        "message": "Lead scores recalculated successfully",
        "updated_count": updated_count
    }


# ============================================================================
# Health Check Endpoints
# ============================================================================

@app.get("/health", tags=["System"])
async def health_check(db: Session = Depends(get_db)):
    """
    System health check endpoint
    """
    try:
        # Test database connection
        db.execute("SELECT 1")

        return {
            "status": "healthy",
            "database": "connected",
            "websocket_connections": manager.get_connection_count()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")
