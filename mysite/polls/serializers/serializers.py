from rest_framework import serializers

from polls.models import Question, Choice, Course


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ['question', 'choice_text', 'votes']


class QuestionSerializer(serializers.ModelSerializer):

    choices = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['question_text', 'pub_date', 'course', 'choices']

    def get_choices(self, instance):
        queryset = instance.choices
        serializer = ChoiceSerializer(queryset, many=True)
        return serializer.data


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['name', 'start_date', 'end_date', 'teacher', 'leaners']
