from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from users import views

app_name = 'users'

urlpatterns = [
    path('users/', views.UsersListView.as_view(), name='users-list'),
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
