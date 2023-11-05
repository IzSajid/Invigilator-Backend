from accounts.models import User
from accounts.models import Cohort
from accounts.models import JoinedCohort
from accounts.serializer import UserSerializer
from accounts.serializer import CohortSerializer
from accounts.serializer import JoinedCohortSerializer
from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET','POST'])
#@permission_classes([IsAuthenticated])
def cohorts(request):
    if request.method == 'GET':
        data = Cohort.objects.all()
        serializer = CohortSerializer(data, many=True)
        return Response({'cohorts': serializer.data})
    
    elif request.method == 'POST':
        serializer = CohortSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'cohort' : serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','POST'])
#@permission_classes([IsAuthenticated])
def joined_cohorts(request):
    if request.method == 'GET':
        data = JoinedCohort.objects.all()
        serializer = JoinedCohortSerializer(data, many=True)
        return Response({'Joined_cohorts': serializer.data})
   
    elif request.method == 'POST':
        serializer = JoinedCohortSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Joined_cohort' : serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST','DELETE'])
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