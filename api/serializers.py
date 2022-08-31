from rest_framework import serializers
from .models import Category, Followers, Posts, User


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


class EditPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['title', 'caption', 'category']


class PostsSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(source='get_username')
    class Meta:
        model = Posts
        fields = ['id', 'title', 'username', 'image', 'video']

    def get_username(self,obj):
        return obj.user.username


class CategorySerializer(serializers.ModelSerializer):
    class Meta :
        model = Category
        fields = ['id', 'title', 'image', 'video']


class UserPostSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField(source='get_content')
    author = serializers.SerializerMethodField(source='get_author')

    class Meta:
        model = Posts
        fields = [
            'content',
            'author',
        ]
    
    def get_content(self,obj):
        if obj.image != None:
            return obj.image
        return obj.video

    def get_author(self,obj):
        author = obj.user
        return author.id


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ChangeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'biography', 'photo', 'age', 'birth_date']


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


class UserExploreSerializer(serializers.Serializer):
    username = serializers.CharField()


class FollowingSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField(source='get_followers_count')
    followers = serializers.SerializerMethodField(source='get_followers')
    following_count = serializers.SerializerMethodField(source='get_following_count')
    following = serializers.SerializerMethodField(source='get_following')
    class Meta:
        model = Followers
        fields = [
            'followers_count',
            'followers',
            'following_count',
            'following'
        ]
    def get_followers_count(self,obj):
        return obj.followers.count()
    
    def get_following_count(self,obj):
        return obj.following.count()
    
    def get_followers(self,obj):
        qs = obj.followers
        serializer = UserSerializer(qs,many=True)
        return serializer.data

    def get_following(self,obj):
        qs = obj.following
        serializer = UserSerializer(qs,many=True)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title']


class CategoryExploreSerializer(serializers.Serializer):
    category_title = serializers.ListField()
'''
class PostsCategoryExploreSerializer(serializers.ModelSerializer):

    top_view = serializers.SerializerMethodField(source='get_top_view')
    top_like = serializers.SerializerMethodField(source='get_top_like')
    top_new = serializers.SerializerMethodField(source='get_top_new')

    class Meta:
        model = Posts
        fields = [
            'top_view',
            'top_like',
            'top_new',
        ]
    
    def get_top_view(self,obj):
        posts = obj.order_by('-view')[:10]
        print(posts)
        serializer = UserPostSerializer(posts,many=True)
        return serializer.data

    def get_top_like(self,obj):
        posts = obj.order_by('-like')[:10]
        serializer = UserPostSerializer(posts,many=True)
        return serializer.data
    
    def get_top_new(self,obj):
        posts = obj.order_by('-created_at')[:10]
        serializer = UserPostSerializer(posts,many=True)
        return serializer.data
'''



