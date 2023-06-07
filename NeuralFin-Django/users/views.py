from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

import random
import string

def generate_unique_username(name):
    username = name.replace(" ", "")
    while User.objects.filter(username=username).exists():
        random_number = ''.join(random.choices(string.digits, k=4))
        username = f"{name}{random_number}"
    return username



class RegisterView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['username'] = generate_unique_username(data['name'])
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response()
        response.set_cookie(key='jwt', value=access_token, httponly=True, samesite='None', secure=True, domain='neuralfin.xyz') #, httponly=True, samesite='None', secure=True
        response.data = {
            'jwt': access_token
        }
        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            jwt_authentication = JWTAuthentication()
            validated_token = jwt_authentication.get_validated_token(token)
            user = jwt_authentication.get_user(validated_token)
        except InvalidToken:
            raise AuthenticationFailed('Unauthenticated!')

        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            jwt_authentication = JWTAuthentication()
            validated_token = jwt_authentication.get_validated_token(token)
            request.user = jwt_authentication.get_user(validated_token)
        except InvalidToken:
            raise AuthenticationFailed('Unauthenticated!')
        
        data = request.data.copy()
        data['username'] = generate_unique_username(data['username'])
        serializer = UserSerializer(instance=request.user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt', samesite='None')
        response.data = {
            'message': 'success'
        }
        return response


