from django.shortcuts import render
from .serializer import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
 
 
 
 
 
 
# Create your views here.


class SignUpView(APIView):
    
        def post(self,request):
            validate_data = request.data
            # print('\n\n\n',validate_data,'\n\n\n')
            user_obj = validate_data['user_name']


            # print('\n\n\n\n',user_data,'\n\n\n\n')

            serializer=SignUpSerializer(data=validate_data)
            if serializer.is_valid():
                user = CoreUser.objects.create( 
                    user_name = validate_data['user_name']
                )
                user.set_password(validate_data.get('password'))
                user.save()
                return Response(
                            {"message":"User Registered Successfully"}
                       )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





        

class LoginView(APIView):

    def post(self,request):
        try:
            data = request.data 
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                try:
                    username = serializer.data['user_name']
                    password = serializer.data['password']
                    user = authenticate(username=username,password=password)
                    if user is None:
                        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
                    
                    refresh = RefreshToken.for_user(user)
                    access_token = refresh.access_token
                    custom_claims = access_token.get('custom_claims', {})
                    print({'refresh': str(refresh),
                        'access': str(access_token)})
                    return Response({
                        'refresh': str(refresh),
                        'access': str(access_token),
                         
                    }) 
                except Exception as e:
                    return Response({"error": f"Error during authentication: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
                  
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
              
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
 



class Logout(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print('\n\n\n',request.data,'\n\n\n')
        
        try:
            refresh_token = request.data.get("refresh_token")

            if not refresh_token:
                return Response({"Message":"Enter refresh_token"})
            
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message":"Success"},
                            status=status.HTTP_200_OK
                            )
        

        except Exception as e:
            return Response({"message":str(e)})











class TodoApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
 

    def get(self,request):
        try:

            todo_obj = Todo.objects.all()
            serializer_obj = TodoSerializer(todo_obj,many=True)
            return Response(serializer_obj.data)
    
        except Exception as e:
            return Response({"error":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def post(self,request):
        try:
            validated_data = request.data
            print(validated_data)
            serializer_obj = TodoSerializer(data=validated_data)

            if serializer_obj.is_valid():
                serializer_obj.save()
                return Response({'Message':'Todo Created Successfully ',"Data":serializer_obj.data},status=status.HTTP_201_CREATED)
            
            else:
                return Response({"Message":serializer_obj.errors},status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"error":f"Unexcepted error :{str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(self,request):

        try:
            validated_data = request.data

            try:
                todo_obj = Todo.objects.get(address_id = validated_data['t_id'])
            
            except Todo.DoesNotExist:
                return Response({"Message":"Address not found "},status=status.HTTP_404_NOT_FOUND)
            
            serializers_obj = TodoSerializer(todo_obj, data=validated_data, partial=True)
            
            if serializers_obj.is_valid():
                serializers_obj.save()
                return Response({"Message":"Todo Updated Successfully ","Data":serializers_obj.data},status=status.HTTP_201_CREATED)
            
            else:
                return Response({"Message":serializers_obj.errors},status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"Error":f"Unexcepted error {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



    def delete(self,request):
        try:
            delete = request.GET.get('delete')
            
            if delete:
                try:
                    address_obj = Todo.objects.get(t_id = delete)
                    address_obj.delete()
                    return Response({"Message":"Data Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)
                
                except Todo.DoesNotExist:
                    return Response({"Message":" Todo Not Found"},status=status.HTTP_404_NOT_FOUND)
                
            else:
                return Response({"Message":"No todo id provided "},status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"Error":f"Unexcepted error {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    



