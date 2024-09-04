from datetime import date, datetime
from enum import StrEnum
from uuid import UUID

from pydantic import Field, field_validator

from importer.types import Entity


class RecordModifiedMixin(Entity):
    record_modified: datetime = Field(..., alias="Record_Modified")


class TableType(StrEnum):
    AIRFIELD = "airfield"
    AIRCRAFT = "aircraft"
    AIRPORT = "airport"
    PILOT = "pilot"
    FLIGHT = "flight"
    IMAGE_PIC = "imagepic"
    LIMIT_RULES = "limitrules"
    MY_QUERY = "myquery"
    MY_QUERY_BUILD = "myquerybuild"
    QUALIFICATION = "qualification"
    SETTING_CONFIG = "settingconfig"

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(v, v) for v in cls]


class LogRecordEntity(Entity):
    user_id: int
    guid: str
    table: TableType
    meta: RecordModifiedMixin
    platform: int
    record_modified: datetime = Field(..., alias="_modified")

    @field_validator("table", mode="before")
    @classmethod
    def validate_table_name(cls, v: str) -> str:
        return v.lower()


class AirCraftEntity(RecordModifiedMixin):
    code: UUID = Field(..., alias="AircraftCode")
    fin: str = Field(..., alias="Fin")
    sea: bool = Field(..., alias="Sea")
    tmg: bool = Field(..., alias="TMG")
    efis: bool = Field(..., alias="Efis")
    fnpt: int = Field(..., alias="FNPT")
    make: str = Field(..., alias="Make")
    run2: bool = Field(..., alias="Run2")
    aircraft_class: int = Field(..., alias="Class")
    model: str = Field(..., alias="Model")
    power: int = Field(..., alias="Power")
    seats: int = Field(..., alias="Seats")
    active: bool = Field(..., alias="Active")
    kg5700: bool = Field(..., alias="Kg5700")
    rating: str = Field(..., alias="Rating")
    company: str = Field(..., alias="Company")
    complex: bool = Field(..., alias="Complex")
    cond_log: int = Field(..., alias="CondLog")
    fav_list: bool = Field(..., alias="FavList")
    category: int = Field(..., alias="Category")
    high_perf: bool = Field(..., alias="HighPerf")
    sub_model: str = Field(..., alias="SubModel")
    aerobatic: bool = Field(..., alias="Aerobatic")
    ref_search: str = Field(..., alias="RefSearch")
    reference: str = Field(..., alias="Reference")
    tail_wheel: bool = Field(..., alias="Tailwheel")
    default_app: int = Field(..., alias="DefaultApp")
    default_log: int = Field(..., alias="DefaultLog")
    default_ops: int = Field(..., alias="DefaultOps")
    device_code: int = Field(..., alias="DeviceCode")
    default_launch: int = Field(..., alias="DefaultLaunch")

    # "table": "aircraft" fields
    eng_group: int | None = Field(None, alias="EngGroup")
    eng_type: int | None = Field(None, alias="EngType")


class AirFieldEntity(RecordModifiedMixin):
    code: UUID = Field(..., alias="AFCode")
    af_cat: int = Field(..., alias="AFCat")
    afiata: str = Field(..., alias="AFIATA")
    aficao: str = Field(..., alias="AFICAO")
    af_name: str = Field(..., alias="AFName")
    tz_code: int = Field(..., alias="TZCode")
    latitude: float = Field(..., alias="Latitude")
    show_list: bool = Field(..., alias="ShowList")
    af_country: int = Field(..., alias="AFCountry")
    longitude: float = Field(..., alias="Longitude")
    notes_user: str = Field(..., alias="NotesUser")
    region_user: int = Field(..., alias="RegionUser")
    elevation_ft: int = Field(..., alias="ElevationFT")

    # "table": "airfield" fields
    affaa: str | None = Field(None, alias="AFFAA")
    user_edit: bool | None = Field(None, alias="UserEdit")
    city: str | None = Field(None, alias="City")
    notes: str | None = Field(None, alias="Notes")


