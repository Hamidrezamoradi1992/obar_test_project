from django.urls import path
from app.user.views import SendCode, SingIn, VerifiCode, SignupView

urlpatterns = [
    path('send_code/', SendCode.as_view(), name='send_ciode'),


]