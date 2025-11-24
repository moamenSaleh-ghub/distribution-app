#!/bin/bash
# Script to package Lambda functions for deployment

set -e

cd "$(dirname "$0")"
mkdir -p deploy

# Install dependencies (use pip3 if pip is not available)
if command -v pip3 &> /dev/null; then
    PIP_CMD=pip3
elif command -v pip &> /dev/null; then
    PIP_CMD=pip
else
    echo "Error: pip or pip3 not found"
    exit 1
fi

$PIP_CMD install -r requirements.txt -t src/

# Package each Lambda function
LAMBDA_FUNCTIONS=(
  "create_product"
  "get_products"
  "get_product"
  "update_product"
  "create_customer"
  "get_customers"
  "get_customer_detail"
  "create_order"
  "get_customer_orders"
  "adjust_customer_debt"
)

for func in "${LAMBDA_FUNCTIONS[@]}"; do
  echo "Packaging $func..."
  cd src
  zip -r "../deploy/${func}.zip" . -x "*.pyc" -x "__pycache__/*" -x "*/__pycache__/*"
  cd ..
done

echo "All Lambda functions packaged successfully!"

