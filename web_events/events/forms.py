from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import datetime
from .models import *
from django.utils.safestring import mark_safe


class CreateEventForm(forms.Form):
    title = forms.CharField(label='Title', max_length=50)  # required=False
    choise_event_type = [('offline event', 'offline event'), ('online event', 'online event')]
    event_type = forms.ChoiceField(choices=choise_event_type, widget=forms.RadioSelect)
    YEARS = [x for x in range(2020, 2022)]
    start_date = forms.DateField(label='Start date', initial=datetime.date.today,
                                 widget=forms.SelectDateWidget(years=YEARS))
    end_date = forms.DateField(label='End date', initial=datetime.date.today,
                               widget=forms.SelectDateWidget(years=YEARS))
    start_time = forms.TimeField(label='Start time', initial='08:00')
    end_time = forms.TimeField(label='End time', initial='08:00')
    description = forms.CharField(label='Description', min_length=4)
    location = forms.CharField(label='Location', max_length=200)
    host = forms.CharField(label='Host', max_length=30)
    cover = forms.FileField(label='Cover')
    choise_category_type = [('Film', 'Film'), ('Party', 'Party')]
    category = forms.CharField(label='Category', widget=forms.Select(choices=choise_category_type))

    # This is for a contact form
    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        if email.endswith('.edu'):
            raise forms.ValidationError('Please do not use .edu')
        return email

    # def clean(self):
    #     super(CreateEventForm, self).clean()
    #     discount = self.cleaned_data.get('discount')
    #     id = self.cleaned_data.get('id')
    #     if type(discount) != int:
    #         self._errors['discount'] = self.error_class(['Discount must be a integer'])
    #     discountFloat = discount/100
    #     print(discountFloat)
    #     prod = Product.objects.get(id=id)
    #     prod.price = prod.price - (prod.price*discountFloat)
    #     # don't forget to save the object after modifying
    #     prod.save()
    #     print(discount, id)
    #     return discount


class EventPostModelForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['title', 'event_type', 'start_date', 'end_date', 'start_time', 'end_time', 'description',
                  'location', 'host', 'category', 'cover', 'members_number']  # cover

    def clean_title(self, *args, **kwargs):
        instance = self.instance
        title = self.cleaned_data.get('title')
        qs = Events.objects.filter(title=title)
        if instance is not None:  # change the same object
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError('This title is already exists')
        return title


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfoModel
        fields = ['profile_pic']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), help_text=mark_safe("Required. 8-30 characters."),
                               label='Password')
    username = forms.CharField(
        help_text=mark_safe("Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only."), label='Username')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        if 8 <= len(password) <= 30:
            return password
        else:
            raise forms.ValidationError('The password should contain from 8-30 characters')

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('The user with this email already registered')
        return email

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        if len(username) > 50 or len(username) == 0:
            raise forms.ValidationError('The username cannot be empty or exceed 50 characters')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError('The user with this username already registered')
        return username


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']

    widgets = {
        'text': forms.TextInput(attrs={'class': 'editable medium-editor-textarea'})
    }
