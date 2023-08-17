from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.db import models
from .models import User
from django.views.generic import TemplateView, CreateView, ListView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from floatapp.decorators import user_is_teacher, user_is_student

from .forms import CourseCreateForm, AssignmentCreateForm
from .models import Course, Assignment

# Create your views here.
def home(request):
    return render(request, 'course/home.html')

#COURSE CREATE VIEW
class CourseCreateView(CreateView):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    template_name = 'course/teacher/course_create.html'
    form_class = CourseCreateForm
    extra_context = {
        'title': 'New Course'
    }
    success_url = reverse_lazy('course:course')

    @method_decorator(login_required(login_url=reverse_lazy('/login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('/login')
        #if self.request.user.is_authenticated and self.request.user.role != 'teacher':
        #    return reverse_lazy('/login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CourseCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# VIEW FOR COURSE LIST
class CourseView(ListView):
    model = Course
    template_name = 'course/teacher/courses.html'
    context_object_name = 'course'

    @method_decorator(login_required(login_url=reverse_lazy('/login')))
    #@method_decorator(user_is_teacher, user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')  # filter(user_id=self.request.user.id).order_by('-id')


def course_single(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, "course/teacher/view_course.html", {'course': course})


# CREATE ASSIGNMENT VIEW
class AssignmentCreateView(CreateView):
    template_name = 'course/teacher/assignment_create.html'
    form_class = AssignmentCreateForm
    extra_context = {
        'title': 'New Course'
    }
    success_url = reverse_lazy('course:assignment-list')

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('floatapp:login')
        #if self.request.user.is_authenticated and self.request.user.role != 'instructor':
        #    return reverse_lazy('floatapp:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AssignmentCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# VIEW FOR ASSIGNMENT LIST
class AssignmentView(ListView):
    model = Assignment
    template_name = 'course/teacher/assignments.html'
    context_object_name = 'assignment'

    @method_decorator(login_required(login_url=reverse_lazy('floatapp:login')))
    # @method_decorator(user_is_student, user_is_instructor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()  # filter(user_id=self.request.user.id).order_by('-id')


