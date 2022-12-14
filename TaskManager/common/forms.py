from django import forms

from TaskManager.common.models import NewsComment, ShortNewsArticle


class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = ('news_comment',)


# Future extensibility with task comments
# class TaskCommentForm(forms.ModelForm):
#     class Meta:
#         model = TaskComment
#         fields = '__all__'
#

class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = ShortNewsArticle
        exclude = ('user', 'date_and_time_of_article',)
        widgets = {
            'news_Title': forms.TextInput(attrs={'placeholder': 'Title here...'}),
            'news_article': forms.Textarea(
                attrs={
                    'cols': 20,
                    'rows': 5,
                    'placeholder': '  Write here....',
                }
            ),
        }


class EditNewsForm(forms.ModelForm):
    class Meta:
        model = ShortNewsArticle
        exclude = ('user', 'date_and_time_of_article',)
        widgets = {
            'news_Title': forms.TextInput(attrs={'placeholder': 'Title here...'}),
            'news_article': forms.Textarea(
                attrs={
                    'cols': 20,
                    'rows': 5,
                    'placeholder': '  Write here....',
                }
            ),
        }