class PilotEntity(RecordModifiedMixin):
    code: UUID = Field(..., alias="PilotCode")
    notes: str = Field(..., alias="Notes")
    active: bool = Field(..., alias="Active")
    company: str = Field(..., alias="Company")
    fav_list: bool = Field(..., alias="FavList")
    user_api: str = Field(..., alias="UserAPI")
    facebook: str = Field(..., alias="Facebook")
    linkedin: str = Field(..., alias="LinkedIn")
    pilot_ref: str = Field(..., alias="PilotRef")
    pilot_name: str = Field(..., alias="PilotName")
    pilot_email: str = Field(..., alias="PilotEMail")
    pilot_phone: str = Field(..., alias="PilotPhone")
    certificate: str = Field(..., alias="Certificate")
    phone_search: str = Field(..., alias="PhoneSearch")
    pilot_search: str = Field(..., alias="PilotSearch")
    roster_alias: str | None = Field(None, alias="RosterAlias")


class FlightEntity(RecordModifiedMixin):
    code: UUID = Field(..., alias="FlightCode")
    pf: bool = Field(..., alias="PF")
    pax: int = Field(..., alias="Pax")
    fuel: int = Field(..., alias="Fuel")
    de_ice: bool = Field(..., alias="DeIce")
    route: str = Field(..., alias="Route")
    to_day: int = Field(..., alias="ToDay")
    min_u1: int = Field(..., alias="minU1")
    min_u2: int = Field(..., alias="minU2")
    min_u3: int = Field(..., alias="minU3")
    min_u4: int = Field(..., alias="minU4")
    min_xc: int = Field(..., alias="minXC")
    arr_rwy: str = Field(..., alias="ArrRwy")
    dep_rwy: str = Field(..., alias="DepRwy")
    ldg_day: int = Field(..., alias="LdgDay")
    lift_sw: int = Field(..., alias="LiftSW")
    report: str = Field(..., alias="Report")
    tag_ops: str = Field(..., alias="TagOps")
    to_edit: bool = Field(..., alias="ToEdit")
    min_air: int = Field(..., alias="minAIR")
    min_ifr: int = Field(..., alias="minIFR")
    min_pic: int = Field(..., alias="minPIC")
    min_rel: int = Field(..., alias="minREL")
    min_sfr: int = Field(..., alias="minSFR")
    date_utc: date = Field(..., alias="DateUTC")
    hobbs_in: int = Field(..., alias="HobbsIn")
    holding: int = Field(..., alias="Holding")
    pairing: str = Field(..., alias="Pairing")
    remarks: str = Field(..., alias="Remarks")
    sign_box: int = Field(..., alias="SignBox")
    to_night: int = Field(..., alias="ToNight")
    user_num: int = Field(..., alias="UserNum")
    min_dual: int = Field(..., alias="minDUAL")
    min_exam: int = Field(..., alias="minEXAM")
    crew_list: str = Field(..., alias="CrewList")
    date_base: date | None = Field(None, alias="DateBASE")
    fuel_used: int = Field(..., alias="FuelUsed")
    hobbs_out: int = Field(..., alias="HobbsOut")
    ldg_night: int = Field(..., alias="LdgNight")
    next_page: bool = Field(..., alias="NextPage")
    tag_delay: str = Field(..., alias="TagDelay")
    training: str = Field(..., alias="Training")
    user_bool: bool = Field(..., alias="UserBool")
    user_text: str = Field(..., alias="UserText")
    min_inst: int = Field(..., alias="minINSTR")
    min_night: int = Field(..., alias="minNIGHT")
    min_picus: int = Field(..., alias="minPICUS")
    min_total: int = Field(..., alias="minTOTAL")
    arr_offset: int = Field(..., alias="ArrOffset")
    date_local: date | None = Field(None, alias="DateLocal")
    dep_offset: int = Field(..., alias="DepOffset")
    tag_launch: str = Field(..., alias="TagLaunch")
    tag_lesson: str = Field(..., alias="TagLesson")
    to_time_utc: int = Field(..., alias="ToTimeUTC")
    base_offset: int = Field(..., alias="BaseOffset")
    ldg_time_utc: int = Field(..., alias="LdgTimeUTC")
    fuel_planned: int = Field(..., alias="FuelPlanned")
    next_summary: bool = Field(..., alias="NextSummary")
    tag_approach: str = Field(..., alias="TagApproach")
    arr_time_sched: int = Field(..., alias="ArrTimeSCHED")
    dep_time_sched: int = Field(..., alias="DepTimeSCHED")
    flight_number: str = Field(..., alias="FlightNumber")
    flight_search: str = Field(..., alias="FlightSearch")

    # table: "flight" fields
    cargo: int | None = Field(None, alias="Cargo")
    arr_time_utc: int | None = Field(None, alias="ArrTimeUTC")
    dep_time_utc: int | None = Field(None, alias="DepTimeUTC")

    p1_code: UUID = Field(..., alias="P1Code")
    p2_code: UUID = Field(..., alias="P2Code")
    p3_code: UUID = Field(..., alias="P3Code")
    p4_code: UUID = Field(..., alias="P4Code")
    aircraft_code: UUID | None = Field(None, alias="AircraftCode")
    arr_code: UUID = Field(..., alias="ArrCode")
    dep_code: UUID = Field(..., alias="DepCode")


