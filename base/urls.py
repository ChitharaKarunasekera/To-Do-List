from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage  # Views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # paths for login logout and registration
    path('login/', CustomLoginView.as_view(), name='login'),  # Login page
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Log-out page
    path('register', RegisterPage.as_view(), name='register'),  # register page

    # paths for tasks
    path('', TaskList.as_view(), name='tasks'),  # List of tasks
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),  # Detailed Task
    path('task-create/', TaskCreate.as_view(), name='tasks-create'),  # Create Tasks
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),  # Update Task
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),  # Delete Task
]
