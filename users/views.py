from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, LogoutView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('signin')
    template_name = 'reg.html'

class SignIn(LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')
    template_name = 'authForm.html'
    redirect_authenticated_user = True

class SignOut(LogoutView):
    next_page = reverse_lazy('index')

class PassChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "changePassword.html"

class PassChangeDone(PasswordChangeDoneView):
    template_name = "changePasswordDone.html"

class PassReset(PasswordResetView):
    template_name = "resetPassword.html"
    email_template_name = "resetPasswordEmail.html"
    success_url = reverse_lazy("password_reset_done")

    def form_valid(self, form):
        if form.cleaned_data['email'] is not None:
            email = form.cleaned_data['email']
            users = User.objects.filter(email=email)
            if users.exists():
                user = users.first()  # Получаем первого найденного пользователя
                uid = urlsafe_base64_encode(force_str(user.pk).encode('utf-8'))  # Кодируем ID пользователя в uid
                token = default_token_generator.make_token(user)  # Генерируем токен для сброса пароля
                                                    
                # Теперь отправляем письмо с корректным uid и token
                self.send_password_reset_email(user.email, uid, token)
                messages.success(self.request, 'Информация о сбросе пароля отправлена на ваш email.')
                return render(self.request, self.template_name, {'email': user.email})  # Параметры для отображения в шаблоне
            else:
                messages.error(self.request, 'Пользователь с таким email не найден.')
                return self.form_invalid(form)
        else:
            return super().form_invalid(form)
        
    def send_password_reset_email(self, email, uid, token):
        context = {
            'email': email,
            'protocol': self.request.scheme,  # http или https
            'domain': self.request.get_host(),  # Получение домена
            'uid': uid,
            'token': token,
        }
        subject = "Сброс пароля"
        html_message = render_to_string(self.email_template_name, context)
        email_message = EmailMessage(subject, html_message, to=[email])
        email_message.content_subtype = "html"  # Укажите, что контент - HTML
        email_message.send()


class PassResetDone(PasswordResetDoneView):
    template_name = "resetPasswordDone.html"

@login_required
def custom_userpage(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'customPage.html', {'user':user})

@login_required
def send_message(request, recipient_id):
    if request.method == 'POST':
        recipient = User.objects.get(pk = recipient_id)
        if recipient == request.user:
            messages.error(request, 'Нельзя отправлять сообщения самому себе')
            return redirect('index')
        subject = request.POST.get('subject')
        message_body = request.POST.get('message_body')
        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            subject=subject,
            message_body=message_body
        )
        return redirect('message_sent')
    else:
        recipient = User.objects.get(pk=recipient_id)
        return render(request, 'send_message.html', {'recipient':recipient})
    
def message_sent(request):
    return render(request, 'message_sent.html')

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'inbox.html', {'messages':messages})

@login_required
def outbox(request):
    messages = Message.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'outbox.html', {'messages':messages})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        if message.sender == request.user:
            message.delete()
            return redirect('outbox')
        else:
            message.delete()
            return redirect('inbox')