from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager ,PermissionsMixin


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, user_name, password):
        if not user_name:
            raise ValueError('user name is required')
        if not password:
            raise ValueError('password is required')
        
        user = self.model(user_name=user_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,user_name,password,**kwargs):
        user = self.create_user(
            user_name ,password
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user



class CoreUser(AbstractBaseUser,PermissionsMixin):
        user_id = models.AutoField(primary_key=True)
        user_name = models.CharField(max_length=255,unique=True)
        is_admin=models.BooleanField(default=False)
        is_staff=models.BooleanField(default=False)
 

        USERNAME_FIELD = 'user_name'
        objects = UserManager() 
        DisplayField = ['user_id','user_name','is_admin','is_staff']
        
        class Meta: 
            db_table = 'core_user'
            
        def __str__(self):
            return self.user_name
        
        

class Todo(models.Model):
    t_id = models.AutoField(primary_key=True)
    user_id=models.ForeignKey(CoreUser,on_delete=models.CASCADE)
    t_name = models.CharField(max_length=255)
    description = models.CharField(max_length=355)


    DisplayField = ['t_id','t_name','description']
