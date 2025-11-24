import json
from src.db.product_repo import create_product, compute_effective_price
from src.utils.response import success_response, error_response


def handler(event, context):
    """Create a new product"""
    try:
        body = json.loads(event.get('body', '{}'))
        
        # Validate required fields
        name = body.get('name')
        base_buying_price = body.get('baseBuyingPrice')
        base_selling_price = body.get('baseSellingPrice')
        
        if not name:
            return error_response(400, 'name is required', 'MISSING_FIELD')
        if base_buying_price is None:
            return error_response(400, 'baseBuyingPrice is required', 'MISSING_FIELD')
        if base_selling_price is None:
            return error_response(400, 'baseSellingPrice is required', 'MISSING_FIELD')
        
        # Validate numeric fields
        try:
            base_buying_price = float(base_buying_price)
            base_selling_price = float(base_selling_price)
        except (ValueError, TypeError):
            return error_response(400, 'Prices must be valid numbers', 'INVALID_INPUT')
        
        if base_buying_price < 0 or base_selling_price < 0:
            return error_response(400, 'Prices must be non-negative', 'INVALID_INPUT')
        
        discount_percent = body.get('discountPercent')
        if discount_percent is not None:
            try:
                discount_percent = float(discount_percent)
                if discount_percent < 0 or discount_percent > 100:
                    return error_response(400, 'discountPercent must be between 0 and 100', 'INVALID_INPUT')
            except (ValueError, TypeError):
                return error_response(400, 'discountPercent must be a valid number', 'INVALID_INPUT')
        
        image_key = body.get('imageKey')
        is_active = body.get('isActive', True)
        
        # Create product
        product = create_product(
            name=name,
            base_buying_price=base_buying_price,
            base_selling_price=base_selling_price,
            discount_percent=discount_percent,
            image_key=image_key,
            is_active=is_active
        )
        
        # Add computed effective prices (convert Decimal to float for computation)
        from decimal import Decimal
        base_buying = float(product['baseBuyingPrice']) if isinstance(product['baseBuyingPrice'], Decimal) else product['baseBuyingPrice']
        base_selling = float(product['baseSellingPrice']) if isinstance(product['baseSellingPrice'], Decimal) else product['baseSellingPrice']
        discount = float(product.get('discountPercent', 0)) if isinstance(product.get('discountPercent', 0), Decimal) else product.get('discountPercent', 0)
        
        product['effectiveBuyingPrice'] = compute_effective_price(base_buying, discount)
        product['effectiveSellingPrice'] = compute_effective_price(base_selling, discount)
        
        return success_response(201, product)
    
    except json.JSONDecodeError:
        return error_response(400, 'Invalid JSON in request body', 'INVALID_JSON')
    except Exception as e:
        return error_response(500, f'Internal server error: {str(e)}', 'INTERNAL_ERROR')

