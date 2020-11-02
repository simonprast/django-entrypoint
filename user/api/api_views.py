from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status, mixins, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import obtain_auth_token

from ..models import User
from .serializers import UserSerializer, RegisterUserSerializer


class UserList(mixins.ListModelMixin,
               generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return self.list(request, *args, **kwargs)
        elif not request.user.is_anonymous:
            user = self.get_object(request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserCreateOrLogin(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            # Deny any request thats not from an AnonymousUser
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = RegisterUserSerializer(data=request.data)

            if settings.ALLOW_REGISTER:
                if serializer.is_valid():
                    # Creates the user using create_user()
                    serializer.save()

            # Authenticate the newly created user
            # OR authenticate the existing user with given username and password combination.
            token, created, user = obtain_auth_token(
                request.data.__getitem__('username'),
                request.data.__getitem__('password')
            )

            # If a user with given username does already exist but the username password
            # combination is wrong, 'token', 'created' and 'user' will be set to 'None'.
            # In this case, this error response is thrown.
            if not token:
                errors = {
                    'username': [
                        'user with this username already exists',
                        'username and password combination wrong'
                    ]
                }
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            # Either the user object was created or the user just logged in
            auth_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK

            return Response({'username': user.username, 'token': token.key}, status=auth_status)


# class UserList(APIView):
#     def get(self, request, format=None):
#         users = User.objects.all()
#         serializer = UserSerializer(
#             users, many=True, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def check_requested_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            return user
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, *args, **kwargs):
        requested_user = self.check_requested_object(pk=pk)
        if request.user.is_staff or requested_user == request.user:
            return self.retrieve(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        requested_user = self.check_requested_object(pk=pk)
        if request.user.is_staff or requested_user == request.user:
            return self.update(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    # def delete(self, request, *args, **kwargs):
    #     requested_user = self.check_requested_object(pk=pk)
    #     if request.user.is_staff or requested_user == request.user:
    #         return self.destroy(request, *args, **kwargs)
    #     else:
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)

    # class UserDetail(APIView):
    #     def get_object(self, pk):
    #         try:
    #             user = User.objects.get(pk=pk)
    #         except User.DoesNotExist:
    #             return Response(status=status.HTTP_404_NOT_FOUND)

    #     def get(self, request, pk, format=None):
    #         user = self.get_object(pk)
    #         serializer = UserSerializer(user)
    #         return Response(serializer.data)

    #     def put(self, request, pk, format=None):
    #         user = self.get_object(pk)
    #         serializer = UserSerializer(user, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     def delete(self, request, pk, format=None):
    #         user = self.get_object(pk)
    #         user.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
