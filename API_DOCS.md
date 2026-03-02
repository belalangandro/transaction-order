# Transaction Order API Documentation

## Overview
This API provides CRUD operations for managing transaction orders in the Transaction Order Service.

## Base URL
`http://localhost:8000` (when running locally)

## Endpoints

### GET /
Get a welcome message from the Transaction Order Service.

#### Response
```json
{
  "Hello": "Transaction Order Service"
}
```

### POST /transaction-orders/
Create a new transaction order.

#### Request Body
```json
{
  "customer_id": 1,
  "product_name": "Product Name",
  "quantity": 2,
  "total_amount": 99.99,
  "status": "pending"
}
```

#### Response
```json
{
  "id": 1,
  "customer_id": 1,
  "product_name": "Product Name",
  "quantity": 2,
  "total_amount": 99.99,
  "status": "pending"
}
```

### GET /transaction-orders/
Get all transaction orders.

#### Response
```json
[
  {
    "id": 1,
    "customer_id": 1,
    "product_name": "Product Name",
    "quantity": 2,
    "total_amount": 99.99,
    "status": "pending"
  }
]
```

### GET /transaction-orders/{order_id}
Get a specific transaction order by ID.

#### Path Parameters
- `order_id` (integer): The ID of the transaction order

#### Response
```json
{
  "id": 1,
  "customer_id": 1,
  "product_name": "Product Name",
  "quantity": 2,
  "total_amount": 99.99,
  "status": "pending"
}
```

### PUT /transaction-orders/{order_id}
Update a specific transaction order by ID.

#### Path Parameters
- `order_id` (integer): The ID of the transaction order

#### Request Body
```json
{
  "customer_id": 1,
  "product_name": "Updated Product Name",
  "quantity": 3,
  "total_amount": 149.99,
  "status": "completed"
}
```

#### Response
```json
{
  "id": 1,
  "customer_id": 1,
  "product_name": "Updated Product Name",
  "quantity": 3,
  "total_amount": 149.99,
  "status": "completed"
}
```

### DELETE /transaction-orders/{order_id}
Delete a specific transaction order by ID.

#### Path Parameters
- `order_id` (integer): The ID of the transaction order

#### Response
```json
{
  "message": "Transaction order 1 deleted successfully"
}
```

## Models

### TransactionOrder
| Field | Type | Description | Default |
|-------|------|-------------|---------|
| id | integer | Unique identifier for the transaction order | Auto-generated |
| customer_id | integer | ID of the customer associated with the order | Required |
| product_name | string | Name of the product ordered | Required |
| quantity | integer | Quantity of products ordered | Required |
| total_amount | float | Total amount for the order | Required |
| status | string | Status of the order (pending, processing, completed, cancelled) | "pending" |

## Running the Application

To run this application locally:

1. Make sure you have Python installed
2. Install the required dependencies:
   ```bash
   pip install fastapi uvicorn
   ```
3. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Visit `http://localhost:8000` to access the API
5. Visit `http://localhost:8000/docs` for interactive API documentation