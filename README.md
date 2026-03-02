# Transaction Order Service

A FastAPI-based RESTful API service for managing transaction orders. This service provides full CRUD (Create, Read, Update, Delete) operations for handling customer transaction orders with support for tracking order status, quantities, and amounts.

## Features

- **RESTful API**: Clean and intuitive endpoints following REST conventions
- **CRUD Operations**: Full Create, Read, Update, and Delete functionality for transaction orders
- **FastAPI**: Built with FastAPI for high performance and automatic API documentation
- **Pydantic Models**: Strong typing and validation with Pydantic models
- **JSON Responses**: Consistent JSON response format

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn (ASGI server)

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:yudoeastern/transaction-order.git
   cd transaction-order
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate 
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To run the application locally:

```bash
uvicorn app.main:app --reload
```

The API will be accessible at `http://localhost:8000` and the interactive documentation at `http://localhost:8000/docs`.

## API Endpoints

### GET /
Get a welcome message from the Transaction Order Service.

### POST /transaction-orders/
Create a new transaction order with the following body:
```json
{
  "customer_id": 1,
  "product_name": "Product Name",
  "quantity": 2,
  "total_amount": 99.99,
  "status": "pending"
}
```

### GET /transaction-orders/
Retrieve all transaction orders.

### GET /transaction-orders/{order_id}
Retrieve a specific transaction order by ID.

### PUT /transaction-orders/{order_id}
Update a specific transaction order by ID with the same body format as POST.

### DELETE /transaction-orders/{order_id}
Delete a specific transaction order by ID.

## Data Model

### TransactionOrder
| Field | Type | Description | Default |
|-------|------|-------------|---------|
| id | integer | Unique identifier for the transaction order | Auto-generated |
| customer_id | integer | ID of the customer associated with the order | Required |
| product_name | string | Name of the product ordered | Required |
| quantity | integer | Quantity of products ordered | Required |
| total_amount | float | Total amount for the order | Required |
| status | string | Status of the order (pending, processing, completed, cancelled) | "pending" |

## Project Structure

```
transaction-order/
├── app/
│   └── main.py          # Main FastAPI application
├── scripts/
│   └── review.py        # Review script
├── API_DOCS.md          # Detailed API documentation
├── README.md            # This file
├── requirements.txt     # Python dependencies
└── .gitignore          # Git ignore rules
```

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions, please file an issue in the GitHub repository.