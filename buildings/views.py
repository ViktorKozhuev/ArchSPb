from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .forms import CreateCommentForm
from .models import Building, Architect, Archstyle, Street
from users.models import Profile


class BuildingsHome(ListView):
    model = Building
    template_name = 'buildings/index.html'
    context_object_name = 'buildings'
    extra_context = {'title': 'Главная страница'}

    def get_queryset(self):
        return Building.objects.filter(draft=False).select_related('archstyle').order_by('-time_create')[:2]


class BuildingsCategory(ListView):
    model = Building
    template_name = 'buildings/buildings_list.html'
    context_object_name = 'buildings'
    allow_empty = False

    def get_queryset(self):
        return Building.objects.filter(category__url=self.kwargs['category_url'],
                                       draft=False).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Категория: " + str(context['buildings'][0].category)
        return context


class Architects(ListView):
    model = Architect
    template_name = 'buildings/architects_list.html'
    context_object_name = 'architects'
    extra_context = {'title': 'Архитекторы'}

    def get_queryset(self):
        return Architect.objects.all()


class ArchStyles(ListView):
    model = Architect
    template_name = 'buildings/archstyles_list.html'
    context_object_name = 'archstyles'
    extra_context = {'title': 'Архитектурные стили'}

    def get_queryset(self):
        return Archstyle.objects.all()


class Streets(ListView):
    model = Street
    template_name = 'buildings/streets_list.html'
    context_object_name = 'streets'
    extra_context = {'title': 'Улицы'}

    def get_queryset(self):
        return Street.objects.all()


class BuildingsArchitect(ListView):
    model = Building
    template_name = 'buildings/buildings_list.html'
    context_object_name = 'buildings'
    slug_field = "slug"
    allow_empty = False
    paginate_by = 3

    def get_queryset(self):
        return Building.objects.filter(architect__slug=self.kwargs['slug'],
                                       draft=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Архитектор: " + str(context['buildings'][0].architect.filter(slug=self.kwargs['slug'])[0])
        return context


class BuildingsArchStyle(ListView):
    model = Building
    template_name = 'buildings/buildings_list.html'
    context_object_name = 'buildings'
    slug_field = "slug"
    allow_empty = False

    def get_queryset(self):
        return Building.objects.filter(archstyle__slug=self.kwargs['slug'],
                                       draft=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Архитектурный стиль: " + str(context['buildings'][0].archstyle)
        return context


class ShowBuilding(DetailView):
    model = Building
    template_name = 'buildings/building.html'
    slug_field = "url"
    context_object_name = 'building'


class BuildingsStreet(ListView):
    model = Building
    template_name = 'buildings/buildings_list.html'
    context_object_name = 'buildings'
    slug_field = "slug"
    allow_empty = False

    def get_queryset(self):
        return Building.objects.filter(street__slug=self.kwargs['slug'],
                                       draft=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Улица: " + str(context['buildings'][0].street.filter(slug=self.kwargs['slug'])[0])
        return context


@login_required
def add_comment(request, pk):
    building = Building.objects.get(id=pk)
    if request.method == 'POST':
        post = {
            'user': request.user.id,
            'profile': Profile.objects.get(user_id=request.user.id).id,
            'comment': request.POST['comment'],
            'building': Building.objects.get(id=pk).id
        }

        form = CreateCommentForm(post)
        if request.POST.get("parent", None):
            post['parent'] = int(request.POST.get("parent"))
        if form.is_valid():
            form.save()
            return redirect(building.get_absolute_url())
    else:
        return HttpResponse(status=405)
    return HttpResponse(status=500)
