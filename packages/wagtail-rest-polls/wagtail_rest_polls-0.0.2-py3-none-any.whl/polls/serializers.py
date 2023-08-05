from rest_framework.serializers import ModelSerializer

from polls.models import Poll, Vote


class PollSerializer(ModelSerializer):
    class Meta:
        model = Poll
        depth = 1
        fields = ['id', 'question', 'description', 'image', 'choices']


class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"

    def create(self, validated_data):
        vote = Vote(
            poll=validated_data['poll'],
            choice=validated_data['choice'],
            user=validated_data.get('user', None)
        )
        vote.save()
        return vote
