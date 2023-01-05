from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


def my_custom_error_view(request):
    return render(request, '404.html', status=500)

