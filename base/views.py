from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')



class SignupFormView(FormView):
    template_name = 'base/signup.html'
    form_class = UserCreationForm
    # redirect_authenticated_user = True
    success_url = reverse_lazy('tasks') 

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignupFormView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(SignupFormView, self).get(*args, **kwargs)




class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'base/task-list.html'
    context_object_name = 'task_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_list'] = context['task_list'].filter(user=self.request.user)
        context['count'] = context['task_list'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['task_list'] = context['task_list'].filter(
                title__startswith=search_input)

        context['search_input'] = search_input
        return context




class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'base/task-detail.html'
    context_object_name = 'task'




class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'base/task-create.html'
    fields = ('title', 'description', 'complete')
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)




class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'base/task-update.html'
    fields = ('title', 'description', 'complete')
    success_url = reverse_lazy('tasks')




class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task-delete.html'
    success_url = reverse_lazy('tasks')