from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from polls.models import Question, Choice
from polls.serializers.serializers import ChoiceSerializer, QuestionListSerializer, QuestionDetailSerializer


class QuestionViewset(ReadOnlyModelViewSet):

    serializer_class = QuestionListSerializer

    detail_serializer_class = QuestionDetailSerializer

    def get_queryset(self):
        return Question.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class ChoiceViewset(ReadOnlyModelViewSet):

    serializer_class = ChoiceSerializer

    def get_queryset(self):
        queryset = Choice.objects.all()
        question_id = self.request.GET.get('question_id')
        if question_id is not None:
            queryset = queryset.filter(question_id=question_id)
        return queryset
