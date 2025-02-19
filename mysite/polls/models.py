import datetime

from django.contrib import admin
from django.db.models import Sum
from django.utils import timezone

from django.db import models


MAX_LENGTH = 20


def text_excerpt(text, max_length):
    return text[:max_length] + ('...' if len(text) > max_length else '')


class Question(models.Model):
    """Question entity"""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def age(self):
        return timezone.now() - self.pub_date

    def get_choices(self):
        result = self.choice_set.aggregate(total=Sum('votes'))
        total = result['total']
        if total == 0:
            return [(c.choice_text, c.votes, 0) for c in self.choice_set.all()]

        return [(c.choice_text, c.votes, (c.votes / total)*100) for c in self.choice_set.all()]

    def get_max_choice(self):
        choices = self.choice_set.all()

        result = self.choice_set.aggregate(total=Sum('votes'))
        total = result['total']
        max_choice = max(choices, key=lambda c: c.votes / total)
        return max_choice.choice_text, max_choice.votes / total

    def __str__(self):
        return f"{self.pub_date} - {text_excerpt(self.question_text, MAX_LENGTH)}"

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        """
        Determinate if the question was published recently
        :return: boolean
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    """Choice of question"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return text_excerpt(self.choice_text, MAX_LENGTH)
