from django.contrib.auth import mixins as auth_mixins, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from django.db.models import Q

from TaskManager.tasks.forms import TasksCreateForm, TaskSearchForm
from TaskManager.tasks.models import Task

UserModel = get_user_model()


@login_required
def task_list_funct_view(request):
    search_pattern = None

    # Search Form logic
    if request.method == 'POST':
        search_form = TaskSearchForm(request.POST)
        if search_form.is_valid():
            search_pattern = search_form.cleaned_data['search_in_task_name_or_description']
    else:
        search_form = TaskSearchForm()

    tasks = Task.objects.all()

    if search_pattern:
        tasks = tasks.filter(
            Q(name__icontains=search_pattern) |
            Q(description__icontains=search_pattern))

    tasks = tasks.order_by('due_date', 'priority', 'pk')

    context = {
        "object_list": tasks,
        "search_form": search_form,
        "total_tasks": len(tasks),
    }
    return render(request, template_name='tasks/list_tasks.html', context=context)


class TasksCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    template_name = 'base/base-create-view.html'
    form_class = TasksCreateForm

    success_url = reverse_lazy('tasks list')

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create Task'
        context['form__button_title'] = 'CREATE'
        return context

# @login_required
# def task_create_view(request):
#     if request.method == 'GET':
#         form = TasksCreateForm()
#     else:
#         form = TasksCreateForm(request.POST, request.FILES)
#         if form.is_valid():
#             photo = form.save(commit=False)  # form.save return object itself
#             photo.user = request.user
#             photo.save()
#             form.save()
#             return redirect(reverse_lazy('tasks list'))
#
#     context = {
#         'form': form,
#         'form_title': 'Create Vacation',
#         'form__button_title': 'CREATE',
#     }
#
#     return render(request, 'base/base-create-view.html', context)


class TaskEditView(views.UpdateView):
    template_name = 'base/base-edit-view.html'
    model = Task
    fields = ('name', 'description', 'due_date', 'priority', 'attached_file_by_author', 'attached_file_by_executor',
              'executor')

    def get_success_url(self):
        return reverse_lazy(
            'task detail',
            kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Task'
        context['form__button_title'] = 'EDIT'
        return context


class TaskDetailsView(views.DetailView):
    template_name = 'tasks/task-details.html'
    model = Task


def task_delete(request, pk):
    task = Task.objects.filter(pk=pk).get()
    task.delete()
    return redirect('tasks list')
