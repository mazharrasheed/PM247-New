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

# class UserWithEngineerAvailability(User):
#     class Meta:
#         proxy = True
#     def save(self, *args, **kwargs):
#         created = not self.pk  # Check if the user is being created for the first time
#         super().save(*args, **kwargs)  # Call the original save method
#         if created:  # If the user is newly created, create an Engineer_Availability instance
#             Engineer_Availability.objects.create(engineer=self)

class SearchEngineerForm(forms.Form):
    job_type = forms.ModelChoiceField(queryset=Job_Type.objects.all(), required=False ,label="Job Type")
    post_code = forms.ModelChoiceField(queryset=Post_Code.objects.all(), required=False,label="Post Code")
    rating = forms.IntegerField(min_value=0, max_value=5, required=False)

    
    def __init__(self, *args, **kwargs):
        super(SearchEngineerForm, self).__init__(*args, **kwargs)
       
        self.fields['job_type'].empty_label = "Select Job Type"
        self.fields['post_code'].empty_label = "Select Post Code"
        
class EditUserWithEngineer(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        labels={'email':'Email'}

    

class UserWithEngineerForm(UserCreationForm):
    username = forms.CharField(max_length=150, label=_("Username"))
    email = forms.EmailField(required=True, label=_("Email"))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': _('Email')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None  # Remove password help text
        self.fields['password2'].help_text = None  # Remove password confirmation help text

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create Engineer_Availability instance
            Engineer_Availability.objects.create(engineer=user)
        return user

class EngineerAvailabilityForm(forms.ModelForm):
    jobs = forms.ModelMultipleChoiceField(queryset=Job_Type.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-select selectpicker', 'multiple aria-label':"Default select example",'data-live-search':"true"}))
    cities = forms.ModelMultipleChoiceField(queryset=Post_Code.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-select selectpicker','multiple aria-label':"Default select example",'data-live-search':"true"}))

    class Meta:
        model = Engineer_Availability
        exclude = ['engineer']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('jobs', css_class='form-control '),
            Field('cities', css_class='form-control'),
            Field('date', css_class='form-control'),
            Field('start_time', css_class='form-control'),
            Field('end_time', css_class='form-control'),
            Submit('submit', 'Save')
        )
        self.fields['jobs'].label = 'Job Type'
        self.fields['cities'].label = 'Post Code'
        self.fields['rating'].label = 'Rating'
        self.fields['start_time'].label = 'Add Start Time'
        self.fields['end_time'].label = 'Add End Time'
        self.fields['date'].label = 'Date'

class CustUserCreationForm1(UserCreationForm):

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

class CustUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class CustomUserCreationForm(UserCreationForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(content_type__id__in=[4, 9]),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email','password1', 'password2',  'permissions']
        labels = {'email': 'Email'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['permissions'].initial = self.instance.user_permissions.values_list('pk', flat=True)

        permissions = Permission.objects.filter(content_type__id__in=[4, 9])
        self.fields['permissions'].label = 'Permissions'
        self.fields['permissions'].queryset = permissions
        self.fields['permissions'].widget.choices = [(p.pk, p.name) for p in permissions]
    
class EditUserPrifoleForm(UserChangeForm):
    
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(content_type__id__in=[4, 9]),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','permissions']
        labels={'email':'Email'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial permissions for the user
        if self.instance.pk:
            self.fields['permissions'].initial = self.instance.user_permissions.values_list('pk', flat=True)

        permissions = Permission.objects.filter(content_type__id__in=[4,9])
        self.fields['permissions'].label = 'Permissions'
        self.fields['permissions'].queryset = permissions
        self.fields['permissions'].widget.choices = [(p.pk, p.name) for p in permissions]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            # user.set_password(self.cleaned_data["password"])
            user.save()
            # Save many-to-many relationships (permissions)
            self.save_permissions(user)
            self.save_m2m()  # Save any many-to-many relationships for the user
        return user

    def save_permissions(self, user):
        # Clear existing permissions
        user.user_permissions.clear()
        # Add selected permissions
        permissions = self.cleaned_data['permissions']
        for permission in permissions:
            user.user_permissions.add(permission)  

