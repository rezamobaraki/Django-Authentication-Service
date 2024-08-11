from rest_framework.routers import SimpleRouter

from accounts.apis.authentication import AuthenticationViewSet, LoginViewSet, RegistrationViewSet

app_name = 'authentication'
router = SimpleRouter()

router.register(r'', AuthenticationViewSet, basename='authentication')
router.register(r'register', RegistrationViewSet, basename='registration')
router.register(r'login', LoginViewSet, basename='login')

urlpatterns = router.urls
