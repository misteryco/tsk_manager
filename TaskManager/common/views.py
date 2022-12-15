from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import mixins as auth_mixins, get_user_model
# from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic as views
from TaskManager.common.forms import NewsCommentForm, NewsCreateForm
from TaskManager.common.models import ShortNewsArticle

UserModel = get_user_model()


class HomePage(views.ListView):
    model = UserModel
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        news = ShortNewsArticle.objects.all().order_by('-pk')
        context['news'] = news
        context['comment_form'] = NewsCommentForm()
        return context


class NewsCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    template_name = 'base/base-create-view.html'
    form_class = NewsCreateForm

    success_url = reverse_lazy('home page')

    def form_valid(self, form):
        news = form.save(commit=False)
        # 2:
        # We add info about the current user News.user field
        news.user = self.request.user
        # 3:
        # Now we can populate autogenerated id field
        news.save()
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create News'
        context['form__button_title'] = 'CREATE'
        if not self.request.user.is_general_manager:
            raise PermissionDenied()
        return context


@login_required
def comment_article(request, pk):
    # We can use default article get:
    # article = ShortNewsArticle.objects.filter(pk=pk).get()
    # or we can use django shortcuts : get_object_or_404
    article = get_object_or_404(ShortNewsArticle, pk=pk)

    form = NewsCommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)  # Does not persist to DB
        comment.commented_section = article
        comment.comment_user = request.user
        comment.save()

    return redirect('home page')


# def home_page(request):
#     news = ShortNewsArticle.objects.all()
#     users = UserModel.objects.all()
#     if request.method == "POST":
#         comment_form = NewsCommentForm(request.POST)
#         if comment_form.is_valid():
#             comment = comment_form.save(commit=False)
#             comment.comment_user = request.user
#             comment_form.save()
#             return redirect('home page')
#     else:
#         comment_form = NewsCommentForm()
#
#     context = {
#         'news': news,
#         'object_list': users,
#         'comment_form': comment_form,
#     }
#     return render(request, template_name='index.html', context=context)


class NewsDetailView(auth_mixins.LoginRequiredMixin, views.DetailView):
    template_name = 'common/news-details.html'
    model = ShortNewsArticle


def news_delete(request, pk):
    # We can use default article get:
    # article = ShortNewsArticle.objects.filter(pk=pk).get()
    # or we can use django shortcuts : get_object_or_404,
    # or we can use custom exception handler
    try:
        vacation = ShortNewsArticle.objects.filter(pk=pk).get()
    except ObjectDoesNotExist as ex:
        raise Http404
    vacation.delete()
    return redirect('home page')


class NewsEditView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = ShortNewsArticle
    template_name = 'base/base-edit-view.html'
    fields = ['news_Title', 'news_article', ]
    success_url = reverse_lazy('home page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit News'
        context['form__button_title'] = 'EDIT'
        if not self.request.user.is_general_manager:
            raise PermissionDenied()
        return context
