from django.views.generic import DetailView, ListView, RedirectView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins

from polls.models import Choice, Poll, Vote
from polls.serializers import PollSerializer, VoteSerializer


# Generic Views for rendering templates
class PollListView(ListView):
    model = Poll


class PollDetailView(DetailView):
    model = Poll


class PollVoteView(RedirectView):
    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(id=kwargs['pk'])
        user = request.user
        choice = Choice.objects.get(id=request.POST['choice_pk'])
        Vote.objects.create(poll=poll, user=user, choice=choice)
        messages.success(request, _("Thanks for your vote."))
        return super(PollVoteView, self).post(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return reverse_lazy('polls:detail', args=[kwargs['pk']])


# API views

class PollViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class VoteViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Custom Viewset so Votes can only be created from REST
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def create(self, request):
        """
        override the default create method to return a list of results
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        poll = Poll.objects.get(id=serializer.data['poll'])
        result = {
            "results": [{choice.choice: choice.count_votes()} for choice in poll.choices.all()]}
        return Response(result, status=status.HTTP_201_CREATED, headers=headers)
