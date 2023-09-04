from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles_api import views


# branches off from the urls.py in profiles_project
router = DefaultRouter()
router.register("hello-viewset", views.HelloViewSet, basename="hello-viewset")
router.register("profile", views.UserProfileViewSet) #doesn't need a basename because this view has a "queryset = ..."

urlpatterns = [
    path("hello-view/", views.HelloApiView.as_view()),
    path("", include(router.urls))
]