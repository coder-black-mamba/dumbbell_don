from rest_framework.views import APIView
from rest_framework.response import Response

class BASEApiView(APIView):
    """
    Base API view to automatically wrap all successful responses
    with a consistent API response format.
    """

    def finalize_response(self, request, response, *args, **kwargs):
        # check if response is a dict
        if hasattr(response, "data") and isinstance(response.data, dict):
            # checking if error then ir will be handeld by our custom exception handler
            if response.data.get("success") is False:
                return super().finalize_response(request, response, *args, **kwargs)

            if not all(i in response.data for i in ("success", "status", "message", "data")):
                wrapped_response = {
                    "success": True,
                    "status": response.status_code,
                    "message": "Success",
                    "data": response.data,
                    "meta": response.data.get("meta", {}),
                }
                response.data = wrapped_response
        return super().finalize_response(request, response, *args, **kwargs)

        

               

           