"""
URL configuration for accounts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/register/', views.register, name='register'),
    path('api/login/', views.login, name='login'),
    path('api/cohorts/', views.cohorts, name='cohorts'),
    path('api/cohorts/<int:id>/', views.cohort, name='cohort'),
    path('api/cohorts/<int:cohort_id>/users/',views.cohort_users, name='cohort_users'),
    path('api/joined/', views.joined_cohorts, name='joined_cohorts'),
    path('api/exams/<int:id>/', views.exams, name='exams'),
    path('api/exam/cohort/<int:cohort_id>/', views.exams_by_cohort, name='exams_by_cohort'),
    path('api/exam/<int:exam_id>/questions/', views.exam_questions, name='exam_questions'),
    path('api/answer/mcq/', views.answer_mcq, name='answer_mcq'),
    path('api/exam/answers/<int:user_id>/<int:exam_id>/', views.user_exam_answers, name='user_exam_answers'),
]
