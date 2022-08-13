from django.urls import path
from .views import SignUp, TaskHistorial, TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, LogIn
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(TaskList.as_view()), name="index"),
    path('iniciar-sesion', LogIn.as_view(), name="login"),
    path('cerrar-sesion', login_required(LogoutView.as_view(next_page="login")), name="logout"),
    path('registrarse', SignUp.as_view(), name="signup"),
    path('historial-tareas', login_required(TaskHistorial.as_view()) ,name="historial"),
    path('tarea/<int:pk>/', login_required(TaskDetail.as_view()), name="task"),
    path('crear-tarea', login_required(TaskCreate.as_view()), name="create"),
    path('editar-tarea/<int:pk>/', login_required(TaskUpdate.as_view()), name="update"),
    path('eliminar-tarea/<int:pk>/', login_required(TaskDelete.as_view()), name="delete"),
]