class ImagePicEntity(RecordModifiedMixin):
    code: UUID = Field(..., alias="ImgCode")
    file_ext: str = Field(..., alias="FileExt")
    file_name: str = Field(..., alias="FileName")
    link_code: UUID = Field(..., alias="LinkCode")
    img_upload: bool = Field(..., alias="Img_Upload")
    img_download: bool = Field(..., alias="Img_Download")


class LimitRulesEntity(RecordModifiedMixin):
    code: UUID = Field(..., alias="LimitCode")
    l_to: date = Field(..., alias="LTo")
    l_from: date = Field(..., alias="LFrom")
    l_type: int = Field(..., alias="LType")
    l_zone: int = Field(..., alias="LZone")
    l_minutes: int = Field(..., alias="LMinutes")
    l_period_code: int = Field(..., alias="LPeriodCode")


class MyQueryEntity(RecordModifiedMixin):
    code: UUID = Field(..., alias="mQCode")
    name: str = Field(..., alias="Name")
    quick_view: bool = Field(..., alias="QuickView")
    short_name: str = Field(..., alias="ShortName")


class MyQueryBuildEntity(RecordModifiedMixin):
    code: UUID = Field(..., alias="mQBCode")
    build_1: str = Field(..., alias="Build1")
    build_2: int = Field(..., alias="Build2")
    build_3: int = Field(..., alias="Build3")
    build_4: str = Field(..., alias="Build4")
    my_query_code: UUID = Field(..., alias="mQCode")


class QualificationEntity(RecordModifiedMixin):
    code: UUID = Field(..., alias="QCode")
    ref_extra: int = Field(..., alias="RefExtra")
    ref_model: str = Field(..., alias="RefModel")
    validity: int = Field(..., alias="Validity")
    date_valid: date | None = Field(alias="DateValid")
    q_type_code: int = Field(..., alias="QTypeCode")
    date_issued: date | None = Field(alias="DateIssued")
    minimum_qty: int = Field(..., alias="MinimumQty")
    notify_days: int = Field(..., alias="NotifyDays")
    minimum_period: int = Field(..., alias="MinimumPeriod")
    notify_comment: str = Field(..., alias="NotifyComment")

    ref_airfield_code: UUID = Field(..., alias="RefAirfield")

    @field_validator("date_valid", "date_issued", mode="before")
    @classmethod
    def validate_date(cls, v: date | None) -> date | None:
        return v or None


class SettingConfigEntity(RecordModifiedMixin):
    code: int = Field(..., alias="ConfigCode")
    data: str = Field(..., alias="Data")
    name: str = Field(..., alias="Name")
    group: str = Field(..., alias="Group")
