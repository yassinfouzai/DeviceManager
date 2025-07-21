def htmx_flag(request):
    return {
        'is_htmx': request.headers.get('HX-Request') == 'true'
    }
