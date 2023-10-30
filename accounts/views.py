from accounts.models import Cohort
from django.http import JsonResponse
from accounts.serializer import CohortSerializer

def accounts(request):
    #invoke serializer
    data = Cohort.objects.all()
    serializer = CohortSerializer(data, many=True)
    return JsonResponse({'accounts': serializer.data}, safe=False)

