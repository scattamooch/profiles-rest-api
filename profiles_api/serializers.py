from rest_framework import serializers
from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        # which model is being serialized?
        model = models.UserProfile

        # which fields are being validated?
        fields = ("id", "email", "name", "password")

        # make the password write only, and style it, so that it remains protected as a hash
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"}
            }
        }

    # "overwrite" the previously written create function to validate data + generate password hash instead of plain text password
    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email = validated_data["email"],
            name = validated_data["name"],
            password = validated_data["password"],
        )

        return user
    
    # prevents updated passwords being stored as plain text
    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
 
        return super().update(instance, validated_data)

