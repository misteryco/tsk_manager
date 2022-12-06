from django import forms

from TaskManager.common.models import NewsComment, TaskComment, ShortNewsArticle


class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = ('news_comment',)
        widgets = {
            'news_comment': forms.Textarea(
                attrs={
                    'cols': 20,
                    'rows': 5,
                    'placeholder': 'Comment the news....',
                }
            )
        }


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = '__all__'
        # widgets = {
        #     'task_comment': forms.Textarea(
        #         attrs={
        #             'cols': 30,
        #             'rows': 5,
        #             'placeholder': 'Comment the task....',
        #         }
        #     )
        # }


class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = ShortNewsArticle
        exclude = ('user', 'date_and_time_of_article',)
