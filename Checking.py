# from services.auth import login, ACCESS_TOKEN
# import requests
# from fastapi import APIRouter, HTTPException
# from services.tracking import fetch_tracking_status
#
#
# app = APIRouter()
#
# @app.get("/track/{consignment_id}")
# def track_order(consignment_id: str):
#     """Fetch tracking details from Pathao API and store in the database."""
#     print(f"Tracking ID: {consignment_id}")
#
#     tracking_data = fetch_tracking_status(consignment_id)
#     if tracking_data is None:
#         raise HTTPException(status_code=404, detail="Tracking data not found")
#
#     return consignment_id
#
#
#
import pandas as pd
def FindingLlistofConsID(filepath):
    file = pd.read_csv(filepath)
    return file['Order consignment id'].tolist()


file = pd.read_csv('deliveries_2025-02-04.csv')
print(file.columns)
print(len(file['Order consignment id']))