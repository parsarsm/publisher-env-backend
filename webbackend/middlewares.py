from django.http import HttpResponse


def cors_middleware(get_response):
    def middleware(request):
        if request.method == 'OPTIONS':
            response = HttpResponse()
        else:
            response = get_response(request)

        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        response["Access-Control-Allow-Methods"] = "*"
        return response

    return middleware
