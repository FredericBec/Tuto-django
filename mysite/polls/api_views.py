from rest_framework.response import Response
from rest_framework.views import APIView

from polls.models import Question
from polls.serializers.serializers import QuestionSerializer


class QuestionAPIView(APIView):

    def get(self, *args, **kwargs):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
