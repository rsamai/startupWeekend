from rest_framework import serializers
from models import Profile

class UserSerializer(serializers.Serializer):
  username = serializers.CharField(max_length=100)
  password = serializers.CharField(max_length=100)

class SocialSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    exclude = ('user',)
