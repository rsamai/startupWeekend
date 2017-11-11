from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from serializers import UserSerializer, SocialSerializer
from django.utils.http import urlencode
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from models import Profile
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

# Create your views here.

class CreateUser(APIView):
  def post(self, request, format=None):
    print "here"
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
      try:
        user = User.objects.get(username=serializer.data['username'])
      except ObjectDoesNotExist:
        user = User.objects.create_user(serializer.data['username'], password=serializer.data['password'])
        user.save()
        profile = Profile(user=user)
        profile.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'id': user.id}, status=status.HTTP_201_CREATED)
      return Response({'errors': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'errors': 'Fields may not be blank'}, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(APIView):
  def post(self, request, format=None):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
      user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
      if user:
        token = Token.objects.get_or_create(user=user)
        return Response({'token': token[0].key, 'id': user.id})
    return Response({'errors': 'Username/Password is not correct'}, status=status.HTTP_400_BAD_REQUEST)

class UserInfo(APIView):
  def get_object(self, request, pk):
    try:
      user = User.objects.get(pk=pk)
      return user.profile
    except User.DoesNotExist:
      raise Http404

  def get(self, request, pk, format=None):
    profile = self.get_object(request, pk)
    if not profile:
      return Response('Weird Error', status=status.HTTP_400_BAD_REQUEST)
    return Response(SocialSerializer(profile).data, status=status.HTTP_200_OK)

class WebUserInfo(APIView):
  def get_object(self, request, pk):
    try:
      user = User.objects.get(pk=pk)
      return user.profile
    except User.DoesNotExist:
      raise Http404

  def get(self, request, pk):
    profile = self.get_object(request, pk)
    context = {'profile': profile}
    return render(request, 'contacts/index.html', context)

class ConnectUser(APIView):
  authentication_classes = (SessionAuthentication, BasicAuthentication)
  def get_object(self, request, pk):
    try:
      user = User.objects.get(pk=pk)
      if user == request.user:
        return user.profile
      else:
        return None
      return user.profile
    except User.DoesNotExist:
      raise Http404

  def post(self, request, pk, format=None):
    profile = self.get_object(request, pk)
    if not profile:
      return Response('Not Owner', status=status.HTTP_400_BAD_REQUEST)
    serializer = SocialSerializer(profile, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(SocialSerializer(profile).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
