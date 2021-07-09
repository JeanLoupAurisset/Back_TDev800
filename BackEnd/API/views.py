from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import AlbumSerializer, UserSerializer, PasswordSerializer, PasswordSerializer, PhotoSerializer, MetaDataSerializer
from .models import Album, Photo, MetaData
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from django.core.exceptions import ObjectDoesNotExist

class CustomAuthToken(ObtainAuthToken):
    throttle_classes = [UserRateThrottle]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    throttle_classes = [UserRateThrottle]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny(), ]       
        elif self.action == 'logout':
            return [permissions.IsAuthenticated(), ]  
        elif self.action == 'destroy':
            return [permissions.IsAuthenticated(), ]   
        elif self.action == 'get_queryset':
            return [permissions.IsAuthenticated(),]
        return super(UserViewSet, self).get_permissions()

    @action(detail=False)
    def get_queryset(self):

        user = self.request.user
        if (username := self.request.GET.get('username')) is not None:
            return User.objects.filter(username__contains=username).values('username')
        return User.objects.filter(id=user.id)
    
    @action(detail=False)
    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Wrong password.']}, 
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user_id = request.user.id
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        partial = True # Here I change partial to True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    throttle_classes = [UserRateThrottle]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), ]       
        elif self.action == 'destroy':
            return [permissions.IsAuthenticated(), ]   
        elif self.action == 'get_queryset':
            return [permissions.IsAuthenticated(), ]
        return super(AlbumViewSet, self).get_permissions()

    @action(detail=False)
    def get_queryset(self):

        user = self.request.user
        if (name := self.request.GET.get('name')) is not None:
            return Album.objects.filter(name__contains=name).filter(Access_public__contains="true")
        return Album.objects.filter(user_id=user.id)


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    throttle_classes = [UserRateThrottle]
    http_method_names = ['post', 'delete', 'put']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), ]    
        elif self.action == 'destroy':
            return [permissions.IsAuthenticated(), ]   
        elif self.action == 'update':
            return [permissions.IsAuthenticated(), ]      
        return super(PhotoViewSet, self).get_permissions()


class MetaDataViewSet(viewsets.ModelViewSet):
    queryset = MetaData.objects.all()
    serializer_class = MetaDataSerializer
    throttle_classes = [UserRateThrottle]
    http_method_names = ['post', 'delete', 'put']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), ]    
        elif self.action == 'destroy':
            return [permissions.IsAuthenticated(), ]   
        elif self.action == 'update':
            return [permissions.IsAuthenticated(), ]      
        return super(MetaDataViewSet, self).get_permissions()
