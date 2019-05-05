from django.core.management.base import BaseCommand, CommandError
from mining.models import Active
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        active = Active()
        while(True):
            active.id = None
            active.name = 'Test'
            active.ticker = 'Test3'
            active.save()
            time.sleep(10)