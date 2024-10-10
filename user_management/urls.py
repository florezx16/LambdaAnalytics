from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

userManagement_patterns = ([
    path(route='user_home_view/',view=views.user_home_view,name='home_view'),
    path(route='user_list_view/',view=views.user_list_view, name='user_list_view'),
    
    path(route='user_add_view/',view=views.user_add_view,name='user_add_view'),
    path(route='user_add/',view=views.user_add, name='user_add'),#Endpoint
    
    path(route='user_login_view/',view=views.user_login_view, name='user_login_view'),
    path(route='user_login/',view=views.user_login, name='user_login'),#Endpoint
    
    path(route='user_logout_view/',view=views.user_logout_view, name='user_logout_view'),
    path(route='user_logout/',view=views.user_logout, name='user_logout'),#Endpoint
    
    path(route='user_update_view/<int:user_id>/',view=views.user_update_view, name='user_update_view'),
    path(route='user_update/<int:user_id>/',view=views.user_update, name='user_update'),#Endpoint
    
    path(route='user_disable_view/<int:user_id>/',view=views.user_disable_view, name='user_disable_view'),
    path(route='user_partial_update/<int:user_id>/',view=views.user_partial_update, name='user_partial_update'),#Endpoint
    
    path(route='tokenLogout/',view=views.tokenLogout, name='tokenLogout'),#Endpoint
    path(route='api/token',view=TokenObtainPairView.as_view(),name='token_obtain_pair'),#Endpoint
    path(route='api/token/refresh',view=TokenRefreshView.as_view(),name='token_refresh')#Endpoint
],'user_management')