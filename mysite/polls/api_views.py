from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from polls.models import Question
from polls.serializers.serializers import QuestionSerializer


class QuestionViewset(ReadOnlyModelViewSet):

    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.all()
