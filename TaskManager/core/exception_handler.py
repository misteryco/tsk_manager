from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, template_name='base/404.html', status=404)
