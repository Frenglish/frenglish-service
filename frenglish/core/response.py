from django.http import JsonResponse, HttpResponseNotFound


def create_response(payload=None, error=None):
    return JsonResponse(
        {"response": payload if payload else "", "error": error if error else ""}
    )


def http_404():
    return HttpResponseNotFound()
