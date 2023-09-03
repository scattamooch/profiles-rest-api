from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status # list of HTTP status codes
from profiles_api import serializers

class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer # pulls from serializers.py

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            "Uses HTTP methods as function (get, post, patch, put, delete)",
            "Is similar to a traditional Django View",
            "Gives you the most control over your application logic",
            "Is mapped manually to URLS",
        ]

        return Response({"message": "Hello", "an_apiview": an_apiview})
    
    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data) # retrieves the serializer declared above and passes the POSTed data through it

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f"Hello {name}"

            return Response({"message": message})
        
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )
        
    def put(self, request, pk=None):          # updates(replaces) an entire object... pk=None takes the id of the object to be updated
        """Handle updating an object"""
        return Response({"method": "PUT"})
    
    def patch(self, request, pk=None):        # only updates the fields provided; not the whole object
        """Handle a partial update of an object"""
        return Response({"method": "PATCH"})
    
    def delete(self, request, pk=None):
        """Deletes an object"""
        return Response({"method": "DELETE"})