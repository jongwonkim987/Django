# utils/email.py
from django.core.mail import send_mail as django_send_mail
from django.core.signing import TimestampSigner
from django.conf import settings


def send_verification_email(request, user):
    """
    TimestampSigner 로 email 을 서명한 뒤,
    인증 링크를 이메일로 발송합니다.
    """
    signer = TimestampSigner()
    # 이메일 주소를 서명하여 인증 코드 생성
    signed_code = signer.sign(user.email)

    # 절대 URL 생성 (예: http://127.0.0.1:8000/users/verify/?code=...)
    verify_url = request.build_absolute_uri(
        f'/users/verify/?code={signed_code}'
    )

    subject = '[Todo App] 이메일 인증을 완료해주세요'
    message = (
        f'안녕하세요, {user.name}님!\n\n'
        '아래 링크를 클릭하면 이메일 인증이 완료됩니다.\n'
        '링크는 발급 후 1시간 동안 유효합니다.\n\n'
        f'{verify_url}\n\n'
        '본인이 가입하지 않으셨다면 이 메일을 무시해주세요.'
    )

    django_send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )
