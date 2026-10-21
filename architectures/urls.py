from django.urls import path
from . import views

app_name = "architectures"

urlpatterns = [
    path(
        "",
        views.library,
        name="library"
    ),

    path(
        "architecture/<slug:slug>/",
        views.architecture_detail,
        name="detail"
    ),
]