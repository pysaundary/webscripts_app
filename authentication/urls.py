from rest_framework.urls import path
from .views import CreateUserView,LoginUserView,ForgetPasswordView,ConfirmPasswordView
app_name = "authentication"

urlpatterns = [
    path("register/",CreateUserView.as_view(
        {
            'post':"create"
        }
    ),name="create user"),
    path("login/",LoginUserView.as_view(
        {
    'post':"create"
}
    ),name="login user"),
    path("forget-password-request/",ForgetPasswordView.as_view(
        {
            "post":"create"
        }
    )),
    path(
        "confirm-password/",ConfirmPasswordView.as_view(
            {
                "post":"create"
            }
        )
    )
]
