from django.http import JsonResponse


def handler404_req(request, exception):
    message = ("Route Not Found")
    response = JsonResponse(data={'error': message})
    response.status_code = 404
    return response


def handler500_req(request):
    message = ("Internal Server Error")
    response = JsonResponse(data={'error': message})
    response.status_code = 500
    return response
