from rest_framework.response import Response


class BadgeAPIResponse(Response):
    def __init__(
        self,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
        schema=None,
        message=None,
    ):

        data = {
            "VERSION": 1,
            "message": message,
            "status": status,
            "payload": data,
        }

        super(BadgeAPIResponse, self).__init__(
            data, status, template_name, headers, exception, content_type
        )
