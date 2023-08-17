from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save

# Create your models here.
#class User(AbstractUser):
#    is_student = models.BooleanField()
#    is_teacher = models.BooleanField()

#    def _str_(self):
#        return self.username

#class Students(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)

#    def _str_(self):
#        return self.user.username
    
class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager,self).get_queryset().filter(city='pansalwa')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100,default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
        
post_save.connect(create_profile, sender=User)