from django.http import StreamingHttpResponse
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView

from exporter.services import CSVTemplateRenderer, CSVWriter
from pilotlog.api.serializers import ImportSerializer
from pilotlog.exporter.services import generate_logbook_template


class ImportView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ImportSerializer


class Echo:
    """An object that implements just the write method of the file-like interface."""

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


class ExportView(APIView):
    def get(self, request: Request) -> StreamingHttpResponse:
        csv_writer = CSVWriter()
        csv_template_renderer = CSVTemplateRenderer()

        logbook_template = generate_logbook_template()
        rendered_data = csv_template_renderer.render(template=logbook_template)

        response = StreamingHttpResponse(
            csv_writer.write(data=rendered_data), content_type="text/csv"
        )
        response["Content-Disposition"] = 'attachment; filename="export.csv"'

        return response
