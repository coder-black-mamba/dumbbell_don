from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from core.utils.api_response import error_response
class BaseModelViewSet(ModelViewSet):
    """
    Base ModelViewSet to automatically wrap all successful responses
    with a consistent API response format.
    """

    def finalize_response(self, request, response, *args, **kwargs):
        if hasattr(response, "data") and isinstance(response.data, dict):
            # Skip wrapping if explicitly an error
            if response.data.get("success") is False:
                return super().finalize_response(request, response, *args, **kwargs)

            # Wrap only if not already in the desired format
            if not all(key in response.data for key in ("success", "status", "message", "data")):
                # check the status code and send error response
                if response.status_code >= 400:
                    wrapped_response = {
                        "success": False,
                        "status": response.status_code,
                        "message": f"Error - {response.data.get('detail', 'Something went wrong')}",
                        "data": response.data,
                        "meta": response.data.get("meta", {}) if isinstance(response.data, dict) else {},
                    }
                    response.data = wrapped_response
                
                else:   
                    wrapped_response = {    
                        "success": True,
                        "status": response.status_code,
                        "message": "Success",
                        "data": response.data,
                        "meta": response.data.get("meta", {}) if isinstance(response.data, dict) else {},
                    }
                    response.data = wrapped_response

        return super().finalize_response(request, response, *args, **kwargs)
