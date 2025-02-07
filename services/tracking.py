import requests
from services.auth import login, ACCESS_TOKEN
from db.database import get_db_connection
from  Checking import FindingLlistofConsID
import pandas as pd

# 📌 Pathao API Configuration
BASE_URL = "https://api-hermes.pathao.com"
TRACKING_ENDPOINT = "/aladdin/api/v1/orders/{}/info"

def fetch_tracking_status(consignment_id, retry=False):
    """Fetches tracking status via Pathao API and stores in database."""
    global ACCESS_TOKEN

    if ACCESS_TOKEN is None:
        login()

    tracking_url = f"{BASE_URL}{TRACKING_ENDPOINT.format(consignment_id)}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }

    response = requests.get(tracking_url, headers=headers)

    if response.status_code == 200:
        tracking_data = response.json()
        store_tracking_data(consignment_id, tracking_data)
        print(f'Con ID: {tracking_data["data"]["consignment_id"]}')
        print(f'Order ID: {tracking_data["data"]["merchant_order_id"]}')
        print(f'Status: {tracking_data["data"]["order_status"]}')
        print(f'Status 2: {tracking_data["data"]["order_status_slug"]}')
        print(f'Time: {tracking_data["data"]["updated_at"]}')
        print(tracking_data)

        return {"success": True, "order_id": consignment_id, "tracking_details": tracking_data}


    elif response.status_code == 401:
        print("🔄 Token expired. Logging in again...")
        login()
        return fetch_tracking_status(consignment_id)

    else:
        print(f"❌ Failed to fetch tracking details: {response.text}")
        return None

def store_tracking_data(consignment_id, tracking_data):
    """Stores tracking information in SQL Server database."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Use SQL Server's MERGE statement for upsert
            cursor.execute("""
                MERGE INTO Orders AS target
                USING (VALUES (?, ?, ?, ?, ?)) AS source (consignment_id, order_id, status, status_on_slug, time)
                ON target.consignment_id = source.consignment_id
                WHEN MATCHED THEN
                    UPDATE SET
                        target.order_id = source.order_id,
                        target.status = source.status,
                        target.status_on_slug = source.status_on_slug,
                        target.time = source.time
                WHEN NOT MATCHED THEN
                    INSERT (consignment_id, order_id, status, status_on_slug, time)
                    VALUES (source.consignment_id, source.order_id, source.status, source.status_on_slug, source.time);
            """, (
                consignment_id,
                tracking_data['data']['merchant_order_id'],
                tracking_data['data']['order_status'],
                tracking_data['data']['order_status_slug'],
                tracking_data['data']['updated_at']
            ))
            conn.commit()
            print("✅ Order stored in database.")
        except Exception as e:
            print(f"❌ Error storing tracking data: {e}")
        finally:
            conn.close()


# # fetch_tracking_status('DG270125BAU47Z')
# value = FindingLlistofConsID('Test_del.csv')
# for val in value:
#     fetch_tracking_status(val)
