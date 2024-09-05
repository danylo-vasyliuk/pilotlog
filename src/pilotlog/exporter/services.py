from exporter.types import Table, Template
from pilotlog.exporter.constants import AIRCRAFT_TABLE_HEADERS, FLIGHT_TABLE_HEADERS
from pilotlog.models import Aircraft, Flight


def generate_logbook_template() -> Template:
    return Template(
        name="ForeFlight Logbook Import",
        tables=[
            Table(
                name="Aircraft Table",
                headers=AIRCRAFT_TABLE_HEADERS,
                rows=Aircraft.objects.data_for_export().iterator(chunk_size=100),
            ),
            Table(
                name="Flights Table",
                headers=FLIGHT_TABLE_HEADERS,
                rows=Flight.objects.data_for_export().iterator(chunk_size=100),
            ),
        ],
    )
