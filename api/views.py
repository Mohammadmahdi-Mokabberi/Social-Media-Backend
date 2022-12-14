from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from functools import reduce
import operator

from api.models import Category, Followers, Posts
from .serializers import (CategorySerializer, ChangePasswordSerializer, ChangeProfileSerializer, EditPostSerializer, FollowingSerializer, 
                          LoginSerializer, CategoryExploreSerializer,
                          RegisterSerializer,PostsSerializer, PostDetailSerializer,
                          UserExploreSerializer, UserPostSerializer)

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
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            email = request.data['email']
            username = request.data['username']
            password = request.data['password']
            if email != '':
                if not User.objects.filter(email=email).exists():
                    return response_data(status_code=0, message='User  not found')
                password = make_password(password)
                if not User.objects.filter(email=email, password=password).exists:
                    return response_data(status_code=0, message='password not valid')
                user = User.objects.get(email=email)
                refresh = RefreshToken.for_user(user)
                data = {
                    'access': str(refresh.access_token)
                }
                return response_data(status_code=1, data=data)

            if username !='':
                if not User.objects.filter(username=username).exists():
                    return response_data(status_code=0, message='User  not found')
                password = make_password(password)
                if not User.objects.filter(username=username, password=password).exists:
                    return response_data(status_code=0, message='password not valid')
                user = User.objects.get(username=username)
                refresh = RefreshToken.for_user(user)
                data = {
                    'access': str(refresh.access_token)
                }
                return response_data(status_code=1, data=data)

        except:
            return response_data(status_code=0, message='server error')


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                fields_error = get_key_error_from_serializer_errors(serializer.errors)
                return Response(status=status.HTTP_400_BAD_REQUEST, data=fields_error)
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            if not len(password)>8 : 
                response_data(status_code=0, message='password is not long enough')
            if User.objects.filter(username=username).exists():
                return response_data(status_code=0, message='Username already exist')
            if User.objects.filter(email=email).exists():
                return response_data(status_code=0, message='Email already exist')
            password = make_password(password)
            first_name = request.data['first_name']
            last_name = request.data['last_name']
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
            new_password2 = request.data['new_password2']
            
            if new_password1 != new_password2 :
                return response_data(status_code=0, message='new passwords are not same')
            
            if not user.check_password(old_password):
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
            return response_data(status_code=1)
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
            return response_data(status_code=1)
        except:
            return response_data(status_code=0, message='server error')


class PostsAPIView(generics.ListAPIView):
    serializer_class = PostsSerializer

    def get_queryset(self):
        return Posts.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return response_data(status_code=1, data=serializer.data)        
        except:
            return response_data(status_code=0, message='server error')


class PostDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PostDetailSerializer
    def get_object(self):
        return self.kwargs.get('pk')
    
    def get(self, request, *args, **kwargs):
        try :
            post_id = self.get_object()
            if not Posts.objects.filter(id=post_id).exists():
                return response_data(status_code=0, message='post not found')
            post = Posts.objects.get(id=post_id)
            post.viewed()
            serializer = self.get_serializer(post)
            return response_data(status_code=1, data=serializer.data)
        except:
            return response_data(status_code=0, message='server error')


class UserProfileAPIView(generics.CreateAPIView):
    serializer_class = UserExploreSerializer

    def post(self, request, *args, **kwargs):
        try :
            username = request.data['username']
            if not User.objects.filter(username=username).exists():
                return response_data(status_code=0, message='User not found')
            user = User.objects.get(username=username)
            followers_qs = Followers.objects.get(user=user)
            follower_serializer = FollowingSerializer(followers_qs)
            post_qs = Posts.objects.filter(user=user)
            post_serializer = PostsSerializer(post_qs,many=True)

            data = {
                'username' : user.username,
                'name' : f'{user.first_name} {user.last_name}',
                'followers_info' : follower_serializer.data,
                'user_post_info' : post_serializer.data,
            }
            return response_data(status_code=1, data=data)
        except:
            return response_data(status_code=0, message='server error')


class UserChangeProfileAPIView(generics.CreateAPIView):
    serializer_class = ChangeProfileSerializer
    def get_object(self):
        return self.request.user
    
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return response_data(status_code=1, data=serializer.data)
    
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.username = request.data['username']
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.biography = request.data['biography']
        user.photo = request.data['photo']
        user.age = request.data['age']
        user.birth_date = request.data['birth_date']
        user.save()
        return response_data(status_code=1, message='Profile Updated')


class CategoryAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

    def get(self, request, *args, **kwargs):
        try :
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset,many=True)
            return response_data(status_code=1, data=serializer.data)
        except :
            return response_data(status_code=0, message='server error')


class PostsCategoryExploreAPIView(generics.CreateAPIView):
    serializer_class = CategoryExploreSerializer

    def post(self, request, *args, **kwargs):
        try:
            category_title = request.data['category_title']
            for title in category_title:
                if not Category.objects.filter(title=title):
                    return response_data(status_code=0, message=f'No category found by name {title}')
            categories = reduce(operator.and_ , (Q(category__title=cat) for cat in category_title) )
            posts = Posts.objects.exclude(~categories)
            serializer = PostsSerializer(posts, many=True)
            return response_data(status_code=1, data=serializer.data)
        except:
            return response_data(status_code=0, message='server error')


class EditPostAPIView(generics.CreateAPIView):
    serializer_class = EditPostSerializer
    
    def get_object(self):
        return self.kwargs.get('pk')
    
    def get_user(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_user()
            post_id = self.get_object()
            if not Posts.objects.filter(id=post_id).exists():
                return response_data(status_code=0, message='post not found')
            post = Posts.objects.get(id=post_id)

            serializer = PostDetailSerializer(post)
            return response_data(status_code=1, data=serializer.data)
        except:
            return response_data(status_code=0, message='server error')
    
    def post(self, request, *args, **kwargs):
        #try:
            user = self.get_user()
            post_id = self.get_object()
            if not Posts.objects.filter(id=post_id).exists():
                return response_data(status_code=0, message='post not found')
            post = Posts.objects.get(id=post_id)
            if user != post.user :
                return response_data(status_code=0, message='no permission')
            post.title = request.data['title']
            post.category.set(request.data['category'])
            post.caption = request.data['caption']
            post.save()
            return response_data(status_code=1)
        #except:
            return response_data(status_code=0, message='server error')