from django.urls import path
from . import views

urlpatterns = [
    path('', views.GoalListView.as_view(), name='goal_list'),
    path('create/', views.GoalCreateView.as_view(), name='goal_create'),
    path('<int:pk>/', views.GoalDetailView.as_view(), name='goal_detail'),
    path('<int:pk>/edit/', views.GoalUpdateView.as_view(), name='goal_edit'),
    path('<int:pk>/delete/', views.GoalDeleteView.as_view(), name='goal_delete'),
]
