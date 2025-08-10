from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

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
                wrapped_response = {
                    "success": True,
                    "status": response.status_code,
                    "message": "Success",
                    "data": response.data,
                    "meta": response.data.get("meta", {}) if isinstance(response.data, dict) else {},
                }
                response.data = wrapped_response

        return super().finalize_response(request, response, *args, **kwargs)
