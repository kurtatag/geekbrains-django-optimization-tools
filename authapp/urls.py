from django.urls import path

import authapp.views as authapp_views

app_name = 'mainapp'

urlpatterns = [
    path('login/', authapp_views.Login.as_view(), name='login'),
    path('logout/', authapp_views.Logout.as_view(), name='logout'),
    path('register/', authapp_views.Register.as_view(), name='register'),
    path('edit/', authapp_views.EditUser.as_view(), name='edit'),
    path(
        'verify/<str:email>/<str:activation_key>/',
        authapp_views.Verify.as_view(),
        name='verify'
    ),
]
