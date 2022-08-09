from django.urls import path
from .views import (LoginAPIView, ChangePasswordAPIView, RegisterAPIView,
                    PostDetailAPIView, PostsAPIView, CategoryAPIView,
                    PostsCategoryExploreAPIView,FollowAPIView, UnFollowAPIView,
                    LikeAPIView, DislikeAPIView, UserProfileAPIView)
urlpatterns = [
    path('v1/posts/all/', PostsAPIView.as_view(),),
    path('v1/posts/<int:pk>/', PostDetailAPIView.as_view(),),
    path('v1/posts/<int:pk>/like/', LikeAPIView.as_view(),),
    path('v1/posts/<int:pk>/dislike/', DislikeAPIView.as_view(),),
    path('v1/category/',CategoryAPIView.as_view(),),
    path('v1/category/explore/',PostsCategoryExploreAPIView.as_view(),),
    path('v1/auth/register/', RegisterAPIView.as_view(),),
    path('v1/auth/login/', LoginAPIView.as_view(),),
    path('v1/auth/change-password/', ChangePasswordAPIView.as_view()),
    path('v1/user/follow/<int:pk>/', FollowAPIView.as_view()),
    path('v1/user/unfollow/<int:pk>/', UnFollowAPIView.as_view()),
    path('v1/user/user-profile/<int:pk>/',UserProfileAPIView.as_view(),),
]