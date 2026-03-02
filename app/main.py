from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Transaction Order Service")

# Model untuk Transaction Order 
class TransactionOrder(BaseModel):
    id: Optional[int] = None
    customer_id: int
    product_name: str
    quantity: int
    total_amount: float
    status: str = "pending"

# Simulasi database sederhana dengan list
db_transaction_orders: List[TransactionOrder] = []

@app.get("/")
async def read_root():
    return {"Hello": "Transaction Order Service"} 

@app.post("/transaction-orders/")
async def create_transaction_order(transaction: TransactionOrder):
    # Generate ID otomatis.
    transaction.id = len(db_transaction_orders) + 1
    db_transaction_orders.append(transaction)
    return transaction

@app.get("/transaction-orders/")
async def get_all_transaction_orders():
    return db_transaction_orders

@app.get("/transaction-orders/{order_id}")
async def get_transaction_order(order_id: int):
    for order in db_transaction_orders:
        if order.id == order_id:
            return order
    return {"error": "Transaction order not found"}

@app.put("/transaction-orders/{order_id}")
async def update_transaction_order(order_id: int, transaction: TransactionOrder):
    for idx, order in enumerate(db_transaction_orders):
        if order.id == order_id:
            transaction.id = order_id  # Pastikan ID tetap sama
            db_transaction_orders[idx] = transaction
            return transaction
    return {"error": "Transaction order not found"}

@app.delete("/transaction-orders/{order_id}")
async def delete_transaction_order(order_id: int):
    for idx, order in enumerate(db_transaction_orders):
        if order.id == order_id:
            deleted_order = db_transaction_orders.pop(idx)
            return {"message": f"Transaction order {deleted_order.id} deleted successfully"}
    return {"error": "Transaction order not found"}
