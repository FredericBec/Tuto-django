from rest_framework.serializers import ModelSerializer

from polls.models import Question, Choice


class QuestionSerializer(ModelSerializer):

    class Meta:
        model = Question
        fields = ['question_text', 'pub_date', 'course']


class ChoiceSerializer(ModelSerializer):

    class Meta:
        model = Choice
        fields = ['question', 'choice_text', 'votes']
