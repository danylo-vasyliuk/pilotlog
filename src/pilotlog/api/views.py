from django.http import HttpResponse
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView

from pilotlog.api.serializers import ImportSerializer


class ImportView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ImportSerializer


class ExportView(APIView):
    def get(self, request: Request) -> HttpResponse:
        content = b""  # TODO call pilotlog exporter here
        response = HttpResponse(content=content, content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename=output.csv"
        return response
