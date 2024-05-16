
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from .forms import EngineerAvailabilityForm
from home.models import Engineer_Availability
from datetime import date,timedelta,time, datetime


@login_required
@permission_required('home.add_engineer_availability')
def engineer_profile(request):
   
    availibility=Engineer_Availability.objects.filter(engineer_id=request.user.id)
    data={'availibility':availibility}
    return render(request,"engineer_profile.html",data)

@login_required
@permission_required('home.add_engineer_availability')
def add_availability(request):
    if request.method == 'POST':
        
        form = EngineerAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.engineer = request.user  # Set the engineer to the current user
            availability.save()
            form.save_m2m()
            return redirect('engrprofile')  # Redirect to a success page
    else:
        engr=Engineer_Availability.objects.filter(engineer_id=request.user.id)
        engr=engr.first()
        form = EngineerAvailabilityForm(instance=engr)   
    data={'form':form}
    return render(request,"set-availablity.html",data)

@login_required
@permission_required('home.change_engineer_availability')
def edit_availability(request,id):
    if request.method=="POST":

        print(request.POST)
        print("i m here")
        print("Job Type:", request.POST.getlist('jobs'))
        print("Post Code:", request.POST.getlist('cities'))
        print("Rating:", request.POST.get('rating'))
        engr=Engineer_Availability.objects.get(id=id)
        form=EngineerAvailabilityForm(request.POST,instance=engr)
        form.is_valid()
        messages.success(request,"Your availability Updated successfully")
        form.save()
        return redirect('engrprofile')
    else: 
        engr=Engineer_Availability.objects.get(id=id)
        form=EngineerAvailabilityForm(instance=engr)
        # form="form"
    data={'form':form}
    return render(request,"set-availablity.html",data)

@login_required
@permission_required('home.delete_engineer_availability')
def delete_availability(request,id):
  
    engr=Engineer_Availability.objects.get(id=id)
    engr.delete()
    messages.success(request,"Your availability deleted successfully")
    return redirect('engrprofile')