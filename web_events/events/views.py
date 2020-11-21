from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, get_list_or_404
from django.views.generic import TemplateView, ListView, CreateView, FormView, DetailView
from .models import Events, Category, JoinModelButton
from django.urls import reverse_lazy, reverse
from django import forms
from .forms import CreateEventForm, EventPostModelForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone


# from django.contrib.auth import get_user_model


def home_page_view(request):
    template_name = 'events/home.html'
    events = Events.objects.eventtime()[0:3]
    # events = get_list_or_404(Events)[0:3]
    context = {'events': events}
    return render(request, template_name, context)

def get_qs(request, event):
    if event.join.filter(id=request.user.pk).exists():
        return True
    return False


@login_required
def create_event(request):
    form = EventPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        print(form.cleaned_data)
        obj = form.save(commit=False)
        obj.category = form.cleaned_data.get('category')
        obj.author = request.user
        obj.save()
        form = EventPostModelForm()
    template_name = 'events/create.html'
    context = {'form': form}
    return render(request, template_name, context)


@staff_member_required
def event_post_update_view(request, pk):
    obj = get_object_or_404(Events, id=pk)
    form = EventPostModelForm(request.POST or None, request.FILES or None,
                              instance=obj)  # request.FILES - to work with images
    if form.is_valid():
        obj = form.save(commit=False)
        obj.cover = form.cleaned_data.get('cover')
        form.save()
    template_name = 'events/create.html'
    context = {'form': form, 'title': f'Update {obj.title}'}
    return render(request, template_name, context)


@staff_member_required()
def event_post_delete_view(request, pk):
    obj = get_object_or_404(Events, id=pk)
    template_name = 'events/delete.html'
    if request.method == 'POST':
        obj.delete()
        return redirect('/')
    context = {'object': obj}
    return render(request, template_name, context)


def my_event_list(request):
    template_name = 'events/list_view.html'
    events = Events.objects.filter(author=request.user)
    context = {'events': events}
    return render(request, template_name, context)


def detail_event(request, pk):
    template_name = 'events/detail_events.html'
    event = get_object_or_404(Events, id=pk)
    is_joined = False
    if event.join.filter(id=request.user.pk).exists():
        is_joined = True
    total_members = Events.total_members(event)
    context = {'event': event, 'is_joined': is_joined, 'total_members': total_members}
    return render(request, template_name, context)


def join_event(request):
    user = request.user
    if request.method == 'POST':
        event_id = request.POST.get('event_pk')
        event = get_object_or_404(Events, id=request.POST.get('event_pk'))
        if user in event.join.all():
            event.join.remove(user)
        else:
            event.join.add(user)
    joined, created = JoinModelButton.objects.get_or_create(user=user, event_id=event_id)
    if not created:
        if joined.value == 'Join':
            joined.value = 'UnJoin'
        else:
            joined.value = 'Join'
    joined.save()
    # success_url = reverse_lazy('event_detail', kwargs={'pk': event.id})
    success_url = reverse_lazy('home')
    return HttpResponseRedirect(success_url)


def members_list(request, pk):
    template_name = 'events/members_list.html'
    event = get_object_or_404(Events, id=pk)
    members = JoinModelButton.objects.filter(event=pk, value='Join')
    context = {'members': members, 'event': event}
    return render(request, template_name, context)
