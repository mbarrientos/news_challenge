import datetime
import time
from collections import defaultdict
from functools import reduce

from django.db.models import Q
from django_pandas.io import read_frame
from rest_framework.decorators import list_route
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from news.models import Topic, Audience, Segment
from news.serializers import TopicSerializer, SegmentSerializer, AudienceSerializer


def to_epoch(*args):
    return time.mktime(datetime.datetime(*args).timetuple())


class AudienceViewSet(ReadOnlyModelViewSet):
    """
    """
    queryset = Audience.objects.all()
    serializer_class = AudienceSerializer

    @list_route(url_path='by-date')
    def by_date(self, request, format=None, *args, **kwargs):
        """
        For a given date "YYYY-mm-dd" return each topic that happened on that date with its performance on
        every channel.

        Performance is the mean audience during the segment of the topic.
        :return: JSON with the following format:

        {
            "topic1": {"A": 1.2, "B": 3.4},
            "topic2": {"A": 6.4, "B": 6123},
            ...
        }
        """
        #  Parse parameters from URL
        try:
            date = datetime.datetime.strptime(request.query_params['date'], "%Y-%m-%d")
        except KeyError:
            raise ParseError

        #  Range of 24 hours for the given day
        day_start = date.timestamp()
        day_end = (date + datetime.timedelta(days=1)).timestamp()

        report = defaultdict(dict)

        #  Building queryset with topics that happened on the given day
        topics = Topic.objects.select_related('segment').filter(
            Q(segment__start_ts__range=(day_start, day_end)) | Q(segment__end_ts__range=(day_start, day_end))
        )

        #  Aggregating audiences for each topic
        for t in topics:
            audiences = Audience.objects.filter(
                timestamp__range=(t.segment.start_ts, t.segment.end_ts)
            ).values_list('value', flat=True)
            report[t.name][t.segment.channel.name] = sum(audiences) / len(audiences)

        return Response(report)


class TopicViewSet(ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    @list_route()
    def timeline(self, request, format=None, *args, **kwargs):
        """
        For a given topic, returns a list of audience measures over time at each channel.

        [
            {"channel": A,
            "audience": [
                {
                    "timestamp": 1448760420,
                    "value": 68798
                },
                {
                    "timestamp": 1448416560,
                    "value": 43010
                },
                ...
            ]},
            {"channel": B,
            "audience": [
                {
                    "timestamp": 1446504900,
                    "value": 116138
                },
                {
                    "timestamp": 1446726480,
                    "value": 111083
                }
                ...
            ]},
        ]
        """

        try:
            topic_name = request.query_params['topic']
        except KeyError:
            raise ParseError('Missing parameter "topic".')

        topics = Topic.objects.filter(name__iexact=topic_name).select_related()
        if topics:
            filters = [Q(timestamp__range=(t.segment.start_ts, t.segment.end_ts)) for t in topics]
            df_audiences = read_frame(Audience.objects.filter(reduce((lambda x, y: x | y), filters)),
                                      fieldnames=('timestamp', 'value', 'channel__name'))

            response = [{'channel': k, 'audience': [{'timestamp': a[1]['timestamp'], 'value': a[1]['value']}
                                                    for a in aud.iterrows()]}
                        for k, aud in df_audiences.groupby('channel__name')]
        else:
            response = []

        return Response(response)

    @list_route(url_path='segments')
    def best_segments(self, request, format=None, *args, **kwargs):
        """
        For a given topic, show segments where performance on each channel was best.
        :return:
        """

        try:
            topic_name = request.query_params['topic']
        except KeyError:
            raise ParseError('Missing parameter "topic".')

        topics = Topic.objects.filter(name__iexact=topic_name).select_related('segment')
        segment_ids = topics.values_list('segment__id', flat=True)
        segments = Segment.objects.filter(id__in=segment_ids)
        if topics:
            filters = [Q(timestamp__range=(t.segment.start_ts, t.segment.end_ts)) for t in topics]
            df_audiences = read_frame(Audience.objects.filter(reduce((lambda x, y: x | y), filters)),
                                      fieldnames=('timestamp', 'value', 'channel__name'))

            df = read_frame(segments, fieldnames=('id', 'start_ts', 'end_ts', 'channel__name'))
            mean_func = lambda x: df_audiences[(df_audiences['timestamp'] <= x['end_ts'])
                                               & (df_audiences['timestamp'] >= x['start_ts'])
                                               & (df_audiences['channel__name'] == x['channel__name'])
                                               ]['value'].mean()

            df['audience'] = df.apply(mean_func, axis=1)

            response = {}
            for ch, df in df.groupby('channel__name'):
                response[ch] = df.sort_values(by=['channel__name', 'audience'], ascending=(True, False)).to_dict(
                    orient='record')
        else:
            response = []

        return Response(response)


class SegmentViewSet(ReadOnlyModelViewSet):
    queryset = Segment.objects.all()
    serializer_class = SegmentSerializer
