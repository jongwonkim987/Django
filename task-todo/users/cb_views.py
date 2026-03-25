# users/cb_views.py
from django.contrib.auth import login as django_login
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from users.forms import SignupForm, LoginForm
from users.models import User
from utils.email import send_verification_email


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        # 유저 저장 (is_active=False 상태)
        user = form.save()
        # 이메일 인증 메일 발송
        send_verification_email(self.request, user)
        # 인증 안내 페이지 렌더링
        return render(self.request, 'registration/signup_done.html')


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('todo_list')

    def get_form_kwargs(self):
        # AuthenticationForm 은 request 를 첫 번째 인자로 받음
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        # 인증된 유저를 세션에 저장
        django_login(self.request, form.get_user())
        return super().form_valid(form)


def verify_email(request):
    """
    쿼리 파라미터 code 를 TimestampSigner 로 unsign 하여
    해당 이메일의 유저를 활성화합니다.
    """
    code = request.GET.get('code', '')

    if not code:
        return render(request, 'registration/verify_failed.html')

    signer = TimestampSigner()
    try:
        # max_age=3600 → 1시간 이내 서명만 유효
        email = signer.unsign(code, max_age=3600)
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        return render(request, 'registration/verify_success.html')
    except SignatureExpired:
        # 링크 만료
        return render(request, 'registration/verify_failed.html', {'reason': '인증 링크가 만료되었습니다.'})
    except (BadSignature, User.DoesNotExist):
        # 위조된 코드 또는 존재하지 않는 유저
        return render(request, 'registration/verify_failed.html', {'reason': '유효하지 않은 인증 링크입니다.'})
