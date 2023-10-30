from django.contrib import admin
from accounts.models import Cohort
from accounts.models import JoinedCohort
from accounts.models import Exam


admin.site.register(Cohort)
admin.site.register(JoinedCohort)
admin.site.register(Exam)