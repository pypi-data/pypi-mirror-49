from __future__ import unicode_literals

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from ..models import Message

from .mixins import MOTDTestMixin


class MOTDTestCase(MOTDTestMixin, TestCase):
    def setUp(self):
        super(MOTDTestCase, self).setUp()
        self._create_test_message()

    def test_basic(self):
        queryset = Message.objects.get_for_now()

        self.assertEqual(queryset.exists(), True)

    def test_start_datetime(self):
        self.test_message.start_datetime = timezone.now() - timedelta(days=1)
        self.test_message.save()

        queryset = Message.objects.get_for_now()

        self.assertEqual(queryset.first(), self.test_message)

    def test_end_datetime(self):
        self.test_message.start_datetime = timezone.now() - timedelta(days=2)
        self.test_message.end_datetime = timezone.now() - timedelta(days=1)
        self.test_message.save()

        queryset = Message.objects.get_for_now()

        self.assertEqual(queryset.exists(), False)

    def test_enable(self):
        self.test_message.enabled = False
        self.test_message.save()

        queryset = Message.objects.get_for_now()

        self.assertEqual(queryset.exists(), False)
