from rest_framework import serializers
from accounts.models import Cohort
from accounts.models import JoinedCohort
from accounts.models import Exam
from accounts.models import Attended
from accounts.models import MCQ
from accounts.models import AnswerMCQ
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password']
        
    def create(self, validated_data):
        user = User.objects.create_user(
             username= validated_data['username'], 
             email= validated_data['email'],
            )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

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
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = {
            'user_id' : instance.user.id,
            'username' : instance.user.username,
        }
        representation['exam'] = {
            'exam_id' : instance.exam.id,
            'exam_name' : instance.exam.exam_name,
        }

class MCQSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQ
        fields = ['id','exam', 'question', 'option1', 'option2', 'option3', 'option4', 'answer', 'marks']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['exam'] = {
            'exam_id' : instance.exam.id,
            'exam_name' : instance.exam.exam_name,
        }
        return representation

class AnswerMCQSerializer(serializers.ModelSerializer):
    is_correct = serializers.SerializerMethodField()
    class Meta:
        model = AnswerMCQ
        fields = ['id','mcq', 'user', 'selected_option', 'is_correct']
    
    def get_is_correct(self, obj):
        return obj.is_correct()