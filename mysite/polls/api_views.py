from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from polls.models import Question, Choice
from polls.serializers.serializers import ChoiceSerializer, QuestionListSerializer, QuestionDetailSerializer


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class QuestionViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = QuestionListSerializer

    detail_serializer_class = QuestionDetailSerializer

    def get_queryset(self):
        return Question.objects.all()


class ChoiceViewset(ReadOnlyModelViewSet):

    serializer_class = ChoiceSerializer

    def get_queryset(self):
        queryset = Choice.objects.all()
        question_id = self.request.GET.get('question_id')
        if question_id is not None:
            queryset = queryset.filter(question_id=question_id)
        return queryset


class AdminQuestionViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = QuestionListSerializer
    detail_serializer_class = QuestionDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Question.objects.all()


class AdminChoiceViewset(ModelViewSet):
    serializer_class = ChoiceSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Choice.objects.all()
