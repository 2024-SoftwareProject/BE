from django.conf import settings

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate, update_session_auth_hash
from django import forms
from django.views.generic import CreateView, FormView, TemplateView
from django.views.generic import View

from django.contrib.auth.forms import UserChangeForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.contrib import messages
from django.urls import reverse
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError

from .models import User
from .forms import SignupForm, LoginForm
from .forms import CustomUserChangeForm, CheckPasswordForm
from .forms import RecoveryIdForm, RecoveryPwForm
from .forms import CustomPasswordChangeForm, CustomSetPasswordForm

from .helper import send_mail
from .decorators import login_message_required, admin_required, logout_message_required
from django.utils.decorators import method_decorator

# Create your views here.


# 회원가입 인증메일 발송 안내 창
def signup_success(request):
    if not request.session.get('signup_auth', False):
        raise PermissionDenied
    request.session['signup_auth'] = False
    return render(request, 'accounts/signup_success.html')


# 회원가입 약관동의
@method_decorator(logout_message_required, name='dispatch')
class Agreement(View):
    def get(self, request, *args, **kwargs):
        request.session['agreement'] = False
        return render(request, 'accounts/agreement.html')
    def post(self, request, *args, **kwarg):
        if request.POST.get('agreement1', False) and request.POST.get('agreement2', False):
            request.session['agreement'] = True
            if request.POST.get('signup') == 'signup':       
                return redirect('/accounts/signup/')
            else:
                return redirect('/accounts/signup/')
        else:
            messages.info(request, "약관에 모두 동의해주세요.")
            return render(request, 'accounts/agreement.html')  
    

# 회원가입
class signup(CreateView):
    model = User
    template_name = 'accounts/signup.html'
    form_class = SignupForm

    def get(self, request, *args, **kwargs):
        if not request.session.get('agreement', False):
            raise PermissionDenied
        request.session['agreement'] = False
        if request.user.is_authenticated:
            return redirect('home')
        
    def get_success_url(self):
        self.requst.session['signup_auth'] = True
        messages.success(self.request, '회원님의 입력한 Email 주소로 인증 메일이 발송되었습니다. 인증 후 로그인이 가능합니다')
        return reverse('accounts:signup_success')
    
    def form_valid(self, form):
        self.object = form.save()
        send_mail(
            '{}님의 회원가입 인증메일 입니다.'.format(self.object.user_id),
            [self.object.email],
            html = render('accounts/signup_email.html',{
                'user':self.object,
                'uid': urlsafe_base64_encode(force_bytes(self.object.pk)).encode().decode(),
                'domain': self.request.META['HTTP_HOST'],
                'token': default_token_generator.make_token(self.object),
            }),
        )
        return redirect(self.get_success_url())


# 로그인
@method_decorator(logout_message_required, name='dispatch')
class login(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = 'home'

    def form_valid(self, form):
        email = form.cleand_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            self.request.session['email'] = email
            login(self.request, user)

            remember_session = self.request.POST.get('remember_session',False)
            if remember_session:
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
        return super().form_valid(form)


    # #로그인 되면 메인으로 리다이렉트
    # if request.user.is_authenticated:
    #     return redirect('home')
    
    # if request.method == 'POST':
    #     form = AuthenticationForm(request, request.POST)
    #     if form.is_valid():
    #         auth_login(request, form.get_user())
    #         return redirect('home')
    # else:
    #     form = AuthenticationForm()
    # context = {'form': form}
    # return render(request, 'accounts/login.html', context)


# 로그아웃
@require_POST
def logout(request):
    if request.method == 'POST':
        auth_logout(request)
    return redirect('home')


# 계정 삭제
@login_required
def delete_account(request):
    if request.method == 'POST':
        password_form = CheckPasswordForm(request.user, request.POST)

        if password_form.is_valid():
            request.user.delete()
            logout(request)
            messages.success(request, "회원탈퇴가 완료되었습니다.")
            return redirect('home')
    else :
        password_form = CheckPasswordForm(request.user)

    return render(request, 'accounts/delete_profile.html', {'password_form':password_form})


# 계정 수정
@login_required
def update_account(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {'form':form}
    return render(request, 'accounts/update_profile.html', context)


# 마이페이지
@login_required
def mypage(request):
    if request.method == 'POST':
        return render(request, 'accounts/mypage.html')


# 이메일 인증 활성화
def activate(request, uid64, token):
    try:
        uid = str(urlsafe_base64_decode(uid64))
        model = get_user_model()
        current_user = model.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, model.DoesNotExist, ValidationError):
        messages.error(request, '메일 인증에 실패했습니다.')
        return redirect('login')

    if default_token_generator.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()

        messages.info(request, '메일 인증이 완료 되었습니다. 회원가입을 축하드립니다!')
        return redirect('login')

    messages.error(request, '메일 인증에 실패했습니다.')
    return redirect('login')


