#!/usr/bin/env python

from django.core.management.base import BaseCommand
from django.conf import settings

from coreomics.utils import import_submissions

class Command(BaseCommand):
    help = 'Update submissions.'
    def add_arguments(self, parser):
        parser.add_argument("--since_days_ago", type=int, default=90)
    def handle(self, *args, **options):
        days_ago = options.get("since_days_ago")
        import_submissions(days=days_ago)