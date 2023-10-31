from rest_framework import serializers
from accounts.models import Cohort
from accounts.models import JoinedCohort
from accounts.models import Exam
from accounts.models import Attended
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password']


class CohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = ['id','cohort_name', 'cohort_creator']

class JoinedCohortSerializer(serializers.ModelSerializer):
    cohort = CohortSerializer(read_only=True)
    class Meta:
        model = JoinedCohort
        fields = ['id','cohort', 'user']

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id','cohort', 'exam_name', 'exam_duration', 'exam_availabilty']

class AttendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attended
        fields = ['id','exam', 'user', 'score', 'date_taken']

