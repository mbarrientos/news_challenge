import json
import os

from django.conf import settings
from django.core.management import BaseCommand

from news.models import Channel, Topic, Segment


class Command(BaseCommand):
    """
    Load segments dataset located at settings.SEGMENTS_FILE into database.
    """

    def handle(self, *args, **kwargs):
        c_names = ('A', 'B',)

        channels = []
        for c in c_names:
            channels.append(Channel.objects.get_or_create(name=c)[0])

        segments = []
        with open(os.path.join(settings.BASE_DIR, settings.SEGMENTS_FILE)) as f:
            for line in f.readlines():
                segments.append(json.loads(line))

        Segment.objects.all().delete()
        Topic.objects.all().delete()
        for s in segments:
            segment = Segment(channel=Channel.objects.get(name=s['channel']), start_ts=s['start_ts'],
                              end_ts=s['end_ts'])
            segment.save()
            topics = [Topic(name=t['name'], count=t['count'], score=t['score'], segment=segment) for t in s['topics']]
            Topic.objects.bulk_create(topics)
