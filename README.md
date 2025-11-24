# Distribution App

A cost-optimized web application for managing products, customers, orders, and customer debt tracking.

## Architecture

- **Backend**: AWS Lambda functions (Python 3.12)
- **Frontend**: React SPA (Vite)
- **Database**: DynamoDB (single table design)
- **API**: API Gateway HTTP API
- **Storage**: S3 for product images
- **Infrastructure**: Terraform

## Project Structure

```
distribution-app/
├── infra/           # Terraform infrastructure
├── backend/         # Lambda functions
│   └── src/
│       ├── handlers/    # Lambda handlers
│       ├── db/          # DynamoDB repositories
│       └── utils/       # Utilities
└── frontend/        # React application
    └── src/
        ├── pages/       # Page components
        ├── components/  # Reusable components
        └── api/         # API client
```

## Setup

### Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform >= 1.10.0
- Node.js 18+ (for frontend build)
- Python 3.12 (for backend)
- pip or pip3 (for Python dependencies)

### Infrastructure Setup

1. Navigate to the infra directory:
```bash
cd infra
```

2. Initialize Terraform:
```bash
terraform init
```

3. Review the plan:
```bash
terraform plan
```

4. Apply the infrastructure:
```bash
terraform apply
```

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Package Lambda functions:
```bash
# Make the deployment script executable
chmod +x deploy.sh

# Run the deployment script to create zip files
./deploy.sh
```

This will create zip files in the `deploy/` directory for each Lambda function. These zip files are referenced by Terraform when deploying the infrastructure.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set the API URL:
```bash
# Create .env file with your API Gateway URL
# Get the URL from Terraform outputs: cd infra && terraform output api_gateway_url
echo "VITE_API_URL=https://your-api-gateway-url" > .env
```

4. Development mode (optional):
```bash
npm run dev
```

5. Build for production:
```bash
npm run build
```

This creates production-ready files in `frontend/dist/` that can be deployed to any static hosting service.

## Deployment

### Infrastructure Deployment

The infrastructure is already deployed. To redeploy or update:

```bash
cd infra
terraform plan
terraform apply
```

Get the API Gateway URL:
```bash
cd infra
terraform output api_gateway_url
```

### Frontend Deployment

After building the frontend (`npm run build`), deploy the `frontend/dist/` directory to:

- **AWS S3 + CloudFront** (recommended for AWS integration)
- **Netlify**: `netlify deploy --prod --dir=dist`
- **Vercel**: `vercel --prod`
- **Any static hosting service**

## Current Deployment Status

✅ **Infrastructure**: Deployed and running
- API Gateway: `https://jyn96fs7n5.execute-api.eu-central-1.amazonaws.com`
- DynamoDB: `distribution-app-dev`
- S3 Bucket: `distribution-app-product-images-dev`
- All Lambda functions: Deployed

✅ **Backend**: Complete and deployed
- All 10 Lambda functions packaged and deployed
- API endpoints configured and working

✅ **Frontend**: Built and ready for deployment
- Production build available in `frontend/dist/`
- Configured to use deployed API Gateway

⏳ **Remaining**: Deploy frontend to hosting service

## API Endpoints

### Products
- `POST /products` - Create product
- `GET /products` - List products
- `GET /products/{id}` - Get product
- `PATCH /products/{id}` - Update product

### Customers
- `POST /customers` - Create customer
- `GET /customers` - List customers
- `GET /customers/{id}` - Get customer detail

### Orders
- `POST /orders` - Create order
- `GET /customers/{id}/orders` - Get customer orders

### Debt Adjustments
- `POST /customers/{id}/adjust-debt` - Adjust customer debt

## Data Model

### Product
- id, name, baseBuyingPrice, baseSellingPrice, discountPercent, imageKey, isActive

### Customer
- id, name, location, phone, email, totalDebt, notes, isActive

### Order
- id, customerId, orderDate, items[], subtotal, discount, totalAmount, paidNow, debtChange

### Debt Adjustment
- id, customerId, timestamp, amount, reason

## DynamoDB Design

Single table design with composite keys:
- Partition Key: `pk` (e.g., `PRODUCT#<id>`, `CUSTOMER#<id>`)
- Sort Key: `sk` (e.g., `META`, `ORDER#<timestamp>`, `DEBT#<timestamp>`)

## Cost Optimization

- DynamoDB: PAY_PER_REQUEST billing mode
- Lambda: Pay per invocation
- S3: Pay per storage and requests
- API Gateway: Pay per API call

Designed for minimal traffic (single user, <100 customers).

## License

MIT

