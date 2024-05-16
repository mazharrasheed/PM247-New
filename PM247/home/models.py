from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Job_Type(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __str__(self):
            return self.name
    
class Post_Code(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __str__(self):
            return self.name

    def __str__(self):
        return  self.name

class Engineer_Availability(models.Model):
    engineer = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    jobs = models.ManyToManyField(Job_Type)
    cities = models.ManyToManyField(Post_Code)
    rating = models.PositiveIntegerField(default=0)
    date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    class Meta:
        permissions = [
            ('view_engineers_today', 'Can view engineers available today'),
            ('view_index', 'Can view index'),
            ('view_engineer_list', 'Can view engineer list'),
        ]
    