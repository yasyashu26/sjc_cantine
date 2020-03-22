from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/',views.signup,name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
     path('signup/confirmation',views.signup_confirmation,name='signup_confirmation'),
    path('settings/password', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
    name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
    name='password_change_done'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    url(r'^reset/$',
    auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt'
    ),
    name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    #auth for admin staff
    path('staff_admin/login/', auth_views.LoginView.as_view(template_name='login_admin.html'), name='login_admin'),
    path('staff_admin/signup/', views.signup_admin, name='signup_admin'),
    url(r'^activate/admin/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate_admin, name='activate_admin'),
    path('login_success/', views.login_success, name='login_success'),
    ]