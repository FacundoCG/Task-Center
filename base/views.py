from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth import login

from .models import Task
from .forms import InicioForm, RegistroForm, TaskForm


# Create your views here.


class LogIn(LoginView):
    template_name = "base/iniciarSesion.html"
    form_class = InicioForm
    # fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("index")


class SignUp(FormView):
    template_name = "base/registro.html"
    form_class = RegistroForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignUp, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("index")
        return super(SignUp, self).get(*args, **kwargs)


class TaskList(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "base/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        context["guia"] = []

        cantidad_tareas = len(context["tasks"])

        if cantidad_tareas>5:
            context["guia"] = context["tasks"][cantidad_tareas-5:]
        else:
            context["guia"] = context["tasks"]
        
        return context


class TaskHistorial(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "base/historial.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)

        search_input = self.request.GET.get("search-area") or ""

        if search_input:
            context["tasks"] = context["tasks"].filter(title__icontains=search_input)

        context["search-input"] = search_input

        return context


class TaskDetail(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "base/tarea.html"


class TaskCreate(CreateView):
    form_class = TaskForm
    model = Task
    # fields = ['title','description','complete']
    template_name = "base/crearTarea.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "base/actualizarTarea.html"
    success_url = reverse_lazy("index")


class TaskDelete(DeleteView):
    model = Task
    context_object_name = "task"
    template_name = "base/eliminarTarea.html"
    success_url = reverse_lazy("index")
