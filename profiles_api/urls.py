from django.urls import path
from profiles_api import views


# branches off from the urls.py in profiles_project
urlpatterns = [
    path("hello-view/", views.HelloApiView.as_view())
]