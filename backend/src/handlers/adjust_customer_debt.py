import json
from src.db.debt_repo import create_debt_adjustment
from src.db.customer_repo import get_customer
from src.utils.response import success_response, error_response


def handler(event, context):
    """Create a debt adjustment for a customer"""
    try:
        customer_id = event.get('pathParameters', {}).get('id')
        
        if not customer_id:
            return error_response(400, 'Customer ID is required', 'MISSING_PARAMETER')
        
        # Verify customer exists
        customer = get_customer(customer_id)
        if not customer:
            return error_response(404, f'Customer {customer_id} not found', 'NOT_FOUND')
        
        body = json.loads(event.get('body', '{}'))
        
        # Validate required fields
        amount = body.get('amount')
        reason = body.get('reason')
        
        if amount is None:
            return error_response(400, 'amount is required', 'MISSING_FIELD')
        if not reason:
            return error_response(400, 'reason is required', 'MISSING_FIELD')
        
        # Validate amount
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            return error_response(400, 'amount must be a valid number', 'INVALID_INPUT')
        
        # Create adjustment
        adjustment = create_debt_adjustment(
            customer_id=customer_id,
            amount=amount,
            reason=reason
        )
        
        # Get updated customer to get new totalDebt
        updated_customer = get_customer(customer_id)
        new_total_debt = updated_customer.get('totalDebt', 0) if updated_customer else 0
        
        return success_response(201, {
            **adjustment,
            'newTotalDebt': new_total_debt
        })
    
    except json.JSONDecodeError:
        return error_response(400, 'Invalid JSON in request body', 'INVALID_JSON')
    except Exception as e:
        return error_response(500, f'Internal server error: {str(e)}', 'INTERNAL_ERROR')

