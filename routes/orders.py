from fastapi import APIRouter, HTTPException
from uvicorn.loops import asyncio
from services.tracking import fetch_tracking_status
from db.database import get_db_connection
from db.models import OrderCreate

router = APIRouter()


@router.get("/track/{consignment_id}")
def track_order(consignment_id: str):
    """Fetch tracking details from Pathao API and store in the database."""
    print(f"Tracking ID: {consignment_id}")

    tracking_data = fetch_tracking_status(consignment_id)

    if not tracking_data:
        raise HTTPException(status_code=404, detail="Tracking data not found")
    return tracking_data


@router.post("/add_order")
def add_order(order: OrderCreate):
    """Manually add an order to the database."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Orders (consignment_id, order_id, status, status_on_slug, time)
                       VALUES (?, ?, ?, ?, ?)
        """, (
            order.consignment_id, order.order_id, order.status,
            order.status_on_slug, order.time
        ))
        conn.commit()
        conn.close()
        return {"success": True, "message": "Order added successfully"}
    else:
        raise HTTPException(status_code=500, detail="Database connection failed")
