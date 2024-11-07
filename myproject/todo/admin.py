from django.contrib import admin
from .models import *

# Register your models here.



@admin.register(CoreUser)
class CoreUserAdmin(admin.ModelAdmin):
    list_display = CoreUser.DisplayField

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = Todo.DisplayField

    