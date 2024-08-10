from django.urls import path

from accounts.apis.authentication import AuthViewSet, LoginViewSet, RegisterViewSet

urlpatterns = [
    path("", AuthViewSet.as_view({'post': 'create'}), name="auth"),
    path("register/verify/", RegisterViewSet.as_view({'post': 'verify'}), name="register"),
    path("register/information/", RegisterViewSet.as_view({'post': 'information'}), name="register-information"),
    path("register/complete/", RegisterViewSet.as_view({'post': 'complete'}), name="register-complete"),
    path("login/", LoginViewSet.as_view({'post': 'create'}), name="login"),
]
