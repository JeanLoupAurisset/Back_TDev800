from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'metadata', views.MetaDataViewSet, basename="metadata")
router.register(r'photo', views.PhotoViewSet, basename="photo")
router.register(r'album', views.AlbumViewSet, basename="album")
router.register(r'user', views.UserViewSet, basename="user")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.CustomAuthToken.as_view()),
]
