"""
Custom middleware:
    - allow options requests on all endpoints;
    - set CORS options;
"""


def allow_options_requests_wrapper(get_response):
    # One-time configuration and initialization.

    def allow_options_requests(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        # add some cors headers
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST"
        response["Access-Control-Allow-Headers"] = "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range"

        # allow options requests on our endpoint
        if not response.streaming and response.status_code == 405 and request.method == "OPTIONS":
            response.status_code = 200
            response.content = ""

        return response

    return allow_options_requests
