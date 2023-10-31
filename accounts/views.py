from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from accounts.models import Cohort
from accounts.models import JoinedCohort
from accounts.serializer import CohortSerializer
from accounts.serializer import JoinedCohortSerializer
from rest_framework.permissions import IsAuthenticated



@permission_classes([IsAuthenticated])
def cohorts(request):
    #invoke serializer
    data = Cohort.objects.all()
    serializer = CohortSerializer(data, many=True)
    return JsonResponse({'cohorts': serializer.data})


@permission_classes([IsAuthenticated])
def joined_cohorts(request):
    #invoke serializer
    data = JoinedCohort.objects.all()
    serializer = JoinedCohortSerializer(data, many=True)
    return JsonResponse({'joined_cohorts': serializer.data})

