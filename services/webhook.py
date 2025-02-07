from fastapi import APIRouter, Request, HTTPException, Header
from db.database import get_db_connection
import datetime
import json

router = APIRouter()

# ✅ Pathao Webhook Secret
PATHAO_WEBHOOK_SECRET = "f3992ecc-59da-4cbe-a049-a13da2018d51"


@router.post("/webhook/pathao")
async def pathao_webhook(
        request: Request,
        x_pathao_merchant_webhook_integration_secret: str = Header(None)
):
    print("Received request!")
    print(f"Secret: {x_pathao_merchant_webhook_integration_secret}")
    """
    Webhook to receive order status updates from Pathao.
    """

    # ✅ Verify Webhook Secret
    print('Mahin')
    if x_pathao_merchant_webhook_integration_secret != PATHAO_WEBHOOK_SECRET:
        print(f"Expected Secret: {PATHAO_WEBHOOK_SECRET}, Received Secret: {x_pathao_merchant_webhook_integration_secret}")
        raise HTTPException(status_code=403, detail="Invalid webhook secret")

    # ✅ Parse JSON Payload
    try:
        payload = await request.json()
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON format")

    print("📩 Received Pathao Webhook:", json.dumps(payload, indent=4))

    # ✅ Extract Required Fields
    consignment_id = payload.get("consignment_id")
    order_id = payload.get("merchant_order_id")
    status = payload.get("event")
    updated_at = payload.get("updated_at")

    if not (consignment_id and order_id and status and updated_at):
        missing_fields = [field for field in ["consignment_id", "merchant_order_id", "event", "updated_at"] if not payload.get(field)]
        print(f"Missing fields: {missing_fields}")
        raise HTTPException(status_code=400, detail="Missing required fields")

    # ✅ Convert updated_at to datetime
    try:
        updated_at = datetime.datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        print(f"Error converting updated_at: {e}")
        raise HTTPException(status_code=400, detail="Invalid date format")

    # ✅ Store/Update Order in Database
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                MERGE INTO Orders AS target
                USING (VALUES (?, ?, ?, ?, ?)) AS source (consignment_id, order_id, status, status_on_slug, time)
                ON target.consignment_id = source.consignment_id
                WHEN MATCHED THEN
                    UPDATE SET 
                        target.order_id = source.order_id,
                        target.status = source.status,
                        target.status_on_slug = source.status,
                        target.time = source.time
                WHEN NOT MATCHED THEN
                    INSERT (consignment_id, order_id, status, status_on_slug, time)
                    VALUES (source.consignment_id, source.order_id, source.status, source.status, source.time);
            """, (consignment_id, order_id, status, status, updated_at))

            conn.commit()
            print(f"✅ Order {order_id} updated successfully.")
        except Exception as e:
            print(f"❌ Database error: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {e}")
        finally:
            conn.close()

    # ✅ Return status code 202 (Accepted)
    return {"success": True, "message": "Order status updated successfully"}
