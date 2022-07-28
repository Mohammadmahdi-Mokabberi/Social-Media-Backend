from django.urls import path
from .views import (LoginAPIView, ChangePasswordAPIView, RegisterAPIView,
                    PostDetailAPIView, PostsAPIView, FollowAPIView, 
                    UnFollowAPIView, LikeAPIView, DislikeAPIView)
urlpatterns = [
    path('posts', PostsAPIView.as_view(),),
    path('post/<int:pk>', PostDetailAPIView.as_view(),),
    path('post/<int:pk>/like', LikeAPIView.as_view(),),
    path('post/<int:pk>/dislike', DislikeAPIView.as_view(),),
    path('register/', RegisterAPIView.as_view(),),
    path('login/', LoginAPIView.as_view(),),
    path('change-password/', ChangePasswordAPIView.as_view()),
    path('follow/<int:pk>', FollowAPIView.as_view()),
    path('unfollow/<int:pk>', UnFollowAPIView.as_view()),
]