from rest_framework.serializers import ModelSerializer

from polls.models import Question


class QuestionSerializer(ModelSerializer):

    class Meta:
        model = Question
        fields = ['question_text', 'pub_date', 'course']