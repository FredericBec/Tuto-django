from rest_framework.serializers import ModelSerializer

from polls.models import Question, Choice, Course


class QuestionSerializer(ModelSerializer):

    class Meta:
        model = Question
        fields = ['question_text', 'pub_date', 'course']


class ChoiceSerializer(ModelSerializer):

    question = QuestionSerializer()

    class Meta:
        model = Choice
        fields = ['question', 'choice_text', 'votes']


class CourseSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = ['name', 'start_date', 'end_date', 'teacher', 'leaners']
