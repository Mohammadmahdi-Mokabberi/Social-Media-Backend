from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from api.models import Posts
from .serializers import ChangePasswordSerializer, RegisterSerializer

User = get_user_model()

def response_data(message=None, status_code=None, data=None):
    last_response = {}
    if message != None:
        last_response['error_message'] = message
    if status_code != None:
        last_response['status_code'] = status_code
    if data != None:
        last_response['data'] = data
    if status_code == 1:
        get_status = status.HTTP_200_OK
    else:
        get_status = status.HTTP_400_BAD_REQUEST
    return Response(last_response, status=get_status)

def get_key_error_from_serializer_errors(serializer_error):
    return [key for key in serializer_error]


class LoginAPIView(generics.CreateAPIView):



class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                fields_error = get_key_error_from_serializer_errors(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST, data=fields_error)
            username = request.data['username']
            password = request.data['password']
            if not len(password)>8 : 
                response_data(status_code=0, message='password is not long enough')
            password = make_password(password)
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            age = request.data['age']
            birth_date = request.data['birth_date']
            User.objects.create(username=username, password=password, first_name=first_name, last_name=last_name, email=email, age=age, birth_date=birth_date)
            
            return response_data(status_code=1, message='user created')
        except:
            return response_data(status_code=0, message='server error')


class ChangePasswordAPIView(generics.CreateAPIView):
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            old_password = request.data['old_password']
            new_password1 = request.data['new_password1']
            new_password2 = request.data['new_password1']
            
            if new_password1 != new_password2 :
                return response_data(status_code=0, message='new passwords are not same')
            
            old_password = make_password(old_password)
            if user.password != old_password:
                return response_data(status_code=0, message='old password is not correct')
            
            new_password = make_password(new_password1)
            user.password = new_password
            user.save()
            return response_data(status_code=1, message='password changed')
        except :
            return response_data(status_code=0, message='server error')


class FollowAPIView(generics.RetrieveAPIView):
    def get_object(self):
        return self.kwargs.get('pk')
            
    def get_user(self):
        return self.request.user
    
    def get(self, request, *args, **kwargs):
        try :
            following_user_id = self.get_object()
            if not User.objects.filter(id=following_user_id).exists():
                return response_data(status_code=0, message='user does not exist')
            following_user = User.objects.get(id=following_user_id)
            follower_user = self.get_user()
            following_user.followers.add(follower_user)
            following_user.save()
            return response_data(status_code=1)
        except:
            return response_data(status_code=0, message='server error')


class UnFollowAPIView(generics.RetrieveAPIView):

    def get_object(self):
        return self.kwargs.get('pk')
    
    def get_user(self):
        return self.request.user
    
    def get(self, request, *args, **kwargs):
        try :
            following_user_id = self.get_object()
            if not User.objects.filter(id=following_user_id).exists():
                return response_data(status_code=0)
            
            following_user = User.objects.get(id=following_user_id)
            follower_user = self.get_user()
            following_user.followers.remove(follower_user)
            following_user.save()
        except :
            return response_data(status_code=0, message='server error')


class LikeAPIView(generics.RetrieveAPIView):

    def get_object(self):
        return self.kwargs.get('pk')
    
    def get_user(self):
        return self.request.user
    
    def get(self, request, *args, **kwargs):
        try:
            liked_post_id = self.get_object()
            if not Posts.objects.filter(id=liked_post_id).exists():
                return response_data(status_code=0, message='post not found')
            user = request.user
            liked_post = Posts.objects.get(id=liked_post_id)
            liked_post.liked(user)
            response_data(status_code=1, message='Post Liked')
        except:
            return response_data(status_code=0, message='server error')


class DislikeAPIView(generics.RetrieveAPIView):

    def get_object(self):
        return self.kwargs.get('pk')
    
    def get_user(self):
        return self.request.user
    
    def get(self, request, *args, **kwargs):
        try:
            liked_post_id = self.get_object()
            if not Posts.objects.filter(id=liked_post_id).exists():
                return response_data(status_code=0, message='post not found')
            user = request.user
            liked_post = Posts.objects.get(id=liked_post_id)
            liked_post.like.remove(user)
            response_data(status_code=1, message='Post Disliked')
        except:
            return response_data(status_code=0, message='server error')

