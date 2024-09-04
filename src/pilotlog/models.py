from django.db import models

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
