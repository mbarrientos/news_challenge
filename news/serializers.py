"""
Basic serializers for news_desk models.
"""
from rest_framework.serializers import ModelSerializer

from news.models import Topic, Audience, Segment, Channel

__all__ = ['TopicSerializer', 'AudienceSerializer', 'SegmentSerializer', 'ChannelSerializer']


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic


class AudienceSerializer(ModelSerializer):
    class Meta:
        model = Audience


class SegmentSerializer(ModelSerializer):
    class Meta:
        model = Segment


class ChannelSerializer(ModelSerializer):
    class Meta:
        model = Channel
