
from django import forms
from django.contrib.auth.models import User, Permission,Group
from django.contrib.auth.forms import (UserChangeForm, UserCreationForm,
                                       UsernameField)
from django.contrib.auth import (authenticate, get_user_model,
                                 password_validation)
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Fieldset, Layout, Submit
from home.models import Engineer_Availability,Job_Type,Post_Code
from django.contrib.auth.models import User


class Enginer_Avail_Form(forms.ModelForm):
    class Meta:
        model=Engineer_Availability
        fields=['jobs','cities','rating','start_time','end_time','date']
        # labels={'email':'Email'}
        widgets = {
            'jobs': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'cities': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add IDs to form fields
        self.fields['jobs'].widget.attrs['id'] = 'id_jobs'
        self.fields['jobs'].label = 'Job Type'  # Differentiate label ID
        self.fields['cities'].widget.attrs['id'] = 'id_cities'
        self.fields['cities'].label = 'Post Code'  # Differentiate label ID
        self.fields['rating'].widget.attrs['id'] = 'id_rating'
        self.fields['rating'].label = 'Rating'  # Differentiate label ID
        self.fields['start_time'].widget.attrs['id'] = 'id_start_time'
        self.fields['start_time'].label = 'Add Start Time'  # Differentiate label ID
        self.fields['end_time'].widget.attrs['id'] = 'id_end_time'
        self.fields['end_time'].label = 'Add End Time'  # Differentiate label ID
        self.fields['date'].widget.attrs['id'] = 'id_date'
        self.fields['date'].label = 'Date'  # Differentiate label ID


class CustomUserCreationForm(UserCreationForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(content_type_id=6),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta(UserCreationForm.Meta):
        fields = ['username','email','password1', 'password2', 'permissions']
        labels = {'email': 'Email'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        permissions = Permission.objects.filter(content_type_id=6)
        self.fields['permissions'].label = 'Permissions'
        self.fields['permissions'].queryset = permissions
        self.fields['permissions'].widget.choices = [(p.pk, p.name) for p in permissions]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            self.save_permissions(user)
            self.save_m2m()  # Save any many-to-many relationships for the user
        return user

    def save_permissions(self, user):
        permissions = self.cleaned_data.get('permissions')
        if permissions:
            user.user_permissions.set(permissions)

class UserCreationFormWithPermissions(UserChangeForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(content_type_id=6),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    username=UsernameField()
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput()
        self.fields['password2'].widget = forms.PasswordInput()
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data["password"])
            user.save()
            self.save_m2m()  # Save many-to-many relationships (permissions)
        return user