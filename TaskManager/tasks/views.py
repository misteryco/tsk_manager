from django.contrib.auth import views as auth_views, get_user_model, mixins
from django.contrib.auth.decorators import login_required
from django.contrib.auth import mixins as auth_mixins
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic import FormView

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
            search_pattern = search_form.cleaned_data['search_in_task_name']
    else:
        search_form = TaskSearchForm()

    tasks = Task.objects.all()

    if search_pattern:
        # TODO: add serach vector with postgree
        # >> > from django.contrib.postgres.search import SearchVector
        # >> > Entry.objects.annotate(
        #     ...
        # search = SearchVector('body_text', 'blog__tagline'),
        #          ... ).filter(search='Cheese')
        # [ < Entry: Cheese
        # on
        # Toast
        # recipes >, < Entry: Pizza
        # Recipes >]
        tasks = tasks.filter(name__icontains=search_pattern)

    context = {
        "object_list": tasks,
        "search_form": search_form,
        "total_tasks": len(tasks),
    }
    return render(request, template_name='tasks/list_tasks.html', context=context)


class TasksListView(views.ListView, FormView):
    model = Task
    template_name = 'tasks/list_tasks.html'
    form_class = TaskSearchForm
    search_pattern = None
    form = form_class()
    success_url = reverse_lazy('tasks list')

    # success_url = reverse_lazy('tasks list')

    def form_valid(self, form):
        self.search_pattern = form.cleaned_data['search_in_task_name']
        return HttpResponse(self.get_context_data)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.search_pattern:
            context['object_list'] = context['object_list'].filter(name__icontains=self.search_pattern)
        context['total_tasks'] = self.model.objects.count
        context['search_form'] = self.form

        return context


# @login_required
class TasksCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    template_name = 'tasks/task_create.html'
    form_class = TasksCreateForm

    success_url = reverse_lazy('tasks list')

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        task.attached_file_by_author = 'task{0}/{1}/{2}'.format(task.id,
                                                                self.request.user.username,
                                                                task.attached_file_by_author
                                                                )
        form.save()
        return super().form_valid(form)


class TaskEditView(views.UpdateView):
    template_name = 'tasks/task-edit.html'
    model = Task
    fields = ('name', 'description', 'due_date', 'priority', 'attached_file_by_author', 'attached_file_by_executor',
              'executor')

    def get_success_url(self):
        return reverse_lazy(
            'task detail',
            kwargs={'pk': self.object.pk})


class TaskDetailsView(views.DetailView):
    template_name = 'tasks/task-details.html'
    model = Task
