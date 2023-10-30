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
        return f"{self.cohort.cohort_name} ({self.cohort.id}) - {self.user.username}"       


class Exam(models.Model):
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=50)
    exam_duration = models.DurationField(default=timedelta(minutes=30))
    exam_availabilty = models.DurationField(default=timedelta(days=1))

    def __str__(self):
        return f"{self.exam_name} - {self.cohort.cohort_name}.{self.cohort.id}"        
    