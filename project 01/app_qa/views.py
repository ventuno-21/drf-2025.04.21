from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Question
from .serializers import QuestionSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from permissions import IsOwnerOrReadOnly

# Create your views here.


class QuestionListView(APIView):

    def get(self, request):
        questions = Question.objects.all()
        srz_data = QuestionSerializer(instance=questions, many=True).data
        return Response(srz_data, status=status.HTTP_200_OK)


class QuestionCreateView(APIView):
    """
    Create a new question
    """

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = QuestionSerializer

    def post(self, request):
        srz_data = QuestionSerializer(data=request.data)
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_201_CREATED)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionUpdateView(APIView):
    permission_classes = [
        IsOwnerOrReadOnly,
    ]

    def put(self, request, pk):
        my_question = Question.objects.get(pk=pk)
        self.check_object_permissions(request, my_question)
        srz_data = QuestionSerializer(
            instance=my_question, data=request.data, partial=True
        )
        if srz_data.is_valid():
            srz_data.save()
            return Response(srz_data.data, status=status.HTTP_200_OK)
        return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDeleteView(APIView):
    permission_classes = [
        IsOwnerOrReadOnly,
    ]

    def delete(self, request, pk):
        question = Question.objects.get(pk=pk)
        question.delete()
        return Response({"message": "question deleted"}, status=status.HTTP_200_OK)
