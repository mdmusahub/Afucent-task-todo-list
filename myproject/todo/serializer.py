from .models import *
from .serializer import *
from rest_framework import serializers

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreUser
        fields = '__all__'



class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField()
    password = serializers.CharField()



class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"