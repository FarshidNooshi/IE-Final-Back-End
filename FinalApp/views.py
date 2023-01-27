import datetime

import jwt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from FinalApp.models import User, ExpiredToken
from FinalApp.serializers import UserSerializer, ExpiredTokenSerializer

# Create your views here.

EXP_TIME = datetime.timedelta(minutes=120)
UN_AUTHENTICATED_MESSAGE = 'Unauthenticated'
INCORRECT_PASSWORD_MESSAGE = 'Incorrect password!'
USER_NOT_FOUND_MESSAGE = 'User not found!'
QUESTION_FILL_BLANK = 'Fill'
QUESTION_Multiple_CHOICE = 'MCQ'
SECRET_KEY = 'secret'
ALGORITHMS = ['HS256']


def authenticate(request):
    token = request.Headers.get('Authorization')
    if not token:
        raise AuthenticationFailed('%s!' % UN_AUTHENTICATED_MESSAGE)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHMS)
        expired_token = ExpiredToken.objects.filter(token=token)
        if expired_token:
            raise AuthenticationFailed('%s!' % UN_AUTHENTICATED_MESSAGE)
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('%s!' % UN_AUTHENTICATED_MESSAGE)
    return payload


def generate_token(id):
    payload = {
        'id': id,
        'exp': datetime.datetime.utcnow() + EXP_TIME,
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHMS[0])
    return token


def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes,


class RegisterView(APIView):
    """
    This method is used to register a new user in the system
    """

    @swagger_auto_schema(
        operation_description='This method is used to register a new user in the system',
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            400: 'Bad Request'
        }
    )
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.is_active = True
            user.save()
        serializer.save()

        response = Response(serializer.data, status=status.HTTP_201_CREATED)
        response.headers['Authorization'] = generate_token(user.id)

        return response


class LoginView(APIView):
    @swagger_auto_schema(
        operation_description='This method is used to authenticate a user and return a JWT token to be used in other requests',
        # just email and password
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT, properties={
                    'jwt': openapi.Schema(type=openapi.TYPE_STRING),
                }
            ),
            400: openapi.Schema(
                # AuthenticationFailed
                type=openapi.TYPE_OBJECT, properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        }
    )
    def post(self, request):
        password = request.data['password']
        username = request.data['username']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('%s' % USER_NOT_FOUND_MESSAGE)

        if password != user.password:
            raise AuthenticationFailed('%s' % INCORRECT_PASSWORD_MESSAGE)

        token = generate_token(user.id)

        response = Response()

        response.headers['Authorization'] = token
        response.data = {
            'jwt': token
        }
        response.status_code = status.HTTP_200_OK
        return response


class LogoutView(APIView):
    @swagger_auto_schema(
        operation_description='This method is used to logout a user and delete the jwt ',
        responses={
            200: 'OK',
            401: 'Unauthenticated'
        }
    )
    def post(self, request):
        token = request.headers.get('Authorization')
        response = Response()
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHMS)
        serializer = ExpiredTokenSerializer(data={'token': token})
        if serializer.is_valid(raise_exception=True):
            expired_token = serializer.save()
            expired_token.save()
        response.status_code = status.HTTP_200_OK
        response.data = {
            'message': 'success'
        }
        return response


class AuthView(APIView):
    @swagger_auto_schema(
        operation_description='This method is used to check if the user is authenticated with a JWT token',
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT, properties={
                    'logged_in': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example='You are logged in'),
                }
            ),
            400: 'Bad Request'
        },
        request_cookies={
            'jwt': openapi.Schema(type=openapi.TYPE_STRING, description='JWT token')
        },
    )
    def get(self, request):
        log_dict = {'logged_in': False, 'message': "You are not logged in"}
        try:
            token = request.headers.get('Authorization')
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHMS)
                expired_token = ExpiredToken.objects.filter(token=token)
                if expired_token:
                    raise AuthenticationFailed('%s!' % UN_AUTHENTICATED_MESSAGE)
            except jwt.ExpiredSignatureError:
                log_dict['message'] = "Unauthenticated"
                return Response(log_dict, status=status.HTTP_401_UNAUTHORIZED)
            log_dict['logged_in'] = True
            log_dict['message'] = "You are logged in"
            return Response(log_dict, status=status.HTTP_200_OK)
        except jwt.DecodeError:
            log_dict['message'] = "Unauthenticated"
            return Response(log_dict, status=status.HTTP_401_UNAUTHORIZED)
