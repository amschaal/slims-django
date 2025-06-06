#!/usr/bin/env python

from django.core.management.base import BaseCommand
from coreomics.models import Note
from slims.models import Run
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Send unsent notes.'
    def add_arguments(self, parser):
        parser.add_argument("--since_days_ago", type=int, default=14)
    def handle(self, *args, **options):
        days_ago = options.get("since_days_ago")
        created = date.today() - timedelta(days=days_ago)
        notes = Note.objects.filter(sent__isnull=True, created__date__gte=created)
        runs = Run.objects.filter(lanes__notes__in=notes).distinct()
        # print (runs)
        for note in notes:
            try:
                # note.send_note()
                print('Note {note} sent'.format(note=note))
            except:
                print('Note {note} send failed!!'.format(note=note))
        for run in runs:
            run.update_message_status()