from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)

from .forms import CustUserCreationForm, EditUserPrifoleForm,EngineerAvailabilityForm, UserWithEngineerForm
from .forms import EditUserWithEngineer,SearchEngineerForm,CustomUserCreationForm
from django.contrib.auth.models import User,Group
from home.models import Engineer_Availability
from datetime import date,timedelta,time, datetime

# Create your views here.


class Login_View(LoginView):
    template_name='login.html'
    # success_url='dashboard'

def log_in(request):
    mydata = {}
    print("i m login")
    if request.method == 'POST':
      login_form = AuthenticationForm(request=request, data=request.POST)
      if login_form.is_valid():
        uname = login_form.cleaned_data['username']
        upass = login_form.cleaned_data['password']
        user = authenticate(username=uname, password=upass)
        if user is not None:
            login(request, user)
            print("i m login fdfd")
            messages.success(request, "You are successfuly Signin")
            if request.user.is_staff:
                return redirect("dashboard")
            else:
                return redirect('engrprofile')       
    else:
      login_form = AuthenticationForm()
    mydata = {'form': login_form}
    return render(request, "login.html", mydata)
 
def log_out(request):
    logout(request)
    return redirect('login')

@login_required
@permission_required('home.view_index')
def index(request):
    
        today = date.today()
        engineers=Engineer_Availability.objects.filter(date=today)
        # Filter engineers available today
        available_engineers_today = Engineer_Availability.objects.filter(date=today)
        # Example: Filter engineers available today for the job 'Plumbing'
        plumbing_engineers_today = available_engineers_today.filter(jobs__name='Plumbing')
        drainage_engineers_today = available_engineers_today.filter(jobs__name='Drainage')
        heating_engineers_today = available_engineers_today.filter(jobs__name='Heating')
        gas_engineers_today = available_engineers_today.filter(jobs__name='Gas')
        unvented_engineers_today = available_engineers_today.filter(jobs__name='Unvented')
        electricity_engineers_today = available_engineers_today.filter(jobs__name='Electricity')

        plumbing_qty=len(plumbing_engineers_today)
        drainage_qty=len(drainage_engineers_today)
        heating_qty=len(heating_engineers_today)
        gas_qty=len(gas_engineers_today)
        unvented_qty=len(unvented_engineers_today)
        electricity_qty=len(electricity_engineers_today)
        
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Filter Engineer_Availability queryset for the current week
        weekly_availability = Engineer_Availability.objects.filter(
            date__range=[start_of_week, end_of_week]
        )
        print(weekly_availability)

        # Calculate weekly total time availability for each engineer
        weekly_total_availability = {}
        for engineer_availability in weekly_availability:
            engineer = engineer_availability.engineer
            start_time = datetime.combine(today, engineer_availability.start_time)
            end_time = datetime.combine(today, engineer_availability.end_time)
            total_availability = end_time - start_time
            weekly_total_availability[engineer.username] = weekly_total_availability.get(engineer.username, timedelta()) + total_availability

        data={'engineers':engineers ,
            'plumbing_qty':plumbing_qty,
            'drainage_qty':drainage_qty,
            'heating_qty':heating_qty,
            'gas_qty':gas_qty,
            'unvented_qty':unvented_qty,
            'electricity_qty':electricity_qty,
            'weekly_total_availability': weekly_total_availability,
            }
        return render (request,'index.html',data)
    
# @login_required
# def list_engineers(request):
#     if request.user.is_superuser:
#         engineers=Engineer_Availability.objects.all()
#     else:
#         engineers=Engineer_Availability.objects.filter(engineer_id=request.user.id)
#     data={'engineers':engineers}
#     return render (request,'engineers.html',data)

@login_required
@permission_required('home.view_engineers_today')
def engr_available_today(request):
    today = date.today()
    engineers = Engineer_Availability.objects.filter(date=today)
    data={'engineers':engineers }
    return render (request,'engineers_today.html',data)

@login_required
def engr_available_weekly(request):

    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    # Filter Engineer_Availability queryset for the current week
    weekly_availability = Engineer_Availability.objects.filter(date__range=[start_of_week, end_of_week] )
    # Calculate weekly total time availability for each engineer
    weekly_total_availability = {}
    for engineer_availability in weekly_availability:
        engineer = engineer_availability.engineer
        start_time = datetime.combine(today, engineer_availability.start_time)
        end_time = datetime.combine(today, engineer_availability.end_time)
        total_availability = end_time - start_time
        weekly_total_availability[engineer.username] = weekly_total_availability.get(engineer.username, timedelta()) + total_availability

    data={'weekly_total_availability': weekly_total_availability, }
    return render (request,'weekly_available_engineer.html',data)

@login_required

def engr_available_today_jobtype(request):
    today = date.today()
    available_engineers_today = Engineer_Availability.objects.filter(date=today)
    # Example: Filter engineers available today for the job 'Plumbing'
    plumbing_engineers_today = available_engineers_today.filter(jobs__name='Plumbing')
    drainage_engineers_today = available_engineers_today.filter(jobs__name='Drainage')
    heating_engineers_today = available_engineers_today.filter(jobs__name='Heating')
    gas_engineers_today = available_engineers_today.filter(jobs__name='Gas')
    unvented_engineers_today = available_engineers_today.filter(jobs__name='Unvented')
    electricity_engineers_today = available_engineers_today.filter(jobs__name='Electricity')

    plumbing_qty=len(plumbing_engineers_today)
    drainage_qty=len(drainage_engineers_today)
    heating_qty=len(heating_engineers_today)
    gas_qty=len(gas_engineers_today)
    unvented_qty=len(unvented_engineers_today)
    electricity_qty=len(electricity_engineers_today)

    data={
            'plumbing_qty':plumbing_qty,
            'drainage_qty':drainage_qty,
            'heating_qty':heating_qty,
            'gas_qty':gas_qty,
            'unvented_qty':unvented_qty,
            'electricity_qty':electricity_qty,
           
            }
    return render (request,'job_type_engineers.html',data)



