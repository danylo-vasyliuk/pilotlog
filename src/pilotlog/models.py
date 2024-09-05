from django.db import models
from django.db.models import QuerySet
from django.db.models.functions import Cast, Coalesce, Concat

from pilotlog.importer.entities import TableType


class LogRecord(models.Model):
    guid = models.CharField(max_length=36)
    table = models.CharField(max_length=25, choices=TableType.choices)
    user_id = models.PositiveIntegerField()
    platform = models.PositiveIntegerField()
    modified = models.DateTimeField()

    class Meta:
        unique_together = (("guid", "table"),)


class CodeMixin(models.Model):
    code = models.UUIDField(primary_key=True)

    class Meta:
        abstract = True


class RecordModifiedMixin(models.Model):
    record_modified = models.DateTimeField()

    class Meta:
        abstract = True


class AircraftManager(models.Manager):
    def data_for_export(self) -> QuerySet["Aircraft"]:
        empty_value = models.Value("", output_field=models.CharField())

        # if field is commented, it means it exist in requirements template,
        # but I don't know which field is response for this data
        export_annotations = {
            "AircraftID": Cast(models.F("code"), models.CharField()),
            # "EquipmentType": empty_value,
            # "TypeCode": empty_value,
            # "Year": empty_value,
            "Make": models.F("make"),
            # "Model": empty_value,
            "Category": Cast(models.F("category"), models.CharField()),
            "Class": Cast(models.F("aircraft_class"), models.CharField()),
            # "GearType": empty_value,
            "EngineType": Coalesce(
                Cast(models.F("eng_type"), models.CharField()),
                empty_value,
                output_field=models.CharField(),
            ),
            "Complex": models.F("complex"),
            "HighPerformance": models.F("high_perf"),
            # "Pressurized": empty_value,
            # "TAA": empty_value,
        }
        return (
            self.get_queryset()
            .annotate(**export_annotations)
            .values(*export_annotations.keys())
        )


class Aircraft(CodeMixin, RecordModifiedMixin):
    fin = models.CharField(max_length=255)
    sea = models.BooleanField()
    tmg = models.BooleanField()
    efis = models.BooleanField()
    fnpt = models.PositiveIntegerField()
    make = models.CharField(max_length=255)
    run2 = models.BooleanField()
    aircraft_class = models.PositiveIntegerField()
    model = models.CharField(max_length=255)
    power = models.PositiveIntegerField()
    seats = models.PositiveIntegerField()
    active = models.BooleanField()
    kg5700 = models.BooleanField()
    rating = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    complex = models.BooleanField()
    cond_log = models.PositiveIntegerField()
    fav_list = models.BooleanField()
    category = models.PositiveIntegerField()
    high_perf = models.BooleanField()
    sub_model = models.CharField(max_length=255)
    aerobatic = models.BooleanField()
    ref_search = models.CharField(max_length=255)
    reference = models.CharField(max_length=255)
    tail_wheel = models.BooleanField()
    default_app = models.PositiveIntegerField()
    default_log = models.PositiveIntegerField()
    default_ops = models.PositiveIntegerField()
    device_code = models.PositiveIntegerField()
    default_launch = models.PositiveIntegerField()

    # "table": "aircraft" fields
    eng_group = models.PositiveIntegerField(blank=True, null=True)
    eng_type = models.PositiveIntegerField(blank=True, null=True)

    objects = AircraftManager()


class AirField(CodeMixin, RecordModifiedMixin):
    af_cat = models.PositiveIntegerField()
    afiata = models.CharField(max_length=255)
    aficao = models.CharField(max_length=255)
    af_name = models.CharField(max_length=255)
    tz_code = models.PositiveIntegerField()
    latitude = models.FloatField()
    show_list = models.BooleanField()
    af_country = models.PositiveIntegerField()
    longitude = models.FloatField()
    notes_user = models.CharField(max_length=255)
    region_user = models.PositiveIntegerField()
    elevation_ft = models.IntegerField()

    # "table": "airfield" fields
    affaa = models.CharField(max_length=255, blank=True, null=True)
    user_edit = models.BooleanField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)


class Pilot(CodeMixin, RecordModifiedMixin):
    notes = models.CharField(max_length=255)
    active = models.BooleanField()
    company = models.CharField(max_length=255)
    fav_list = models.BooleanField()
    user_api = models.CharField(max_length=255)
    facebook = models.CharField(max_length=255)
    linkedin = models.CharField(max_length=255)
    pilot_ref = models.CharField(max_length=255)
    pilot_name = models.CharField(max_length=255)
    pilot_email = models.CharField(max_length=255)
    pilot_phone = models.CharField(max_length=255)
    certificate = models.CharField(max_length=255)
    phone_search = models.CharField(max_length=255)
    pilot_search = models.CharField(max_length=255)
    roster_alias = models.CharField(max_length=255, blank=True, null=True)


