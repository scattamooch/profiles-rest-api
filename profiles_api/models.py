from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# base user class with built in fields: username, password, last_login, etc

from django.contrib.auth.models import PermissionsMixin
# base user class with built in permissions depending on field: is_staff, is_superuser, etc
    # think of it as a "higher" level of logging in, like an admin

from django.contrib.auth.models import BaseUserManager
# base user class that handles actual user creation, in tandem with the UserProfile class


# Create your models here.
class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    # Django requires passwords to be a hash, so setting password=None is an automatic validation. A password cannot be none

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email) #sets anything after the @ in an email to .lower()
        user = self.model(email=email, name=name) #creates a user object with username(email) and name and then password vvv below
        user.set_password(password) #built in encryption function --> converts password to hash
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    # ^^^ python standard for writing docstrings. Describe what class/function does for yourself and/or future developers
    
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True) 
    # determine whether or not a user is active... this does NOT mean logged in. It determines whether or not they can log in at all. Set false to DEACTIVATE an account without deleting it
    
    is_staff = models.BooleanField(default=False) 
    # determines whether or not the user is a "staff"... should they have access to admin permissions?
    # staff have minor admin privileges, superusers have complete and total access+control

    objects = UserProfileManager()

    USERNAME_FIELD = "email" #Django looks for a username by default, this field tells Django we're auth'ing via email, not username
    REQUIRED_FIELDS = ["name"]

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name
    
    # we have no short name specified above, so we return the full name. But think of this as a field that would return a nickname or 
    # just the first name if first/last were both specified in the class above
    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name
    
    def __str__(self):
        """Return string represetnation of user"""
        return self.email