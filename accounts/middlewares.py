import logging


class CrossOriginOpenerPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
        logging.info("Cross-Origin-Opener-Policy header set")
        return response
