from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name = 'signup'),
    path('signin/', views.SignIn.as_view(), name = 'signin'),
    path('signout/', views.SignOut.as_view(), name = 'signout'),
    path('passchange/', views.PassChange.as_view(), name = 'pass_change'),
    path('passchangedone/', views.PassChangeDone.as_view(), name = 'password_change_done'),
    path('passreset/', views.PassReset.as_view(), name = 'password_reset'),
    path('passresetdone/', views.PassResetDone.as_view(), name = 'password_reset_done'),
    path('passresetconfirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('sendmessage/<int:recipient_id>/', views.send_message, name = 'send_message'),
    path('messagesent/', views.message_sent, name = 'message_sent'),
    path('custompage/<int:user_id>/', views.custom_userpage, name = 'custom_page'),
    path('inbox/', views.inbox, name = 'inbox'),
    path('outbox/', views.outbox, name = 'outbox'),
    path('messagedel/<int:message_id>/', views.delete_message, name = 'message_del'),
]
