from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status


class CustomAPIException(APIException):
    """Custom API exception with code"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'An error occurred.'
    default_code = 'error'

    def __init__(self, detail=None, code=None, status_code=None):
        if status_code:
            self.status_code = status_code
        if detail is not None:
            self.detail = {'code': code or self.default_code, 'detail': detail}
        else:
            self.detail = {'code': self.default_code, 'detail': self.default_detail}


def custom_exception_handler(exc, context):
    """Custom exception handler for consistent API response format"""
    response = exception_handler(exc, context)
    
    if response is not None:
        # Transform response to consistent format
        code = 'error'
        if hasattr(exc, 'default_code'):
            code = exc.default_code
        elif hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict):
                code = exc.detail.get('code', 'error')
        
        custom_response = {
            'code': code,
            'msg': str(exc.detail) if isinstance(exc.detail, str) else response.data.get('detail', str(exc.detail)),
            'data': response.data if isinstance(response.data, dict) else {}
        }
        response.data = custom_response
    
    return response
