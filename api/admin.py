from django.contrib import admin
from .models import User, Posts, Followers, Category



class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email']


admin.site.register(User,UserAdmin)
admin.site.register(Posts,)
admin.site.register(Followers,)
admin.site.register(Category,)

