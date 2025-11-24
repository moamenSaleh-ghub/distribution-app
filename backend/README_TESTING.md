# Backend Testing Guide

## Setup

Install test dependencies:

```bash
cd backend
pip install -r requirements.txt
```

## Running Tests

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_product_repo.py
```

Run specific test:
```bash
pytest tests/test_product_repo.py::TestProductRepo::test_create_product
```

Verbose output:
```bash
pytest -v
```

## Test Structure

- `tests/conftest.py` - Shared fixtures (mock DynamoDB table, sample data)
- `tests/test_product_repo.py` - Product repository tests
- `tests/test_customer_repo.py` - Customer repository tests
- `tests/test_order_repo.py` - Order repository tests
- `tests/test_debt_repo.py` - Debt adjustment repository tests
- `tests/test_handlers.py` - Lambda handler tests
- `tests/test_utils.py` - Utility function tests

## Test Coverage

Tests cover:
- ✅ All repository functions (CRUD operations)
- ✅ All Lambda handlers (request/response handling)
- ✅ Error handling and validation
- ✅ Edge cases (missing data, invalid input)
- ✅ Business logic (price calculations, debt updates)

## Mocking

Tests use `moto` to mock AWS DynamoDB, so no real AWS resources are used during testing.

