# blog 앱 폴더에는 urls.py 이 없기 때문에 따로 추가함.
# mydjango(프로젝트 폴더)\urls.py에 연결시켜줘야 함.
from django.urls import path
from . import views

urlpatterns = [
    # localhost:8000/ 요청
    path('', views.post_list, name='post_list'),
    # localhost:8000/post/5
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    # localhost:8000/post/new
    path('post/new/', views.post_new, name='post_new'),
    # localhost:8000/post/5/edit
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    # localhost:8000/post/5/remove
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    # localhost:8000/post/5/comment
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    # localhost:8000/comment/5/approve
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    # localhost:8000/comment/5/remove
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
]