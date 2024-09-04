from django.urls import path

from pilotlog.api.views import ExportView, ImportView


urlpatterns = [
    path("import/", ImportView.as_view(), name="import"),
    path("export/", ExportView.as_view(), name="export"),
]
