from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, get_list_or_404, HttpResponse
from django.views.generic import TemplateView, ListView, CreateView, FormView, DetailView
from .models import Events, Category, JoinModelButton, UserProfileInfoModel, Comments
from django.urls import reverse_lazy, reverse
from django import forms
from .forms import CreateEventForm, EventPostModelForm, UserProfileInfoForm, UserForm, CommentsForm, SendEmailForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from itertools import chain
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils import timezone, dateformat
from django.core.mail import BadHeaderError, send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import resolve
from pathlib import Path
from email.mime.image import MIMEImage
import os
from email.mime.multipart import MIMEMultipart




# from django.contrib.auth import get_user_model


def home_page_view(request):
    '''home page with 3 upcoming events, available for all'''
    template_name = 'events/home.html'
    events = Events.objects.eventtime()[0:3]
    if request.user.is_authenticated:
        user_profile = UserProfileInfoModel.objects.get(user=request.user)
        context = {'events': events, 'user_profile': user_profile}
    # events = get_list_or_404(Events)[0:3]
    else:
        context = {'events': events}
    return render(request, template_name, context)


@login_required
def create_event(request):
    '''function to create a new event, available only for authorized users'''
    form = EventPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.category = form.cleaned_data.get('category')
        ##???
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        now = dateformat.format(timezone.now(), 'Y-m-d')
        start_date = dateformat.format(start_date, 'Y-m-d')
        end_date = dateformat.format(end_date, 'Y-m-d')
        if start_date > end_date:
            raise forms.ValidationError('Start date cannot be later than end date')
        if start_date < now:
            raise forms.ValidationError('Start date should be upcoming date')
        ##??
        obj.author = request.user
        obj.save()
        form = EventPostModelForm()
    template_name = 'events/create.html'
    user_profile = UserProfileInfoModel.objects.get(user=request.user)
    context = {'form': form, 'title': 'Create event', 'user_profile': user_profile}
    return render(request, template_name, context)


@login_required
def event_post_update_view(request, pk):
    '''function to edut/update event, only authorized creater can modify his event'''
    obj = get_object_or_404(Events, id=pk)
    form = EventPostModelForm(request.POST or None, request.FILES or None,
                              instance=obj)  # request.FILES - to work with images
    if form.is_valid():
        obj = form.save(commit=False)
        obj.cover = form.cleaned_data.get('cover')
        form.save()
    template_name = 'events/create.html'
    user_profile = UserProfileInfoModel.objects.get(user=request.user)
    context = {'form': form, 'title': f'Update -> {obj.title}', 'user_profile': user_profile}
    return render(request, template_name, context)


@login_required
def event_post_delete_view(request, pk):
    '''function to delete event, only authorized creater can delete his event'''
    obj = get_object_or_404(Events, id=pk)
    template_name = 'events/delete.html'
    if request.method == 'POST':
        obj.delete()
        return redirect('/')
    user_profile = UserProfileInfoModel.objects.get(user=request.user)
    context = {'object': obj, 'user_profile': user_profile}
    return render(request, template_name, context)


def detail_event(request, pk):
    '''detail description of the selected event, available for all'''
    template_name = 'events/detail_events.html'
    event = get_object_or_404(Events, id=pk)
    is_joined = False
    # if JoinModelButton.objects.filter(event=event).filter(user=request.user).filter(value='Join').exists():
    if event.join.filter(id=request.user.pk).exists():
        is_joined = True
    total_members = Events.total_members(event)
    if request.user.is_authenticated:
        user_profile = UserProfileInfoModel.objects.get(user=request.user)
        context = {'event': event, 'is_joined': is_joined, 'total_members': total_members, 'user_profile': user_profile}
    else:
        context = {'event': event, 'is_joined': is_joined, 'total_members': total_members}
    return render(request, template_name, context)


@login_required
def join_event(request):
    '''button join/unjoin, available only for authorized users'''
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
    '''See the list of all joined users for an event, available for all users'''
    template_name = 'events/members_list.html'
    event = get_object_or_404(Events, id=pk)
    members = JoinModelButton.objects.filter(event=pk, value='Join')
    if request.user.is_authenticated:
        user_profile = UserProfileInfoModel.objects.get(user=request.user)
        context = {'members': members, 'event': event, 'user_profile': user_profile}
    else:
        context = {'members': members, 'event': event}
    return render(request, template_name, context)


@login_required
def my_event_list(request):
    '''all events where authorized user is going or creater'''
    template_name = 'events/list_view.html'
    events = Events.objects.filter(author=request.user)
    events2 = JoinModelButton.objects.filter(user=request.user, value='Join')
    for event in events2:
        obj = Events.objects.filter(title=event)
        events = events | obj
    user_profile = UserProfileInfoModel.objects.get(user=request.user)
    context = {'events': events, 'user_profile': user_profile}
    return render(request, template_name, context)


