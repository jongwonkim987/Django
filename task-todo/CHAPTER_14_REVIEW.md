# Chapter 14 구현 리뷰 — 코드 차이 분석 & 트러블슈팅

> **대상 프로젝트**: `live_section/restaurant_api/`
> **브랜치**: `chapter_14`

---

## 목차

1. [처음 작성한 코드 vs 가이드 코드 차이](#1-처음-작성한-코드-vs-가이드-코드-차이)
2. [실제 실행 오류 & 트러블슈팅](#2-실제-실행-오류--트러블슈팅)
3. [핵심 개념 정리](#3-핵심-개념-정리)

---

## 1. 처음 작성한 코드 vs 가이드 코드 차이

### 1-1. `config/settings/` — import 방식

#### 처음 작성
```python
# local.py, prod.py
from .base import *  # 상대 import
```

#### 가이드 코드
```python
# local.py, prod.py
from config.settings.base import *  # 절대 import
```

#### 수정 이유
`from .base import *`는 상대 경로 import로, 모듈이 패키지 내부에서 직접 import될 때는 동작하지만
Django의 `DJANGO_SETTINGS_MODULE` 환경변수로 로드되는 구조에서는 절대 경로 import가 더 명확하고 안전합니다.
`config.settings.settings`처럼 전체 경로로 지정하는 방식과 일관성을 유지하기 위해 절대 import를 사용합니다.

---

### 1-2. `config/settings/base.py` — INSTALLED_APPS 구조

#### 처음 작성
```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    # ... Django 기본 앱
    "django_extensions",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_cleanup.apps.CleanupConfig",
    # ... 로컬 앱
    "users",
    "restaurants",
    "reviews",
]
```

#### 가이드 코드
```python
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CUSTOM_APPS = [
    'users',
    'restaurants',
    'reviews',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_cleanup',
    'drf_yasg',
]

INSTALLED_APPS = DJANGO_APPS + CUSTOM_APPS + THIRD_PARTY_APPS
```

#### 수정 이유
- **가독성**: Django 기본 앱 / 외부 라이브러리 / 직접 만든 앱을 분리하면 어떤 앱이 어디서 왔는지 한눈에 파악 가능
- **유지보수성**: 앱을 추가/삭제할 때 해당 그룹만 수정하면 되므로 실수 방지
- **협업**: 팀원이 코드를 읽을 때 구조를 빠르게 이해할 수 있음
- `django_cleanup.apps.CleanupConfig` → `django_cleanup`으로 변경: 가이드 코드 스타일에 맞춤 (두 방식 모두 동작하지만 짧은 형태 사용)

---

### 1-3. `SIMPLE_JWT` 설정 — 세부 옵션

#### 처음 작성
```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "UPDATE_LAST_LOGIN": True,
}
```

#### 가이드 코드
```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),  # hours=1과 동일하지만 명시적
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",                            # JWT 서명 알고리즘 명시
}
```

#### 수정 이유
- `timedelta(hours=1)` vs `timedelta(minutes=60)`: 결과는 동일하지만 "60분"이라고 명시하면 직관적
- `ALGORITHM: "HS256"` 추가: simplejwt의 기본값이 이미 HS256이지만, 사용 중인 알고리즘을 명시적으로 선언하면 보안 감사(audit) 시 설정을 한눈에 파악 가능

---

### 1-4. `drf_yasg` (Swagger) — 처음에 누락

#### 처음 작성
`drf_yasg` 관련 코드 없음.

#### 가이드 코드
**설치:**
```bash
pip install drf-yasg
```

**`config/settings/base.py`:**
```python
THIRD_PARTY_APPS = [
    ...
    'drf_yasg',
]
```

**`config/schema.py` (신규 생성):**
```python
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Restaurant API',
        default_version='v1',
        description='Restaurant Review API Documentation',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
```

**`config/urls.py`:**
```python
from config.schema import schema_view

urlpatterns = [
    ...
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

#### 수정 이유
API 문서 자동화 도구인 Swagger UI / ReDoc을 제공하기 위해 추가합니다.
`drf_yasg`를 사용하면 URL 패턴과 Serializer를 분석해 자동으로 API 명세를 생성하므로,
별도로 문서를 작성하지 않아도 `/swagger/`에서 인터랙티브 문서를 확인할 수 있습니다.

---

### 1-5. `users/urls.py` — JWT URL 이름 차이

#### 처음 작성
```python
urlpatterns = [
    ...
    path("jwt/login/", TokenObtainPairView.as_view(), name="jwt-login"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),     # ❌
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),  # ❌
]
```

#### 가이드 코드
```python
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('login/jwt/', TokenObtainPairView.as_view(), name='jwt-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),  # ✅
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),     # ✅
    path('signup/', views.UserSignupView.as_view(), name='user-signup'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('profile/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
]
```

#### 수정 이유
URL 이름(`name=`)은 테스트 코드의 `reverse()` 호출과 반드시 일치해야 합니다.

```python
# users/tests.py
response = self.client.post(reverse('token-verify'), ...)   # 'jwt-verify'면 NoReverseMatch 오류
response = self.client.post(reverse('token-refresh'), ...)  # 'jwt-refresh'면 NoReverseMatch 오류
```

가이드 테스트 코드가 `token-verify`, `token-refresh`를 사용하므로 URL name을 맞춰야 합니다.
또한 URL 경로 구조도 변경되었습니다:
- 처음: `jwt/verify/`, `jwt/refresh/` (jwt 접두사)
- 가이드: `token/verify/`, `token/refresh/` (token 접두사 — simplejwt 관례 따름)

---

### 1-6. `users/tests.py` — JWT 테스트 상세도 차이

#### 처음 작성
```python
def test_jwt_login(self):
    data = {'email': self.data['email'], 'password': self.data['password']}
    response = self.client.post(reverse('jwt-login'), data)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('access', response.data)
    self.assertIn('refresh', response.data)
    # last_login 검증 없음 ❌
```

#### 가이드 코드
```python
def test_jwt_login(self):
    user = User.objects.create_user(**self.data)
    data = {'email': user.email, 'password': 'testpassword1234'}

    response = self.client.post(reverse('jwt-login'), data)
    last_login = user.last_login          # 로그인 전 last_login 저장
    user.refresh_from_db()               # DB에서 최신 상태 다시 로드

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('access', response.data)
    self.assertIn('refresh', response.data)
    self.assertNotEqual(user.last_login, last_login)  # last_login 변경됐는지 검증 ✅
```

```python
def test_jwt_verify(self):
    user = User.objects.create_user(**self.data)
    refresh = RefreshToken.for_user(user)    # 직접 토큰 생성 ✅
    access = str(refresh.access_token)

    response = self.client.post(path=reverse('token-verify'), data={'token': access})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
```

#### 수정 이유
- **`test_jwt_login`**: `UPDATE_LAST_LOGIN = True` 설정이 실제로 동작하는지 검증합니다. 로그인 전후 `last_login` 필드를 비교해 설정이 적용되었는지 확인하는 것이 TDD의 핵심입니다.
- **`test_jwt_verify` / `test_jwt_refresh`**: API 엔드포인트를 거쳐 토큰을 받는 대신 `RefreshToken.for_user(user)`로 직접 토큰을 생성합니다. 이렇게 하면 verify/refresh 테스트가 login API의 성공 여부에 **의존하지 않아** 테스트가 독립적(isolated)이 됩니다.

---

### 1-7. `reviews/serializers.py` — fields 선언 방식

#### 처음 작성
```python
class ReviewSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user", "restaurant", "title", "comment"]  # 명시적 필드 ❌
        read_only_fields = ["id", "restaurant"]
```

#### 가이드 코드
```python
class ReviewSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'          # 전체 필드 ✅
        read_only_fields = ["id", "restaurant"]
```

#### 수정 이유
가이드 코드는 `fields = '__all__'`을 사용합니다.
`__all__`을 사용하면 모델에 새 필드가 추가되어도 serializer 수정 없이 자동 반영됩니다.
`read_only_fields`로 특정 필드의 쓰기를 제한하면서도 모든 필드를 응답에 포함할 수 있습니다.
단, 민감한 정보가 있는 모델에서는 명시적 필드 선언이 더 안전합니다.

---

## 2. 실제 실행 오류 & 트러블슈팅

### 오류 1: MySQL 접속 실패로 테스트 DB 생성 불가

#### 오류 메시지
```
MySQLdb.OperationalError: (1045, "Access denied for user 'root'@'localhost' (using password: YES)")

django.db.utils.OperationalError: (1045, "Access denied for user 'root'@'localhost' (using password: YES)")
```

#### 발생 상황
```bash
python manage.py test
```
실행 직후, 테스트 데이터베이스(test_restaurant_db)를 MySQL에 생성하려는 시점에 발생.

#### 원인 분석
```
settings.py → local.py (심볼릭 링크)
local.py의 DATABASES → MySQL 설정
```
`python manage.py test`는 테스트 전용 DB(`test_<NAME>`)를 자동으로 생성합니다.
로컬 개발 환경의 MySQL 접속 정보(secret.json)가 테스트 환경에서는 올바르지 않거나,
테스트 DB 생성 권한이 없어 접속이 거부됩니다.

#### 실패한 시도 — `TEST` 키 추가
```python
# local.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        ...
        'TEST': {
            'ENGINE': 'django.db.backends.sqlite3',  # ❌ 이 방법은 동작하지 않음
            'NAME': BASE_DIR / 'test_db.sqlite3',
        },
    }
}
```
**왜 안 되는가**: `TEST` 딕셔너리는 테스트 DB의 **이름, 문자셋 등**을 덮어쓸 수 있지만, `ENGINE`은 변경할 수 없습니다. 상위 `ENGINE`이 MySQL이면 테스트 DB도 MySQL로 생성됩니다.

```
AttributeError: 'PosixPath' object has no attribute 'startswith'
```
SQLite의 `PATH` 타입을 MySQL 백엔드가 처리하려다 발생한 추가 오류입니다.

#### 해결 방법 — `test.py` 분리
```python
# config/settings/test.py (신규 생성)
from config.settings.base import *

DEBUG = True
ALLOWED_HOSTS = []

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / '.static_root'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# SQLite 사용 — 설치 불필요, 빠름, 독립적
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }
}
```

**테스트 실행 명령어:**
```bash
python manage.py test --settings=config.settings.test
```

**왜 이 방법인가**:
- 테스트는 외부 DB 서버에 의존하면 CI/CD 환경에서 불안정해집니다
- SQLite는 파일 기반(또는 메모리 기반)으로 추가 서버 없이 독립적으로 동작합니다
- `test.py`를 별도 파일로 분리하면 local/prod 설정을 건드리지 않아도 됩니다

---

### 오류 2: `test_user_signup` — email이 빈 문자열로 반환

#### 오류 메시지
```
FAIL: test_user_signup (users.tests.UserAPITestCase.test_user_signup)
AssertionError: '' != 'test@example.com'
```

#### 발생 상황
```python
# 테스트 코드
def test_user_signup(self):
    response = self.client.post(reverse('user-signup'), self.data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # ✅ 통과
    self.assertEqual(User.objects.count(), 1)                        # ✅ 통과
    self.assertEqual(response.data.get('nickname'), 'testuser')      # ✅ 통과
    self.assertEqual(response.data.get('email'), 'test@example.com') # ❌ 실패 ('' != 'test@example.com')
```

유저는 생성되었는데(`count() == 1`) 응답의 `email`이 빈 문자열입니다.

#### 원인 분석 — 단계별 추적

**Step 1: 어떤 serializer가 사용되는가?**
```python
class UserSignupView(CreateAPIView):
    serializer_class = UserDetailSerializer  # 이 serializer가 CREATE에 사용됨
```

**Step 2: `UserDetailSerializer`의 fields 확인**

DRF 쉘에서 직접 확인:
```python
from users.serializers import UserDetailSerializer
s = UserDetailSerializer()
for name, field in s.fields.items():
    print(f'{name}: read_only={field.read_only}, required={field.required}')
```

출력:
```
id:            read_only=True,  required=False
nickname:      read_only=False, required=True
email:         read_only=True,  required=False  ← ❗ 문제 발견!
password:      read_only=False, required=True
profile_image: read_only=False, required=False
```

**`email: read_only=True`** — email 필드가 읽기 전용으로 처리되고 있습니다!

**Step 3: 왜 email이 read_only인가?**

`UserDetailSerializer.Meta`를 확인합니다:
```python
# 실제 파일 (users/serializers.py)
class Meta:
    model = User
    fields = ["id", "nickname", "email", "password", "profile_image"]
    read_only_fields = ["id", "email"]  ← email이 포함되어 있음!
```

**Step 4: read_only=True이면 무슨 일이 생기는가?**

DRF에서 `read_only=True`인 필드는:
1. 클라이언트가 보낸 POST 데이터에서 **무시**됩니다
2. `validated_data`에 **포함되지 않습니다**
3. 응답(serialization)에는 **포함됩니다** — 하지만 값을 model instance에서 읽어옵니다

```python
# DRF ModelSerializer.create() 기본 동작
def create(self, validated_data):
    # validated_data = {'nickname': 'testuser', 'password': 'testpassword1234'}
    # email이 없음! read_only라서 제외됨
    instance = User.objects.create(**validated_data)
    return instance
```

**Step 5: email 없이 User가 생성되면?**

```python
User.objects.create(nickname='testuser', password='plain')
# email 필드에 값이 없음
# Django EmailField의 DB 기본값 = '' (빈 문자열)
# → user.email = ''
```

Unique 제약이 있음에도 빈 문자열('')이 저장되는 이유:
- 처음 생성 시에는 email=''로 저장됩니다 (테스트 DB 초기화 후 첫 번째 유저)
- 만약 두 번째 유저를 같은 방식으로 생성하면 IntegrityError 발생

**Step 6: 응답에서 email='' 반환**

```python
# 생성된 user.email = ''
# UserDetailSerializer가 user를 직렬화할 때
# email 필드는 read_only → user.email 값 그대로 반환
# response.data['email'] = ''
```

#### 코드 흐름 전체 요약

```
POST /users/signup/ {'email': 'test@example.com', ...}
    ↓
UserSignupView.create()
    ↓
UserDetailSerializer(data=request.data).is_valid()
    ↓ email이 read_only_fields에 있으므로 validated_data에서 제외
validated_data = {'nickname': 'testuser', 'password': 'testpassword1234'}
    ↓
User.objects.create(**validated_data)  ← email 없이 생성!
    ↓
user.email = ''  (DB 기본값)
    ↓
UserDetailSerializer(user).data
    ↓
response.data = {'email': '', 'nickname': 'testuser', ...}
    ↓
AssertionError: '' != 'test@example.com'
```

#### 가이드 코드와의 차이 — 핵심

| 구분 | 실제 파일 | 가이드 레퍼런스 코드 |
|------|-----------|----------------------|
| read_only 선언 | `read_only_fields = ["id", "email"]` | `READ_ONLY_FIELDS = ['id', 'email']` |
| DRF 인식 여부 | **인식함** (소문자, 올바른 속성명) | **무시됨** (대문자 오타, DRF가 모름) |
| email의 read_only | `True` → validated_data에서 제외 | `False` → validated_data에 포함 |
| 생성된 user.email | `''` | `'test@example.com'` |

가이드 레퍼런스 코드의 `READ_ONLY_FIELDS`(대문자)는 **의도적인 오타**가 아니라 실수지만,
결과적으로 email이 `read_only`가 되지 않아 signup이 정상 동작했습니다.
실제 프로젝트 파일은 `read_only_fields`(소문자)를 사용해 DRF가 정상 인식했고, email이 `read_only=True`가 되어 버그가 발생했습니다.

#### 해결 방법

```python
# users/serializers.py — UserDetailSerializer.Meta
class Meta:
    model = User
    fields = ["id", "nickname", "email", "password", "profile_image"]
    read_only_fields = ["id"]  # email 제거 ✅
```

**왜 email을 read_only_fields에서 제거했는가?**

`UserDetailSerializer`는 두 가지 용도로 사용됩니다:
1. **회원가입(CREATE)**: email을 POST 데이터에서 받아 저장해야 함 → `read_only=False` 필요
2. **프로필 수정(UPDATE)**: email은 변경하면 안 됨 → `update()` 메서드가 email을 처리하지 않으면 됨

`read_only_fields`에서 email을 제거하면:
- CREATE 시: email이 `validated_data`에 포함 → 정상 저장
- UPDATE 시: email이 POST로 전송되더라도 `update()` 메서드가 email을 업데이트하지 않으므로 실질적으로 변경 불가

**`update()` 메서드 확인:**
```python
def update(self, instance, validated_data):
    instance.nickname = validated_data.get('nickname', instance.nickname)
    # email 처리 없음 → PATCH 요청에 email이 포함되어도 무시됨
    password = validated_data.get('password', None)
    if password:
        instance.set_password(password)
    instance.save()
    return instance
```

#### 최종 테스트 결과

```
Ran 23 tests in 5.771s
OK
```

모든 23개 테스트 통과.

---

## 3. 핵심 개념 정리

### DRF `read_only_fields` 동작 원리

```python
class Meta:
    read_only_fields = ['email']   # ← 소문자, DRF가 인식
    READ_ONLY_FIELDS = ['email']   # ← 대문자, DRF가 무시 (일반 파이썬 클래스 속성)
    readonly_fields = ['email']    # ← DRF가 경고 + AssertionError 발생
```

DRF `ModelSerializer`는 내부적으로 `getattr(self.Meta, 'read_only_fields', None)`으로 체크하므로
**대소문자가 정확히 일치**해야 합니다.

`read_only=True`인 필드의 동작:

| 상황 | 동작 |
|------|------|
| 클라이언트가 값을 전송 | 무시됨 (validated_data 미포함) |
| DB에서 읽어 응답 | 포함됨 (to_representation 실행) |
| CREATE 시 | validated_data 없음 → DB 기본값 사용 |
| UPDATE 시 | validated_data 없음 → 기존값 유지 |

### Django 테스트 DB 설정 전략

| 전략 | 방법 | 장점 | 단점 |
|------|------|------|------|
| 운영 DB로 테스트 | 기본 settings 사용 | 실제 환경과 동일 | 느림, 권한 필요, CI 어려움 |
| `test.py` 별도 분리 | `--settings=config.settings.test` | 독립적, 빠름 | 명령어에 옵션 추가 필요 |
| `pytest-django` | `@pytest.mark.django_db` | 강력한 fixture | pytest 설치 필요 |

### simplejwt `UPDATE_LAST_LOGIN` 설정 검증 방법

```python
def test_jwt_login(self):
    user = User.objects.create_user(**self.data)

    last_login_before = user.last_login  # 로그인 전: None

    response = self.client.post(reverse('jwt-login'), {...})

    user.refresh_from_db()  # ← 반드시 DB에서 다시 로드해야 최신값 반영

    self.assertNotEqual(user.last_login, last_login_before)
    # 로그인 후: datetime.now() 값이 저장되어 있음
```

`user.refresh_from_db()`를 호출하지 않으면 Python 메모리의 캐시된 값이 사용되어 검증이 무의미해집니다.
