from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'mop', views.MeansOfPaymentViewSet, basename="mop")
router.register(r'user', views.UserViewSet, basename="user")
router.register(r'bank_account', views.BankAccountViewSet, basename="bankaccount")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.CustomAuthToken.as_view()),
]