class FlightManager(models.Manager):
    def data_for_export(self) -> QuerySet["Flight"]:
        empty_value = models.Value("", output_field=models.CharField())

        def _get_pilot_data(p: str):
            return Concat(
                models.F(f"{p}__pilot_name"),
                models.Value(";"),
                models.F(f"{p}__company"),
                models.Value(";"),
                models.F(f"{p}__pilot_email"),
            )

        def _get_approach():
            return Concat(
                models.F("tag_approach"),
                models.Value(";"),
                models.F("dep_rwy"),
                models.Value(";"),
                models.F("dep__af_name"),
                models.Value(";"),
                models.F("remarks"),
            )

        # if field is commented, it means it exist in requirements template,
        # but I don't know which field is response for this data
        export_annotations = {
            "Date": models.F("date_utc"),
            "AircraftID": Cast(models.F("aircraft_id"), models.CharField()),
            "From": empty_value,
            "To": models.F("to_day"),
            "Route": models.F("route"),
            "TimeOut": empty_value,
            "TimeOff": empty_value,
            "TimeOn": empty_value,
            "TimeIn": empty_value,
            # "OnDuty": empty_value,
            # "OffDuty": empty_value,
            # "TotalTime": empty_value,
            "PIC": models.F("min_pic"),
            # "SIC": empty_value,
            # "Night": empty_value,
            # "Solo": empty_value,
            # "CrossCountry": empty_value,
            # "NVG": empty_value,
            # "NVGOps": empty_value,
            # "Distance": empty_value,
            # "DayTakeoffs": empty_value,
            # "DayLandingsFullStop": empty_value,
            # "NightTakeoffs": empty_value,
            # "NightLandingsFullStop": empty_value,
            # "AllLandings": empty_value,
            # "ActualInstrument": empty_value,
            # "SimulatedInstrument": empty_value,
            "HobbsStart": models.F("hobbs_in"),
            "HobbsEnd": models.F("hobbs_out"),
            # "TachStart": empty_value,
            # "TachEnd": empty_value,
            # "Holds": empty_value,
            "Approach1": _get_approach(),
            # "Approach2": empty_value,
            # "Approach3": empty_value,
            # "Approach4": empty_value,
            # "Approach5": empty_value,
            # "Approach6": empty_value,
            # "DualGiven": empty_value,
            # "DualReceived": empty_value,
            # "SimulatedFlight": empty_value,
            # "GroundTraining": empty_value,
            # "InstructorName": empty_value,
            # "InstructorComments": empty_value,
            "Person1": _get_pilot_data("p1"),
            "Person2": _get_pilot_data("p2"),
            "Person3": _get_pilot_data("p3"),
            "Person4": _get_pilot_data("p4"),
            # "Person5": empty_value,
            # "Person6": empty_value,
            # "FlightReview": empty_value,
            # "Checkride": empty_value,
            # "IPC": empty_value,
            # "NVGProficiency": empty_value,
            # "FAA6158": empty_value,
            # "[Text]CustomFieldName": empty_value,
            # "[Numeric]CustomFieldName": empty_value,
            # "[Hours]CustomFieldName": empty_value,
            # "[Counter]CustomFieldName": empty_value,
            # "[Date]CustomFieldName": empty_value,
            # "[DateTime]CustomFieldName": empty_value,
            # "[Toggle]CustomFieldName": empty_value,
            # "PilotComments": empty_value,
        }
        return (
            self.get_queryset()
            .select_related("p1", "p2", "p3", "p4", "dep")
            .annotate(**export_annotations)
            .values(*export_annotations.keys())
        )