def register(request):
    '''registration to the event website, available for all'''
    template_name = 'events/registration.html'
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST or None)
        profile_form = UserProfileInfoForm(request.POST or None)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.password = user_form.cleaned_data.get('password')
            profile.email = user_form.cleaned_data.get('email')
            profile.first_name = user_form.cleaned_data.get('first_name')
            profile.last_name = user_form.cleaned_data.get('last_name')
            profile.save()
            registered = True
            password = user_form.cleaned_data.get('password')
            user = authenticate(username=user.username, password=password)
            login(request, user)
            return redirect('/')

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, template_name,
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


@login_required
def add_comment(request, pk):
    '''add a new comment to the selected/detailed event, available only for authorized users'''
    template_name = 'events/comments.html'
    event = get_object_or_404(Events, id=pk)
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.author = request.user
            comment.save()
            return redirect('event_detail', pk=event.id)
    else:
        form = CommentsForm()
    user_profile = UserProfileInfoModel.objects.get(user=request.user)
    context = {'form': form, 'title': 'New comment', 'name_button': 'Add comment', 'user_profile': user_profile,
               'event': event}
    return render(request, template_name, context)


@login_required
def event_approve_comment(request, pk):
    '''approve created comment, before it nobody cannot see written comment. Creater or admin can approve it'''
    comment = get_object_or_404(Comments, id=pk)
    event_pk = comment.event.pk
    comment.approve()
    success_url = reverse_lazy('event_detail', kwargs={'pk': event_pk})
    return HttpResponseRedirect(success_url)


@login_required
def event_delete_comment(request, pk):
    '''delete comment, only authorized creator can delete it'''
    comment = get_object_or_404(Comments, id=pk)
    print('ok')
    event_pk = comment.event.pk
    comment.delete()
    success_url = reverse_lazy('event_detail', kwargs={'pk': event_pk})
    return HttpResponseRedirect(success_url)


@login_required
def event_comment_update(request, pk):
    '''edit/update comment, only authorized creator can edit/update it'''
    comment = get_object_or_404(Comments, id=pk)
    event_pk = comment.event.pk
    event = get_object_or_404(Events, id=event_pk)
    # print(event_pk)
    form = CommentsForm(request.POST or None, instance=comment)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.cover = form.cleaned_data.get('cover')
        form.save()
    template_name = 'events/comments.html'
    user_profile = UserProfileInfoModel.objects.get(user=request.user)
    context = {'form': form, 'title': 'Update comment', 'name_button': 'Update comment', 'event_pk': event_pk,
               'user_profile': user_profile, 'event': event}
    return render(request, template_name, context)


@login_required
def form_send_email(request, pk):
    '''the organizer of the event can send the email to all members who are going to his event'''
    template_name = 'events/send_email.html'
    event = get_object_or_404(Events, id=pk)
    members = JoinModelButton.objects.filter(event=pk, value='Join')
    obj = []
    for m in members:
        obj += UserProfileInfoModel.objects.filter(user=m.user)
        # obj += User.objects.filter(username=m.user)
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        if form.is_valid():
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            if subject and message:
                for o in obj:
                    print(o.email, o.user, o.first_name, o.last_name)
                    try:
                        if o.first_name:
                            c = {'title': subject, 'content': message, 'event': event, 'username': o.first_name,
                                 'sendler': request.user.username,
                                 'pk': pk}
                        else:
                            c = {'title': subject, 'content': message, 'event': event, 'username': o.user,
                                 'sendler': request.user.username, 'pk': pk}
                        html_content = render_to_string('templated_email/email.html', c)
                        text_content = strip_tags(html_content)
                        img_data = event.cover.read()
                        img = MIMEImage(img_data, _subtype="jpeg")
                        img.add_header('Content-ID', '<coupon_image>')
                        img.add_header('Content-Disposition', 'inline', filename="coupon_image")
                        email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [o.email], )
                        email.attach_alternative(html_content, "text/html")
                        email.mixed_subtype = 'related'
                        email.attach(img)

                        email.send()
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
            success_url = reverse_lazy('event_detail', kwargs={'pk': event.id})
            return HttpResponseRedirect(success_url)
        else:
            return HttpResponse('Make sure all fields are entered and valid.')
        return redirect('event_detail', pk=event.id)
    else:
        form = SendEmailForm()
    user_profile = UserProfileInfoModel.objects.get(user=request.user)
    context = {'form': form, 'title': 'Send email to all members', 'name_button': 'Send emails',
               'user_profile': user_profile, 'event': event}
    return render(request, template_name, context)
