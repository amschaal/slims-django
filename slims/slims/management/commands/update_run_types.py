#!/usr/bin/env python

from django.core.management.base import BaseCommand

from slims.run_type import RunTypeRegistry

class Command(BaseCommand):
    help = 'Update run types.'
    def handle(self, *args, **options):
        print('Updating database with registered run types...')
        RunTypeRegistry.sync_db()