@login_required
@permission_required('home.view_engineer_list')
def list_engineers(request):
    if request.user.is_superuser:
        engineer_group = Group.objects.get(name='Engineers')
        # engineers= User.objects.filter(groups=engineer_group)
        engineers=Engineer_Availability.objects.all()
    elif request.user.is_staff:
        engineer_group = Group.objects.get(name='Engineers')
        # engineers= User.objects.filter(groups=engineer_group)
        engineers=Engineer_Availability.objects.all()
    else:
        engineers=Engineer_Availability.objects.all()

    data={'engineers':engineers}
    return render (request,'engineersgroup.html',data)

@login_required
@permission_required('home.view_engineer_search')
def search_engineers(request):
    today = date.today()
    if request.method == 'POST':
        form = SearchEngineerForm(request.POST)
        if form.is_valid():
            job = form.cleaned_data.get('job_Type')
            city = form.cleaned_data.get('Post_Code')
            rating = form.cleaned_data.get('rating')
            print(job,city,rating)
            # Filter engineers based on criteria
            engineers = Engineer_Availability.objects.all()
            if job:
                engineers = engineers.filter(jobs=job,date=today)
            if city:
                engineers = engineers.filter(cities=city,date=today)
            if rating is not None:
                engineers = engineers.filter(rating=rating, date=today)
            
            # Sort engineers by rating
            engineers = engineers.order_by('-rating')
            
            return render(request, 'search_engineer.html', {'form': form, 'engineers': engineers})
    else:

        engineers = Engineer_Availability.objects.filter(date=today)
        form = SearchEngineerForm()

        return render(request, 'search_engineer.html', {'form': form,'engineers': engineers})

@login_required
@permission_required('auth.add_user')
def create_engineer(request):
    if request.method == 'POST':
        form =  UserWithEngineerForm(request.POST)
        if form.is_valid():
            # form.save()
            user = form.save()
            # adding user in to a group on Signup
            group = Group.objects.get(name='Engineers')
            user.groups.add(group)
            messages.success(request,"Engineer Added Successfully")
            return redirect('listengineers')  # Redirect to a success page
    else:
        form =  UserWithEngineerForm()
    return render(request, 'add_engineer.html', {'form': form })

@login_required
@permission_required('auth.change_user')
def edit_engineer(request,id=id):
    if request.method == 'POST':
        engineer=User.objects.get(id=id)
        form = EditUserWithEngineer(request.POST,instance=engineer)
        if form.is_valid():
            form.save()
            messages.success(request,"Engineer Updated Successfully")
            return redirect('listengineers')  # Redirect to a success page
    else:
        engineer=User.objects.get(id=id)
        form = EditUserWithEngineer(instance=engineer)
    return render(request, 'edit_engineer.html', {'form': form ,'update':True})

@login_required
@permission_required('auth.delete_user')
def delete_engineer(request,id=id):
   
    engineer=User.objects.get(id=id)
    engineer.is_active=False 
    messages.success(request,"Engineer In_active Successfully")
    return redirect('listengineers')  # Redirect to a success page

@login_required
@permission_required('auth.view_user')
def list_user(request):
    users=User.objects.filter(is_staff=True)
    data={'users':users}
    return render (request,'users.html',data)

@login_required
@permission_required('auth.add_user')
def create_user1(request):
    if request.method == 'POST':
        form = CustUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # adding user in to a group on Signup
            group = Group.objects.get(name='Staff Users')
            user.groups.add(group)
            messages.success(request,"Staff User Added Successfully")
            return redirect('listusers')  # Redirect to a success page
    else:
        form = CustUserCreationForm()
    return render(request, 'create_user.html', {'form': form})

@login_required
@permission_required('auth.add_user')
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the unsaved user object returned by the form save method
            user = form.save(commit=False)
            # Save the user object
            user.save()
            # Get the permissions from the form
            permissions = form.cleaned_data['permissions']
            # Save the permissions associated with the user
            user.user_permissions.set(permissions)
            return redirect('listusers')  # Redirect to a success page
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'create_user.html', {'form': form})

@login_required
@permission_required('auth.change_user')
def edit_user(request,id):
    if request.method=="POST":
        user=User.objects.get(id=id)
        form=EditUserPrifoleForm(request.POST,instance=user)
        form.is_valid()
        messages.success(request,"Your profile Update successfully")
        form.save()
        return redirect('listusers')
    else: 
        user=User.objects.get(id=id)
        form=EditUserPrifoleForm(instance=user)
   
    data={'form':form}
    return render(request,"edit-user.html",data)

@login_required
@permission_required('auth.view_user')
def delete_user(request,id=id):
    engineer=User.objects.get(id=id)
    engineer.is_active=False 
    messages.success(request,"Engineer In_active Successfully")
    return redirect('listusers')  # Redirect to a success page
    
@login_required
@permission_required('home.change_engineer_availability')
def set_availability(request,id):
    if request.method=="POST":
        engr=Engineer_Availability.objects.get(id=id)
        form=EngineerAvailabilityForm(request.POST,instance=engr)
        form.is_valid()
        messages.success(request,"Your availability Updated successfuly")
        form.save()
        return redirect('listengineers')
    else: 

        engr=Engineer_Availability.objects.get(id=id)
        form=EngineerAvailabilityForm(instance=engr)
   
    data={'form':form}
    return render(request,"set-availablity.html",data)