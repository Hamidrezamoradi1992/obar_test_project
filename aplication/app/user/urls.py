from django.urls import path
from app.user.views import SendCode, SingIn, VerifiCode, SignupView

urlpatterns = [
    path('send_code/', SendCode.as_view(), name='send_ciode'),
    path('verify_code/', VerifiCode.as_view(), name='verify'),
    path('singin/', SingIn.as_view(), name='sign_in'),
    path('signup/', SignupView.as_view(), name='signup'),

]