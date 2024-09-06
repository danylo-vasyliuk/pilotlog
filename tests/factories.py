from django.utils import timezone
from factory import fuzzy
from factory.django import DjangoModelFactory

from pilotlog import models


class LogRecordFactory(DjangoModelFactory):
    user_id = fuzzy.FuzzyInteger(1, 1000)
    platform = fuzzy.FuzzyInteger(1, 1000)
    modified = fuzzy.FuzzyDateTime(timezone.now())

    class Meta:
        model = models.LogRecord
