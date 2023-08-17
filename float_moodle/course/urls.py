from django.urls import path
from .views import (
home,
CourseView,
CourseCreateView,
course_single,
AssignmentCreateView,
AssignmentView,
)
from django.conf import settings
from django.conf.urls.static import static

app_name = "course"

urlpatterns = [
                  path('', home, name='home'),
                  path('course/', CourseView.as_view(), name='course'),
                  path('course-create/', CourseCreateView.as_view(), name='course-create'),
                  path('assignment-create/', AssignmentCreateView.as_view(), name='assignment-create'),
                  path('assignment/', AssignmentView.as_view(), name='assignment-list'),
                  path('<int:id>/course-view/', course_single, name='course-view'),
                  
                  #path('assignment-submission/', AssignmentSubmissionView.as_view(), name='assignment-submission'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
