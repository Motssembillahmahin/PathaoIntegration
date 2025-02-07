from fastapi import FastAPI
from routes import orders
from services.webhook import router as webhook_router  # ✅ Import Webhook Router

app = FastAPI()

# ✅ Register API Routes
app.include_router(orders.router, prefix="/api", tags=["Orders"])
app.include_router(webhook_router, prefix="/api", tags=["Webhook"])  # ✅ Register Webhook

# ✅ Run Database Setup on Startup
from db.database import setup_db
setup_db()

@app.get("/")
def root():
    return {"message": "Welcome to Pathao Order Tracking API"}
