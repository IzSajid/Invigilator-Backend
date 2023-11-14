from django.contrib import admin
from accounts.models import Cohort
from accounts.models import JoinedCohort
from accounts.models import Exam
from accounts.models import Attended
from accounts.models import MCQ
from accounts.models import AnswerMCQ


admin.site.register(Cohort)
admin.site.register(JoinedCohort)
admin.site.register(Exam)
admin.site.register(Attended)
admin.site.register(MCQ)
admin.site.register(AnswerMCQ)