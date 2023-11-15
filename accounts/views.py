from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate
from rest_framework import status
from accounts.models import Cohort
from accounts.models import JoinedCohort
from accounts.models import Exam
from accounts.models import MCQ
from accounts.models import AnswerMCQ
from accounts.models import Attended
from accounts.serializer import UserSerializer
from accounts.serializer import CohortSerializer
from accounts.serializer import JoinedCohortSerializer
from accounts.serializer import ExamSerializer
from accounts.serializer import MCQSerializer
from accounts.serializer import AnswerMCQSerializer
from accounts.serializer import AttendedSerializer

#token customization
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user.id,
        }
        return Response(tokens, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#end of token customization

@api_view(['POST'])
def register(request):
    seriallizer = UserSerializer(data=request.data)
    if seriallizer.is_valid():
        user = seriallizer.save()
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user.id,
        }
        return Response(tokens,status=status.HTTP_201_CREATED) 
    return Response(seriallizer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def cohorts(request):
    if request.method == 'GET':
        data = Cohort.objects.filter(cohort_creator=request.user)
        serializer = CohortSerializer(data, many=True)
        return Response({'cohorts': serializer.data})
    
    elif request.method == 'POST':
        serializer = CohortSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'cohort' : serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def joined_cohorts(request):
    if request.method == 'GET':
        data = JoinedCohort.objects.filter(user=request.user)
        serializer = JoinedCohortSerializer(data, many=True)
        return Response({'Joined_cohorts': serializer.data})
   
    elif request.method == 'POST':
        # Get the cohort the user is trying to join
        cohort_id = request.data.get('cohort')

        # Check if the user is the creator of the cohort they are trying to join
        if Cohort.objects.filter(cohort_creator=request.user, id=cohort_id).exists():
            return Response({'detail': 'A creator cannot join their own cohort.'}, status=status.HTTP_400_BAD_REQUEST)

        
        serializer = JoinedCohortSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Joined_cohort' : serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def cohort(request,id):
    try:
        data = Cohort.objects.get(pk=id)
    except Cohort.DoesNotExist:
        raise Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CohortSerializer(data)
        return Response({'cohort': serializer.data})

    elif request.method == 'DELETE':
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'POST':
        serializer = CohortSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'customer': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def cohort_users(request, cohort_id):
    try:
        cohort = Cohort.objects.get(id=cohort_id)
        data = JoinedCohort.objects.filter(cohort__id=cohort_id)
    except Cohort.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        users = [jc.user for jc in data]
        user_serializer = UserSerializer(users, many=True)
        cohort_serializer = UserSerializer(cohort.cohort_creator)
        return Response({'creator': cohort_serializer.data, 'users': user_serializer.data})
    

@api_view(['GET','POST','DELETE'])
#@permission_classes([IsAuthenticated])
def exams(request, id):
    try:
        exam = Exam.objects.get(id=id)
    except Exam.DoesNotExist:
        return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExamSerializer(exam)
        return Response(serializer.data)

    elif request.method in ['POST', 'DELETE']:
        # Check if the request.user is the creator of the cohort
        if exam.cohort.cohort_creator != request.user:
            return Response({'detail': 'Only the creator of the cohort can modify or delete the exam.'}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'POST':
            serializer = ExamSerializer(exam, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            exam.delete()
            return Response({'detail': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def create_exam(request):
    # Check if the request.user is the creator of the cohort
    cohort_id = request.data.get('cohort')
    cohort = Cohort.objects.get(id=cohort_id)
    if cohort.cohort_creator != request.user:
        return Response({'detail': 'Only the creator of the cohort can create an exam.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = ExamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def exams_by_cohort(request, cohort_id):
    exams = Exam.objects.filter(cohort__id=cohort_id)
    serializer = ExamSerializer(exams, many=True)
    return Response(serializer.data)

#QUESTION GET
@api_view(['GET','POST','DELETE'])
#@permission_classes([IsAuthenticated])
def exam_questions(request, exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        mcq = MCQ.objects.filter(exam=exam)
        serializer = MCQSerializer(mcq, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Check if the request.user is the creator of the cohort
        if exam.cohort.cohort_creator != request.user:
            return Response({'detail': 'Only the creator of the cohort can create an exam.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = MCQSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Check if the request.user is the creator of the cohort
        if exam.cohort.cohort_creator != request.user:
            return Response({'detail': 'Only the creator of the cohort can create an exam.'}, status=status.HTTP_403_FORBIDDEN)

        question_id = request.data.get('id')
        question = MCQ.objects.get(id=question_id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#ANSWER GET
@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])
def answer_mcq(request):
    if request.method == 'GET':
        answers = AnswerMCQ.objects.all()
        serializer = AnswerMCQSerializer(answers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AnswerMCQSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#USER ANSWSER IN ONE EXAM   
@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def user_exam_answers(request, user_id, exam_id):
    answers = AnswerMCQ.objects.filter(user_id=user_id, mcq__exam_id=exam_id)
    serializer = AnswerMCQSerializer(answers, many=True)
    return Response(serializer.data)

#ATTENDED EXAM
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def attended_exam(request, exam_id):
    if request.method == 'GET':
        attended = Attended.objects.filter(exam_id=exam_id)
        serializer = AttendedSerializer(attended, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AttendedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)