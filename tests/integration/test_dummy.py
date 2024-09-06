import pytest

from tests.factories import LogRecordFactory


pytestmark = pytest.mark.django_db  # noqa


def test_dummy() -> None:
    log_record = LogRecordFactory.create()
    print(log_record)
