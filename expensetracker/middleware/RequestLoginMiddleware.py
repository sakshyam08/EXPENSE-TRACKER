class RequestLoginMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request) ->any :
        request_info =request 
        print(request_info)
        print('Helo from Middleware')
        print(self.get_response(request))

        return self.get_response(request)


