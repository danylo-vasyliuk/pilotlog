from django.urls import include, path


urlpatterns = [
    path("api/v1/pilotlog/", include("pilotlog.api.urls")),
]
