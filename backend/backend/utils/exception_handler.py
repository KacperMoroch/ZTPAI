from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status as drf_status
from rest_framework.exceptions import AuthenticationFailed

def custom_exception_handler(exc, context):

    # Obsługuje specjalnie AuthenticationFailed i zmienia jego komunikat
    if isinstance(exc, AuthenticationFailed): 
        return Response(
            {
                "error": "Nieprawidłowe dane logowania!",
                "status": drf_status.HTTP_401_UNAUTHORIZED
            },
            status=drf_status.HTTP_401_UNAUTHORIZED
        )


    # Najpierw wywołujemy domyślny handler DRF
    response = drf_exception_handler(exc, context)

    # Jeżeli DRF sam już coś wygenerował, dopasuj do naszego formatu
    if response is not None:
        detail = response.data.get("detail", None)
        error_message = detail if detail else response.data
        return Response(
            {
                "error": error_message,
                "status": response.status_code
            },
            status=response.status_code
        )
    
    # Obsługa niespodziewanych wyjątków
    return Response(
        {
            "error": "Wewnętrzny błąd serwera!",
            "status": drf_status.HTTP_500_INTERNAL_SERVER_ERROR
        },
        status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR
    )
