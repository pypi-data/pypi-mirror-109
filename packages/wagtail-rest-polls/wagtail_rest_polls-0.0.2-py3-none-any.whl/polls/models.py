from django.conf import settings
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, HelpPanel
from wagtail.core.models import Orderable, ClusterableModel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey


@register_snippet
class Poll(ClusterableModel):
    question = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        FieldPanel('question'),
        FieldPanel('description'),
        ImageChooserPanel('image'),
        InlinePanel("choices", label="Choices"),
        HelpPanel(template='polls/votes_panel.html', heading='Results')
    ]

    def __str__(self):
        return self.question

    def count_choices(self):
        return self.choices.count()

    def count_total_votes(self):
        result = 0
        for choice in self.choices.all():
            result += choice.count_votes()
        return result

    def can_vote(self, user):
        return not self.vote_set.filter(user=user).exists()


class Choice(index.Indexed, Orderable):
    poll = ParentalKey("polls.Poll", on_delete=models.CASCADE, related_name="choices")
    choice = models.CharField(max_length=255)

    search_fields = [
        index.SearchField('choice'),
    ]

    class Meta:
        ordering = ['choice']

    def __str__(self):
        return f'{self.poll}: {self.choice} - {self.count_votes()}'

    def count_votes(self):
        return self.vote_set.count()


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True,
                             null=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'Vote for {self.choice}'
