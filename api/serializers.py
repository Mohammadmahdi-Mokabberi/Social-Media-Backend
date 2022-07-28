from rest_framework import serializers
from .models import Category, Posts, User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'age', 'birth_date', 'password']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id', 'title', 'user', 'image', 'video']


class CategorySerializer(serializers.ModelSerializer):
    class Meta :
        model = Category
        fields = ['id', 'title']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class PostDetailSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField(source='get_title')
    caption = serializers.SerializerMethodField(source='get_caption')
    category = serializers.SerializerMethodField(source='get_category')
    author = serializers.SerializerMethodField(source='get_author')
    like_count = serializers.SerializerMethodField(source='get_like_count')
    like_list = serializers.SerializerMethodField(source='get_like_list')
    
    
    class Meta:
        model = Posts
        fields = ['id',
                  'title',
                  'caption',
                  'category',
                  'author',
                  'like_list',
                  'like_count',
                  'view',
                  'image',
                  'video'
                  ]

    def get_title(self,obj):
        return obj.title
    
    def get_caption(self,obj):
        return obj.caption
    
    def get_category(self,obj):
        qs = obj.category
        serializer = CategorySerializer(qs, many=True)
        return serializer.data
    
    def get_author(self,obj):
        data = {
            'user_id' : obj.user.id,
            'user_name' : obj.user.username
        }
        return data
    
    def get_like_count(self,obj):
        return obj.like.count()

    def get_like_list(self,obj):
        qs = obj.like
        serializer = UserSerializer(qs, many=True)
        return serializer.data

    def get_view_count(self,obj):
        return obj.view
    
    def get_image(self,obj):
        if obj.image != None:
            return obj.image
        return 'None'
    
    def get_video(self,obj):
        if obj.video != None:
            return obj.video
        return 'None'