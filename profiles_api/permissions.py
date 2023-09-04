from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile"""

    # the way you define permission classes is you had a hasObject permissions function to the class, 
        # which gets called every time a request is made to the API that we assign our permission to
    # this function will return a TRUE or a FALSE to determine whether the authenticated user has the permissions to perform the change they're trying to make

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""

        # check the method the user is trying to perform, and then check it against the "Safe Methods List"
            # Method meaning get/put/patch/delete
            # Safe Methods are any methods that don't make changes to the object, like GET: you're just reading the object
        if request.method in permissions.SAFE_METHODS:
            return True # "allow this request"
        
        # Check whether the object the user is updating matches the authenticated user profile via their ID
            # Requests in Django are authenticated, so the ID is included with each and every request as a kind of "permission slip" or "key card"
        return obj.id == request.user.id
            # Returns TRUE if the ID's match, or FALSE if they don't

