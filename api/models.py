from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin



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
    username = models.CharField(max_length=100, unique=True, verbose_name='نام کاربری')
    email = models.EmailField(_('email address'), unique=True)
    age = models.CharField(max_length=3, null=True, blank=True, verbose_name='سن')
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد')
    registered_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ثبت نام')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


class Followers(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='user_info', verbose_name='کاربر')
    followers = models.ManyToManyField(User, related_name='user_followers', verbose_name='دنبال کننده ها' )
    following = models.ManyToManyField(User, related_name='user_following', verbose_name='دنبال شونده ها')
    
    class Meta:
        verbose_name = 'دنبال کننده و دنبال شونده'
        verbose_name_plural = 'دنبال کننده ها و دنبال شونده ها'


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان دسته بندی')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Posts(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='author', verbose_name='صاحب پست')
    title = models.CharField(max_length=100, null=True, blank=True, verbose_name='عنوان')
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='عکس')
    category = models.ManyToManyField(Category, related_name='post_category',)
    caption = models.TextField(null=True, blank=True, verbose_name='کپشن')
    like = models.ManyToManyField(User, blank=True, related_name='user_liked', verbose_name='لایک')
    view = models.PositiveIntegerField(default=0, verbose_name='بازدید')
    video = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name='ویدیو')
    created_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ ساخت')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ تغییر')

    def liked(self, user):
        self.like.add(user)
        self.save()

    def viewed(self):
        self.view += 1 
        self.save()

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'