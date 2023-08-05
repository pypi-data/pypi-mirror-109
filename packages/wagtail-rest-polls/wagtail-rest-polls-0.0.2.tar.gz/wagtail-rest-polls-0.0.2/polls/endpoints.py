from rest_framework import routers

from polls.views import PollViewSet, VoteViewSet

router = routers.SimpleRouter()
router.register(r'vote', VoteViewSet, basename='vote')
router.register(r'', PollViewSet, basename='polls')
urlpatterns = router.urls
