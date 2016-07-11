import json
import os

from django.conf import settings
from django.core.management import BaseCommand

from news.models import Channel, Audience


class Command(BaseCommand):
    """
    Load audience dataset located at settings.AUDIENCE_FILE into database.
    """

    def handle(self, *args, **kwargs):
        c_names = ('A', 'B',)

        channels = []
        for c in c_names:
            channels.append(Channel.objects.get_or_create(name=c)[0])

        with open(os.path.join(settings.BASE_DIR, settings.FILES_DIR, settings.AUDIENCE_FILE)) as f:
            audience = json.load(f)

            Audience.objects.all().delete()

            audiences = [Audience(channel=channels[idx], value=sizes[idx], timestamp=epoch)
                         for epoch, sizes in audience.items()
                         for idx, s in enumerate(sizes)]

            Audience.objects.bulk_create(audiences)
