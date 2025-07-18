def is_htmx(request):
    return request.headers.get("HX-Request") == "true"
