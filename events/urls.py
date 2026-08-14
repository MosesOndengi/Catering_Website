from django.urls import path

from . import views


urlpatterns = [
    path(
        "estimator/",
        views.estimator,
        name="estimator"
    ),
]