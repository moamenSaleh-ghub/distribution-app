import json
from decimal import Decimal
from typing import Any, Dict, Optional


def decimal_default(obj):
    """JSON serializer for Decimal objects"""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def success_response(status_code: int, body: Any) -> Dict[str, Any]:
    """Create a successful API Gateway response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET,POST,PATCH,DELETE,OPTIONS'
        },
        'body': json.dumps(body, default=decimal_default)
    }


def error_response(status_code: int, message: str, code: Optional[str] = None) -> Dict[str, Any]:
    """Create an error API Gateway response"""
    error_body = {
        'message': message
    }
    if code:
        error_body['code'] = code
    
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET,POST,PATCH,DELETE,OPTIONS'
        },
        'body': json.dumps(error_body)
    }

