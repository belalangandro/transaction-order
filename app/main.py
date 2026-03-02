from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

### test
app = FastAPI(title="Transaction Order Service")

class OrderStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"

class TransactionOrder(BaseModel):
    id: Optional[int] = None
    customer_id: int
    product_name: str
    quantity: int = Field(..., gt=0)
    total_amount: float = Field(..., gt=0)
    status: OrderStatus = OrderStatus.pending

db_transaction_orders: List[TransactionOrder] = []

@app.get("/")
async def read_root():
    return {"message": "Transaction Order Service running"}

@app.post("/transaction-orders/", response_model=TransactionOrder)
async def create_transaction_order(transaction: TransactionOrder):
    transaction.id = len(db_transaction_orders) + 1
    db_transaction_orders.append(transaction)
    return transaction

@app.get("/transaction-orders/", response_model=List[TransactionOrder])
async def get_all_transaction_orders():
    return db_transaction_orders

@app.get("/transaction-orders/{order_id}", response_model=TransactionOrder)
async def get_transaction_order(order_id: int):
    for order in db_transaction_orders:
        if order.id == order_id:
            return order
    raise HTTPException(status_code=404, detail="Transaction order not found")

@app.put("/transaction-orders/{order_id}", response_model=TransactionOrder)
async def update_transaction_order(order_id: int, transaction: TransactionOrder):
    for idx, order in enumerate(db_transaction_orders):
        if order.id == order_id:
            transaction.id = order_id
            db_transaction_orders[idx] = transaction
            return transaction
    raise HTTPException(status_code=404, detail="Transaction order not found")

@app.delete("/transaction-orders/{order_id}")
async def delete_transaction_order(order_id: int):
    for idx, order in enumerate(db_transaction_orders):
        if order.id == order_id:
            db_transaction_orders.pop(idx)
            return {"message": f"Transaction order {order_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Transaction order not found")