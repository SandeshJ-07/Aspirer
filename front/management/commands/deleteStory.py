from django.core.management.base import BaseCommand, CommandError
from front.models import Story
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "To delete the story after 24 hours"
    def handle(self, *args, **options):
        stories = Story.objects.filter(uploadTime__lte = datetime.now() - timedelta(days = 1))
        for i in stories:
            i.Image.delete()
            i.delete()
        self.stdout.write('Deleted stories older than 1 day')
