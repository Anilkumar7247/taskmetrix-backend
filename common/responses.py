from rest_framework.response import Response
from rest_framework import status


def error_response(message, code=status.HTTP_400_BAD_REQUEST):
    return Response(
        {
            "success": False,
            "error": message
        },
        status=code
    )


def success_response(data=None, message="Success"):
    return Response(
        {
            "success": True,
            "message": message,
            "data": data
        },
        status=status.HTTP_200_OK
    )