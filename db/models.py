import datetime

from click import DateTime
from pydantic import BaseModel

# 📌 Order Model for Request Body
class OrderCreate(BaseModel):
    consignment_id : str
    order_id: str
    status: str
    statusOnSlug: str
    updated_at: datetime  # Make sure this field is of type datetime

    class Config:
        arbitrary_types_allowed = True  # This will allow datetime objects to be used
