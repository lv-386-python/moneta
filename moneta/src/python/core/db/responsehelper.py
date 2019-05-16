"""
Module that provides various HttResponse objects for project.
"""

from django.http import HttpResponse

# status code 2xx
RESPONSE_200_OK = HttpResponse('Operation was successful provided', status=200)
RESPONSE_200_UPDATED = HttpResponse('Object was successfully updated', status=200)
RESPONSE_200_DELETED = HttpResponse('Object was successfully deleted', status=200)
RESPONSE_200_ACTIVATED = HttpResponse('User was successfully activated', status=200)
RESPONSE_201_CREATED = HttpResponse('Object was successfully created', status=201)

# status code 4xx
RESPONSE_400_EMPTY_JSON = HttpResponse('Empty json received', status=400)
RESPONSE_400_INVALID_DATA = HttpResponse('Received data is not valid', status=400)
RESPONSE_400_INVALID_EMAIL = HttpResponse('Received email is not valid', status=400)
RESPONSE_400_INVALID_EMAIL_OR_PASSWORD = HttpResponse('Email or password is not valid', status=400)
RESPONSE_400_EXISTED_EMAIL = HttpResponse('Received email is already exist', status=400)
RESPONSE_400_INVALID_PASSWORD = HttpResponse('Received password is not valid', status=400)
RESPONSE_400_INVALID_HTTP_METHOD = HttpResponse('Invalid HTTP method', status=400)
RESPONSE_400_DB_OPERATION_FAILED = HttpResponse('Database operation is failed', status=400)
RESPONSE_403_ACCESS_DENIED = HttpResponse('Access denied', status=403)
RESPONSE_403_USER_NOT_ACTIVE = HttpResponse('User has not active status', status=403)
RESPONSE_403_USER_NOT_AUTHENTICATED = HttpResponse('User is not authenticated', status=403)
RESPONSE_404_OBJECT_NOT_FOUND = HttpResponse('Object not found', status=404)
RESPONSE_498_INVALID_TOKEN = HttpResponse('Invalid or expired token', status=498)
