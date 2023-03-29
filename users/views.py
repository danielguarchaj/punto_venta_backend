from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListAPIView
from users.serializers import UserProfileSerializer, CustomTokenObtainPairSerializer
from users.models import UserProfile


class UsersListView(ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer