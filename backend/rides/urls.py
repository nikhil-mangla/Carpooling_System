from django.urls import path
from .views import (
    RideListCreateView, RouteMatchView, RideRequestCreateView, 
    InitiateCallView, TwilioCallbackView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('rides/', RideListCreateView.as_view(), name='ride-list-create'),
    path('initiate-call/', InitiateCallView.as_view(), name='initiate-call'),
    path('twilio-callback/', TwilioCallbackView.as_view(), name='twilio-callback'),
    path('ride-requests/', RideRequestCreateView.as_view(), name='ride-requests'),
    path('route-match/', RouteMatchView.as_view(), name='route-match'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]