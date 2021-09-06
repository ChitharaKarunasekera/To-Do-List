from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView  # import login view from Django

from django.contrib.auth.mixins import LoginRequiredMixin  # Use Mixin to Restrict users (users that are not logged in)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task


#   login
class CustomLoginView(LoginView):
    template_name = 'base/login.html'  # html template
    fields = '__all__'  # display all fields
    redirect_authenticated_user = True  # redirect authenticated users to the todolist page

    # Override success url
    def get_success_url(self):
        return reverse_lazy('tasks')  # sends the users to tasks page


# registration
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm  # Django builtin UserCreation form
    redirect_authenticated_user = True  # Redirect authenticated users
    success_url = reverse_lazy('tasks')  # authenticated users are sent to tasks page

    # redirects user when the form is submitted
    def form_valid(self, form):
        user = form.save()

        # if user was successfully created, call login function
        if user is not None:
            login(self.request, user)  # authenticate user
        return super(RegisterPage, self).form_valid(form)

    # override get method and redirect authenticated users, to avoid them seeing the register page
    def get(self, *args, **kwargs):

        # if the user is an authenticated user, redirect them to tasks page
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, *kwargs)


# TaskList Inherits the ListView
class TaskList(LoginRequiredMixin, ListView):
    model = Task  # model name
    context_object_name = 'tasks'  # changing query set name (object_list) to 'tasks'

    # customise data according to user (User specific data)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(
            user=self.request.user)  # Getting items that are relevant to this particular user
        context['count'] = context['tasks'].filter(
            complete=False).count()  # Getting the count of incomplete items of that  particular user

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input

        return context


# To view detailed version of tasks, Inherited from detailed view
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'  # Setting template name to task.html


# To Create Tasks, Inherited from CreateView
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']  # creates a from with the fields to show
    success_url = reverse_lazy('tasks')

    #
    def form_valid(self, form):
        form.instance.user = self.request.user  # get the logged user
        return super(TaskCreate, self).form_valid(form)


# Update Tasks
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = fields = ['title', 'description', 'complete']  # list fields to show
    success_url = reverse_lazy('tasks')


# delete tasks
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
