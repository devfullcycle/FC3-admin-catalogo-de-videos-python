
from core.__seedwork.domain.exceptions import EntityValidationException, NotFoundException
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from rest_framework.views import exception_handler as rest_framework_exception_handler


def handle_serializer_validation_error(exception: ValidationError, context):
    response = rest_framework_exception_handler(exception, context)
    response.status_code = 422
    return response


def handle_entity_validation_error(exception: EntityValidationException, context):
    return Response(exception.error, status=422)


def handle_not_found_error(exception: NotFoundException, context):
    return Response({'message': exception.args[0]}, status=404)


handlers = {
    ValidationError: handle_serializer_validation_error,
    EntityValidationException: handle_entity_validation_error,
    NotFoundException: handle_not_found_error,
}


def custom_exception_handler(exc, context):
    if handler := handlers.get(exc.__class__):
        return handler(exc, context)
    return rest_framework_exception_handler(exc, context)
