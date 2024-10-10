from .forms import CustomUserMainForm, CustomUserLoginForm
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserLoginSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.
def user_home_view(request):
    return render(
        request=request,
        template_name='user_management/user_home.html'
    )

@login_required
def user_list_view(request):
    users = CustomUser.objects.filter(is_superuser=False,is_active=True).exclude(username=request.user)
    return render(
        request=request,
        template_name='user_management/user_list.html',
        context={
            'users':users
        }
    )

#USER_ADD  - START
def user_add_view(request):
    return render(
        request=request,
        template_name='user_management/user_add.html',
        context={
            'CustomUserMainForm':CustomUserMainForm()
        }
    )
    
@api_view(['POST'])
def user_add(request):
    if request.method == 'POST':
        userSerializer = CustomUserSerializer(data=request.data)
        if userSerializer.is_valid():
            userSerializer.create(userSerializer.validated_data)
            return Response(
                data={
                    'request_status':True,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            data={
                'request_status':False,
                'form_errors':userSerializer.errors
            },
            status=status.HTTP_200_OK
        )
#USER_ADD  - END

#USER_LOGIN  - START
def user_login_view(request):
    return render(
        request=request,
        template_name='user_management/user_login.html',
        context={
            'CustomUserLoginForm':CustomUserLoginForm
        }
    )
    
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        if request.data.get('username') and request.data.get('password'):
            loginSerializer = CustomUserLoginSerializer(data=request.data)
            if loginSerializer.is_valid():
                user = authenticate(
                    username=loginSerializer.validated_data['username'], 
                    password=loginSerializer.validated_data['password']
                )
                if user is not None:
                    login(request,user)
                    refresh = RefreshToken.for_user(user)
                    access = refresh.access_token
                    return Response(
                        data={
                            'request_status':True,
                            'refresh_token':str(refresh),
                            'access_token':str(access)
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    #Authentication failed
                    error_code = "Password not match or user is currently disabled."
            else:
                #Serializer validation failed
                error_code = "This username doesn't exist or is currently disabled."
        else:
            #Username or password not in body
            error_code = "This username doesn't exist or is currently disabled."
            
        #Return failed body
        return Response(
            data={
                'request_status':False,
                'refresh_token':'',
                'access_token':'',
                'error_code':error_code #loginSerializer.errors
            },
            status=status.HTTP_200_OK
        ) 
#USER_LOGIN  - END

#USER_LOGOUT  - START
@never_cache
@login_required
def user_logout_view(request):
    return render(
        request=request,
        template_name='user_management/user_logout.html'
    )
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.data.get('refreshToken'):
        refresh_token = request.data.get('refreshToken')
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            print('ERROR: ',e)
        finally:
            logout(request)
            return Response(
                data={
                    'request_status':True
                },
                status=status.HTTP_200_OK
            )
    else:
        #refres_token not available
        error_code = 'Token not found.'
        
    return Response(
        data={
            'request_status':False,
            'error_code':error_code
        },
        status=status.HTTP_200_OK
    )
#USER_LOGOUT  - END

#USER_UPDATE  - START
@login_required
def user_update_view(request,user_id):
    user2update = get_object_or_404(CustomUser,id=user_id)
    if request.user != user2update:
        return render(
            request=request,
            template_name='user_management/user_update.html',
            context={
                'user2update':user2update,
                'CustomUserMainForm':CustomUserMainForm(instance=user2update)
            }
        )
    else:
        #Same user, redirect to home page
        return redirect(reverse('user_management:home_view'))
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_update(request,user_id):
    user2update = get_object_or_404(CustomUser,id=user_id)
    error_msg = ''
    form_errors = ''
    if request.user == user2update:
        error_msg = 'You can not update your own information, please contact with other administrator.'
    else:
        if request.method == 'PUT' and request.data:
            userSerializer = CustomUserSerializer(instance=user2update,data=request.data,partial=True)
            if userSerializer.is_valid():
                userSerializer.save()
                return Response(
                    data={
                        'request_status':True,
                    },
                    status=status.HTTP_200_OK
                )
            else:
                form_errors = userSerializer.errors            
        else:
            error_msg = 'Request failed, please contact the administrator.'
            
    return Response(
        data={
            'request_status':False,
            'form_errors':form_errors,
            'error_msg':error_msg
        },
        status=status.HTTP_200_OK
    )
#USER_UPDATE  - END

#USER_DISABLE  - START
@login_required
def user_disable_view(request,user_id):
    user2update = get_object_or_404(CustomUser,id=user_id)
    if request.user != user2update:
        return render(
            request=request,
            template_name='user_management/user_disable.html',
            context={
                'user2update':user2update,
                'CustomUserMainForm':CustomUserMainForm(instance=user2update)
            }
        )
    else:
        #Same user, redirect to home page
        return redirect(reverse('user_management:home_view'))
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def user_partial_update(request,user_id):
    user2update = get_object_or_404(CustomUser,id=user_id)
    error_msg = ''
    form_errors = ''
    if request.user == user2update:
        error_msg = 'You can not update your own information, please contact with other administrator and try again.'
    else:
        if request.method == 'PATCH' and request.data:
            userSerializer = CustomUserSerializer(instance=user2update,data=request.data,partial=True)
            if userSerializer.is_valid():
                userSerializer.save()
                return Response(
                    data={
                        'request_status':True,
                    },
                    status=status.HTTP_200_OK
                )
            else:
                form_errors = userSerializer.errors   
        else:
            error_msg = 'Request failed, please contact the administrator.'
            
    return Response(
        data={
            'request_status':False,
            'form_errors':form_errors,
            'error_msg':error_msg
        },
        status=status.HTTP_200_OK
    )
#USER_DISABLE  - END

#OTHERS ENDPOINTS
@never_cache
@api_view(['POST'])
def tokenLogout(request):
    logout(request)
    return Response(
        data={
            'request_status':True,
        },
        status=status.HTTP_200_OK
    )
     

    