class Flight(CodeMixin, RecordModifiedMixin):
    pf = models.BooleanField()
    pax = models.PositiveIntegerField()
    fuel = models.PositiveIntegerField()
    de_ice = models.BooleanField()
    route = models.CharField(max_length=255)
    to_day = models.PositiveIntegerField()
    min_u1 = models.PositiveIntegerField()
    min_u2 = models.PositiveIntegerField()
    min_u3 = models.PositiveIntegerField()
    min_u4 = models.PositiveIntegerField()
    min_xc = models.PositiveIntegerField()
    arr_rwy = models.CharField(max_length=255)
    dep_rwy = models.CharField(max_length=255)
    ldg_day = models.PositiveIntegerField()
    lift_sw = models.PositiveIntegerField()
    report = models.CharField(max_length=255)
    tag_ops = models.CharField(max_length=255)
    to_edit = models.BooleanField()
    min_air = models.PositiveIntegerField()
    min_ifr = models.PositiveIntegerField()
    min_pic = models.PositiveIntegerField()
    min_rel = models.PositiveIntegerField()
    min_sfr = models.PositiveIntegerField()
    date_utc = models.DateField()
    hobbs_in = models.IntegerField()
    holding = models.PositiveIntegerField()
    pairing = models.CharField(max_length=255)
    remarks = models.CharField(max_length=255)
    sign_box = models.PositiveIntegerField()
    to_night = models.PositiveIntegerField()
    user_num = models.PositiveIntegerField()
    min_dual = models.PositiveIntegerField()
    min_exam = models.PositiveIntegerField()
    crew_list = models.CharField(max_length=255)
    date_base = models.DateField(blank=True, null=True)
    fuel_used = models.PositiveIntegerField()
    hobbs_out = models.IntegerField()
    ldg_night = models.PositiveIntegerField()
    next_page = models.BooleanField()
    tag_delay = models.CharField(max_length=255)
    training = models.CharField(max_length=255)
    user_bool = models.BooleanField()
    user_text = models.CharField(max_length=255)
    min_inst = models.PositiveIntegerField()
    min_night = models.PositiveIntegerField()
    min_picus = models.PositiveIntegerField()
    min_total = models.PositiveIntegerField()
    arr_offset = models.IntegerField()
    date_local = models.DateField(blank=True, null=True)
    dep_offset = models.IntegerField()
    tag_launch = models.CharField(max_length=255)
    tag_lesson = models.CharField(max_length=255)
    to_time_utc = models.IntegerField()
    base_offset = models.IntegerField()
    ldg_time_utc = models.IntegerField()
    fuel_planned = models.PositiveIntegerField()
    next_summary = models.BooleanField()
    tag_approach = models.CharField(max_length=255)
    arr_time_sched = models.IntegerField()
    dep_time_sched = models.IntegerField()
    flight_number = models.CharField(max_length=255)
    flight_search = models.CharField(max_length=255)

    # table: "flight" fields
    cargo = models.PositiveIntegerField(blank=True, null=True)
    dep_time_utc = models.IntegerField(blank=True, null=True)
    arr_time_utc = models.IntegerField(blank=True, null=True)

    p1 = models.ForeignKey(
        Pilot,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="p1_flights",
    )
    p2 = models.ForeignKey(
        Pilot,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="p2_flights",
    )
    p3 = models.ForeignKey(
        Pilot,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="p3_flights",
    )
    p4 = models.ForeignKey(
        Pilot,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="p4_flights",
    )
    aircraft = models.ForeignKey(
        Aircraft,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="flights",
    )
    arr = models.ForeignKey(
        AirField,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="arrival_flights",
    )
    dep = models.ForeignKey(
        AirField,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="departure_flights",
    )

    objects = FlightManager()


class ImagePic(CodeMixin, RecordModifiedMixin):
    file_ext = models.CharField(max_length=10)
    file_name = models.CharField(max_length=255)
    link_code = models.UUIDField()
    img_upload = models.BooleanField()
    img_download = models.BooleanField()


class LimitRules(CodeMixin, RecordModifiedMixin):
    l_to = models.DateField()
    l_from = models.DateField()
    l_type = models.PositiveIntegerField()
    l_zone = models.PositiveIntegerField()
    l_minutes = models.PositiveIntegerField()
    l_period_code = models.PositiveIntegerField()


class MyQuery(CodeMixin, RecordModifiedMixin):
    name = models.CharField(max_length=255)
    quick_view = models.BooleanField()
    short_name = models.CharField(max_length=255)


class MyQueryBuild(CodeMixin, RecordModifiedMixin):
    my_query = models.ForeignKey(
        MyQuery, on_delete=models.SET_NULL, null=True, related_name="builds"
    )

    build_1 = models.CharField(max_length=255)
    build_2 = models.IntegerField()
    build_3 = models.IntegerField()
    build_4 = models.CharField(max_length=255)


class Qualification(CodeMixin, RecordModifiedMixin):
    ref_extra = models.IntegerField()
    ref_model = models.CharField(max_length=255)
    validity = models.IntegerField()
    date_valid = models.DateField(blank=True, null=True)
    q_type_code = models.IntegerField()
    date_issued = models.DateField(blank=True, null=True)
    minimum_qty = models.PositiveIntegerField()
    notify_days = models.PositiveIntegerField()
    minimum_period = models.PositiveIntegerField()
    notify_comment = models.CharField(max_length=255)

    ref_airfield = models.ForeignKey(
        AirField, on_delete=models.SET_NULL, null=True, related_name="qualifications"
    )


class SettingConfig(RecordModifiedMixin):
    code = models.IntegerField(primary_key=True)

    data = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    group = models.CharField(max_length=255)
