from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta


class Cohort(models.Model):
    cohort_name = models.CharField(max_length=50)
    cohort_creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cohort_name} ({self.id})"
    
class JoinedCohort(models.Model):
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cohort.cohort_name} ({self.cohort.id}) - {self.user.username}({self.user.id})"     
    class Meta:
        unique_together = ('cohort', 'user')  


class Exam(models.Model):
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=50)
    duration = models.DurationField(default=timedelta(minutes=30))


    def __str__(self):
        return f"{self.exam_name} - {self.cohort.cohort_name}.{self.cohort.id}"  

class MCQ(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    option1 = models.CharField(max_length=50)
    option2 = models.CharField(max_length=50)
    option3 = models.CharField(max_length=50)
    option4 = models.CharField(max_length=50)
    answer = models.CharField(max_length=50)
    marks = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.question} - {self.exam.exam_name} {self.exam.cohort.cohort_name}({self.exam.cohort.id})"

class AnswerMCQ(models.Model):
    mcq = models.ForeignKey(MCQ, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=50)

    def is_correct(self):
        return self.selected_option == self.mcq.answer
    
    class Meta:
        unique_together = ('mcq', 'user')

class Attended(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date_taken = models.DateTimeField(auto_now_add=True)

    def calculate_score(self):
        answers = AnswerMCQ.objects.filter(user=self.user, mcq__exam=self.exam)
        score = sum(answer.mcq.marks for answer in answers if answer.is_correct())
        self.score = score
        self.save()

    def __str__(self):
        return f"{self.exam.exam_name} - {self.user.username}({self.user.id})"  
    class Meta:
        unique_together = ('exam', 'user')
