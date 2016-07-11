from django.conf.urls import url, include
from rest_framework import routers

from news.views import SegmentViewSet, TopicViewSet, AudienceViewSet

router = routers.SimpleRouter()
router.register(r'topic', TopicViewSet)
router.register(r'segment', SegmentViewSet)
router.register(r'audience', AudienceViewSet)

urlpatterns = [
    url(r'^api/docs/', include('rest_framework_swagger.urls')),
    url(r'^api/', include(router.urls)),
]
