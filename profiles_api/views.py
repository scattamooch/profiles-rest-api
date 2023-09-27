from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status # list of HTTP status codes
from profiles_api import serializers
from rest_framework import viewsets
from profiles_api import models
from rest_framework.authentication import TokenAuthentication
from profiles_api import permissions
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

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
        
    def put(self, request, pk=None):          # updates(replaces) an entire object... pk=None takes the id of the object to be updated (P rimary K ey)
        """Handle updating an object"""
        return Response({"method": "PUT"})
    
    def patch(self, request, pk=None):        # only updates the fields provided; not the whole object
        """Handle a partial update of an object"""
        return Response({"method": "PATCH"})
    
    def delete(self, request, pk=None):
        """Deletes an object"""
        return Response({"method": "DELETE"})
    
class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer
    
    def list(self, request):
        """Return a hello message"""
        a_viewset = [
            "Uses actions (list, create, retrieve, update, partial_update)",
            "Automatically maps to URLs using Routers",
            "Provides more functionality with less code",
        ]

        return Response({"message": "Hello", "a_viewset": a_viewset})
    
    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f"Hello {name}"

            return Response({"message": message})
        
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
        
    # These map to corresponding CRUD methods, they apply to objects, or instances of a model or models 
    # Traditional CRUD requires more code, and allows for finer, more control
    # These methods are more or less "out of the box", almost built in... they can be implemented quickly for rapid RESTful operations
    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({"http_method": "GET"})
    
    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({"http_method": "PUT"})
    
    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({"http_method": "PATCH"})
    
    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({"http_method": "DELETE"})
    
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()         # applies ALL of the "standard" functions to the model viewset via .all() --> Create, List, Update, Partial Update, and Destroy

    authentication_classes = (TokenAuthentication, )        # set how the user will authenticate (the mechanism they will use)
    # generates a random token on login, specific to the user, that gets set with every request they make

    permission_classes = (permissions.UpdateOwnProfile, )    # how the user gets permission to do certain things
    # controls the finer grain permissions for a user

    # works by adding a whole GET request thats manipulatable via plain text
    filter_backends = (filters.SearchFilter, )
    search_fields = ("name", "email", )
    # performs a GET request conditional to the NAME or EMAIL entered into the search bar OR the url bar (after the "/?search=")

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading, and updating profile feed items"""
    authentication_classes = (TokenAuthentication, )
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus,IsAuthenticated, )

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
        # when a new object is created, it passes in the serializer that we used to create the object
        # the save function in the model serializer saves the content to the object in the database
        # we pass user_profile = self.request.user to auth the user via token. if the user is not auth'd, the post is made anonymously