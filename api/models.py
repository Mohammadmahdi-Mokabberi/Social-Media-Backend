from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin
from django.contrib.auth.hashers import make_password



class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    is_active = models.BooleanField(default=True, verbose_name='فعال؟')
    is_staff = models.BooleanField(default=False, verbose_name='کارمند؟')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین؟')
    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام خانوادگی')
    username = models.CharField(max_length=100, unqique=True, verbose_name='نام کاربری')
    email = models.EmailField(_('email address'), unique=True, verbose_name='ایمیل')
    age = models.CharField(max_length=3, null=True, blank=True, verbose_name='سن')
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    registered_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ثبت نام')


    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


class Followers(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='user_info', verbose_name='کاربر')
    followers = models.ManyToManyField(User, related_name='user_followers', verbose_name='دنبال کننده ها' )
    following = models.ManyToManyField(User, related_name='user_following', verbose_name='دنبال شونده ها')


class StoryPost(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='author', verbose_name='نویسنده')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    image = models.ImageField(upload_to='images/stories/', verbose_name='عکس')
    caption = models.TextField(verbose_name='متن')
    like = models.ManyToManyField(User, related_name='user_liked', verbose_name='لایک')
    
    def liked(self, user):
        self.like.add(user)
        self.save()

class ImagePost(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='author', verbose_name='صاحب پست')
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name='عنوان')
    image = models.CharField(upload_to='images/images/', verbose_name='عکس')
    caption = models.TextField(null=True, blank=True, verbose_name='کپشن')
    like = models.ManyToManyField(User, related_name='user_liked', verbose_name='لایک')

    def liked(self, user):
        self.like.add(user)
        self.save()


class VideoPost(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='author', verbose_name='')
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name='عنوان')
    video = models.FileField(upload_to='videos/videos/', verbose_name='ویدیو')
    caption = models.TextField(null=True, blank=True, verbose_name='کپشن')
    like = models.ManyToManyField(User, related_name='user_liked', verbose_name='لایک')
    view = models.PositiveIntegerField(default=0, verbose_name='بازدید')

    def liked(self, user):
        self.like.add(user)
        self.save()
    
    def viewed(self):
        self.view += 1
        self.save()