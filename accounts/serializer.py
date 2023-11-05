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
    cohort_creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Cohort
        fields = ['id','cohort_name', 'cohort_creator']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['cohort_creator'] = {
            'user_id' : instance.cohort_creator.id,
            'username' : instance.cohort_creator.username,
        }
        return representation

class JoinedCohortSerializer(serializers.ModelSerializer):
    cohort = serializers.PrimaryKeyRelatedField(queryset=Cohort.objects.all())
    class Meta:
        model = JoinedCohort
        fields = ['id','cohort','user']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['cohort'] = {
            'cohort_id' : instance.cohort.id,
            'cohort_name' : instance.cohort.cohort_name,
        }
        return representation

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id','cohort', 'exam_name', 'exam_duration', 'exam_availabilty']

class AttendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attended
        fields = ['id','exam', 'user', 'score', 'date_taken']

