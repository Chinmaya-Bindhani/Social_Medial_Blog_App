from django.urls import path
from .views import PostListView,PostCreateView,PostDetail,PostUpdateView,PostDeleteView,UserPostDetails
urlpatterns=[
    path('',PostListView.as_view(),name='home'),
    path('create/post/',PostCreateView.as_view(),name='post-page'),
    path('post/<int:pk>/detail/',PostDetail.as_view(),name='post-details'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    path('post/<str:username>/list/',UserPostDetails.as_view(),name='post-specific-details'),

]