from rest_framework import viewsets
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import action, permission_classes, api_view
from .serializers import MeansOfPaymentSerializer, UserSerializer, PasswordSerializer, BankAccountSerializer
from .models import MeansOfPayment, BankAccount
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.throttling import UserRateThrottle

class CustomAuthToken(ObtainAuthToken):
    throttle_classes = [UserRateThrottle]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        bank_account = BankAccount.objects.get(users=user.pk)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'bank_id': bank_account.pk
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
        return super(UserViewSet, self).get_permissions()

    def get_queryset(self):
        user = self.request.user
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

class MeansOfPaymentViewSet(viewsets.ModelViewSet):
    queryset = MeansOfPayment.objects.all()
    serializer_class = MeansOfPaymentSerializer
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        user = self.request.user
        return MeansOfPayment.objects.filter(users_id=user.id)

    def destroy(self, request, *args, **kwargs):
        user_id = request.user
        mop_id = request.data
        try:
            mop = MeansOfPayment.objects.get(id=mop_id.id)
            mop.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    throttle_classes = [UserRateThrottle]

    def get_queryset(self,):
        user = self.request.user
        return BankAccount.objects.filter(users_id=user.id)

    def update(self, request, *args, **kwargs):
        user = self.request.user

        # We get the mops associated to the user
        obj = MeansOfPayment.objects.filter(users_id=user.id)
        myDict = dict(request.data)
        
        # If mop in request is not in db we return an error
        if myDict['mop_description'][0] in [i.description for i in obj]:
            partial = True # Here I change partial to True
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



