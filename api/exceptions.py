from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None and isinstance(exc, ValidationError) and response.status_code == 400:
        response.status_code = 422
    return response
