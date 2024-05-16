from django.contrib import admin
from .models import Post_Code,Job_Type,Engineer_Availability
# Register your models here.


@admin.register(Post_Code)
class Post_CodeAdmin(admin.ModelAdmin):
    
    list_display = ['name',]

@admin.register(Job_Type)
class Job_TypeAdmin(admin.ModelAdmin):
    
    list_display = ['name',]

@admin.register(Engineer_Availability)
class Engineer_AvailablityAdmin(admin.ModelAdmin):
    
    list_display = ['engineer','date','start_time','end_time']
    