from django.db import models
from floatapp.models import User
from django.utils import timezone
# Create your models here.


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    course_image = models.ImageField(upload_to='media')
    teacher_name = models.CharField(max_length=50)
    course_description = models.TextField()
    created_at = models.DateField(default=timezone.now)
    start_date = models.CharField(default=timezone.now, max_length=20)
    end_date = models.CharField(max_length=20)

    def __str__(self):
        return self.course_name

class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    marks = models.CharField(max_length=20)
    duration = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.title
