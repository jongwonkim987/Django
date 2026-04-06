# Chapter 13 구현 리뷰 — 코드 차이 분석 & 트러블슈팅

> **대상 프로젝트**: `live_section/restaurant_api/`
> **브랜치**: `chapter_13`
> **관련 커밋**:
> - `ceeb02a` — chapter_12 초기 세팅 (내가 처음 작성한 코드)
> - `f7b9053` — 가이드라인과 차이나는 코드 수정
> - `8c48b7f` — chapter_13 인증/권한 및 CRUD 구현

---

## 목차

1. [Chapter 12 세팅 단계: 처음 코드 vs 가이드 코드 차이](#1-chapter-12-세팅-단계-처음-코드-vs-가이드-코드-차이)
2. [Chapter 13 구현 단계: 처음 코드 vs 가이드 코드 차이](#2-chapter-13-구현-단계-처음-코드-vs-가이드-코드-차이)
3. [실제 실행 오류 & 트러블슈팅](#3-실제-실행-오류--트러블슈팅)
4. [핵심 개념 정리](#4-핵심-개념-정리)

---

## 1. Chapter 12 세팅 단계: 처음 코드 vs 가이드 코드 차이

Chapter 13 기능을 구현하기 전, chapter_12 초기 세팅 코드를 가이드와 비교했을 때 발견된 차이들입니다.
`f7b9053` 커밋이 이 수정 내용을 담고 있습니다.

---

### 1-1. `secret.json` 로드 방식

#### 처음 작성
```python
# config/settings.py
secret_file = BASE_DIR / "secret.json"
with open(secret_file) as f:
    secrets = json.load(f)

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        raise Exception(f"Set the {setting} environment variable in secret.json")

SECRET_KEY = get_secret("SECRET_KEY")

# DB 설정
"NAME": get_secret("DB_NAME"),
"USER": get_secret("DB_USER"),
```

```json
// secret.json (평면 구조)
{
  "SECRET_KEY": "...",
  "DB_NAME": "restaurant_db",
  "DB_USER": "root"
}
```

#### 가이드 코드
```python
# config/settings.py
with open(BASE_DIR / "secret.json") as f:
    secret = f.read()

SECRET = json.loads(secret)
SECRET_KEY = SECRET["DJANGO_SECRET_KEY"]

# DB 설정
"NAME": SECRET["DB"]["NAME"],
"USER": SECRET["DB"]["USER"],
```

```json
// secret.json (중첩 구조)
{
  "DJANGO_SECRET_KEY": "...",
  "DB": {
    "NAME": "restaurant_db",
    "USER": "root",
    "PASSWORD": "...",
    "HOST": "localhost",
    "PORT": "3306"
  }
}
```

#### 수정 이유
- **키 이름 변경**: `"SECRET_KEY"` → `"DJANGO_SECRET_KEY"`. 나중에 다른 서비스의 SECRET_KEY와 혼동을 피하기 위해 Django용임을 명시합니다.
- **중첩 구조**: DB 관련 키를 `DB` 오브젝트 아래에 묶으면 `secret.json`이 여러 설정 항목을 담을 때 더 구조적입니다.
- **`get_secret()` 함수 제거**: 함수를 만들어 wrapping하는 것보다 `SECRET["KEY"]`로 직접 접근하는 것이 더 간결합니다. 키가 없으면 어차피 `KeyError`가 발생해 오류를 알 수 있습니다.
- **`json.load()` vs `json.loads()`**: `json.load(file_object)`도 동작하지만 가이드는 `f.read()`로 문자열을 읽은 뒤 `json.loads(string)`으로 파싱합니다.

---

### 1-2. `INSTALLED_APPS` — 앱 등록 방식

#### 처음 작성
```python
INSTALLED_APPS = [
    "django.contrib.admin",
    # ... Django 기본 앱
    "rest_framework",
    "django_cleanup.apps.CleanupConfig",
    # Local
    "users.apps.UsersConfig",
    "restaurants.apps.RestaurantsConfig",
    "reviews.apps.ReviewsConfig",
]
```

#### 가이드 코드
```python
INSTALLED_APPS = [
    "django.contrib.admin",
    # ... Django 기본 앱
    "django_extensions",         # ← 추가
    "rest_framework",
    "django_cleanup.apps.CleanupConfig",
    # Local
    "users",                     # ← 단순화
    "restaurants",               # ← 단순화
    "reviews",                   # ← 단순화
]
```

#### 수정 이유
- **`"users"` vs `"users.apps.UsersConfig"`**: 두 방식 모두 동작합니다. `"users.apps.UsersConfig"`는 앱 설정 클래스를 명시적으로 지정하는 방식이고, `"users"`는 Django가 자동으로 `UsersConfig`를 찾는 방식입니다. 가이드는 짧고 간결한 방식을 사용합니다.
- **`django_extensions` 추가**: `shell_plus`, `runserver_plus` 등 개발 편의 기능을 제공합니다. 초기 세팅에서 누락했습니다.

---

### 1-3. `AUTH_USER_MODEL` — 커스텀 유저 모델 참조

#### 처음 작성
```python
# settings.py
AUTH_USER_MODEL = "users.CustomUser"
```

```python
# users/models.py
class CustomUserManager(BaseUserManager):
    ...

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ...
```

#### 가이드 코드
```python
# settings.py
AUTH_USER_MODEL = "users.User"
```

```python
# users/models.py
class UserManager(BaseUserManager):
    ...

class User(AbstractBaseUser, PermissionsMixin):
    ...
```

#### 수정 이유
- **네이밍 간소화**: Django의 기본 모델 이름 규칙에 가깝게 `User`로 사용합니다. `CustomUser`라는 이름은 "이미 커스텀했다"는 사실을 강조하지만, 실제 코드에서는 그냥 `User`라고 부르는 것이 더 자연스럽습니다.
- **`AUTH_USER_MODEL`과 모델명 일치**: `AUTH_USER_MODEL = "users.User"`이면 `users/models.py`의 클래스 이름도 `User`여야 합니다. 이름이 일치하지 않으면 Django가 모델을 찾지 못해 마이그레이션 오류나 인증 오류가 발생합니다.

> ⚠️ **주의**: `AUTH_USER_MODEL`을 변경하면 **반드시 마이그레이션을 새로 생성**해야 합니다. 이미 DB에 테이블이 있다면 충돌이 생기므로, 프로젝트 초기에 결정하고 이후에는 바꾸지 않는 것이 원칙입니다.

---

### 1-4. `users/models.py` — `create_user` 시그니처

#### 처음 작성
```python
class CustomUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일은 필수입니다.")
        if not nickname:
            raise ValueError("닉네임은 필수입니다.")
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("슈퍼유저는 is_staff=True 이어야 합니다.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("슈퍼유저는 is_superuser=True 이어야 합니다.")
        return self.create_user(email, nickname, password, **extra_fields)
```

#### 가이드 코드
```python
class UserManager(BaseUserManager):
    def create_user(self, email, password, *args, **kwargs):
        if not email:
            raise ValueError("must have user email")
        user = self.model(email=self.normalize_email(email), *args, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, *args, **kwargs):
        user = self.create_user(
            email=self.normalize_email(email), password=password, *args, **kwargs
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
```

#### 수정 이유
- **시그니처 차이**: 처음 코드는 `create_user(email, nickname, password=None, ...)` — `nickname`이 두 번째 위치 인수입니다. 가이드는 `create_user(email, password, *args, **kwargs)` — `password`가 두 번째 위치 인수입니다.
- **Django `createsuperuser` 명령 호환성**: Django의 `createsuperuser` 명령은 `REQUIRED_FIELDS`에 선언된 필드를 입력받아 `create_superuser(email=..., password=..., nickname=...)`처럼 키워드 인수로 전달합니다. `password`가 위치 인수여야 일반적인 호출 패턴과 맞습니다.
- **`*args, **kwargs` 사용**: nickname 같은 추가 필드를 `model()` 생성자에 `*args, **kwargs`로 전달하면, 나중에 User 모델에 필드가 추가되어도 manager 코드를 수정하지 않아도 됩니다.
- **`create_superuser` 단순화**: 처음 코드는 `is_staff/is_superuser` 검증 로직을 추가했지만, 가이드는 검증 없이 바로 설정합니다. `create_superuser`는 Django 내부에서만 호출되므로 과도한 방어 코드는 불필요합니다.

---

### 1-5. `restaurants/models.py` — `description` 필드 누락

#### 처음 작성
```python
class Restaurant(BaseModel):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)   # ← description 없음
    contact = models.CharField(max_length=50)
    ...
```

#### 가이드 코드
```python
class Restaurant(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)  # ← 추가
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=50)
    ...
```

#### 수정 이유
가이드 명세에 포함된 필드인데 처음 작성 시 누락했습니다. `null=True, blank=True`로 선언해 선택적 입력으로 처리합니다. 이 필드가 없으면 테스트 코드의 `"description": "Test Description"` assertion이 실패합니다.

---

### 1-6. `reviews/models.py` — FK 참조 방식 및 `__str__`

#### 처음 작성
```python
from django.conf import settings

class Review(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,       # 문자열 참조
        on_delete=models.CASCADE,
        related_name="reviews",         # related_name 있음
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="reviews",         # related_name 있음
    )
    ...

    def __str__(self):
        return self.title               # 리뷰 제목 반환
```

#### 가이드 코드
```python
from django.contrib.auth import get_user_model

User = get_user_model()

class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   # 직접 모델 참조
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  # related_name 없음
    ...

    def __str__(self):
        return f"{self.restaurant.name} 리뷰"    # 레스토랑명 + "리뷰"
```

#### 수정 이유

**FK 참조 방식 변경: `settings.AUTH_USER_MODEL` → `get_user_model()`**

두 방식 모두 동작하지만 용도가 다릅니다:

| 방식 | 언제 사용 |
|------|-----------|
| `settings.AUTH_USER_MODEL` (문자열) | **모델 파일 최상단** (앱 로딩 순서 문제 방지) |
| `get_user_model()` | **모델 파일 내부** (이미 앱이 로드된 후) |

`get_user_model()`은 Django의 앱 레지스트리가 초기화된 이후에만 안전합니다. 모델 클래스 정의 시점(파일 로드 시)에는 아직 앱이 완전히 초기화되지 않을 수 있어, 엄밀히는 `settings.AUTH_USER_MODEL`이 더 안전하지만, 가이드는 `get_user_model()`을 사용합니다. 실제 Django 공식 문서도 모델 내 FK 정의에는 `settings.AUTH_USER_MODEL`을 권장합니다.

**`related_name` 제거**

`related_name="reviews"`가 없으면 역참조 시 `user.review_set.all()`을 사용합니다. 가이드는 역참조를 명시적으로 사용하지 않으므로 생략합니다.

**`__str__` 변경**

`return self.title`보다 `return f"{self.restaurant.name} 리뷰"`가 Django Admin에서 더 식별하기 쉬운 표현입니다.

---

### 1-7. `settings.py` — Static/Media URL 형식

#### 처음 작성
```python
STATIC_URL = "/static/"         # 앞뒤 슬래시
STATIC_ROOT = BASE_DIR / "static"     # STATICFILES_DIRS 없음

MEDIA_URL = "/media/"           # 앞뒤 슬래시
MEDIA_ROOT = BASE_DIR / "media"
```

#### 가이드 코드
```python
STATIC_URL = "static/"          # 뒤 슬래시만
STATICFILES_DIRS = [BASE_DIR / "static"]   # 개발 중 static 파일 위치
STATIC_ROOT = BASE_DIR / ".static_root"   # collectstatic 결과 위치 (점 포함)

MEDIA_URL = "media/"            # 뒤 슬래시만
MEDIA_ROOT = BASE_DIR / "media"
```

#### 수정 이유
- **앞 슬래시 제거**: `"/static/"` vs `"static/"` — Django 4.x 이상에서는 앞 슬래시 없이 상대 경로를 권장합니다. 차이는 거의 없지만 가이드 스타일에 맞춥니다.
- **`STATICFILES_DIRS` 추가**: `STATIC_ROOT`는 `collectstatic` 명령이 파일을 **모으는** 최종 폴더이고, `STATICFILES_DIRS`는 개발 중에 Django가 static 파일을 **찾는** 폴더입니다. 두 값이 같으면 `collectstatic`이 오류를 냅니다.
- **`STATIC_ROOT = BASE_DIR / ".static_root"`**: 점(`.`)으로 시작하는 폴더명을 사용하면 `.gitignore`에 `.static_root`로 명확히 추가할 수 있고, 일반 `static` 폴더와 혼동을 피할 수 있습니다.

---

### 1-8. 테스트 코드 스타일 — 데이터 선언 방식과 assertions 상세도

#### 처음 작성
```python
class RestaurantModelTest(TestCase):
    def setUp(self):
        self.restaurant_data = {   # ← 변수명 _data
            "name": "테스트 식당",   # ← 한글
            "address": "서울시 강남구 테스트로 123",
            ...
        }

    def test_create_restaurant(self):
        restaurant = Restaurant.objects.create(**self.restaurant_data)
        self.assertEqual(restaurant.name, self.restaurant_data["name"])
        self.assertIsNotNone(restaurant.created_at)   # ← created_at 확인
```

```python
class RestaurantViewTestCase(APITestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(...)   # ← setUp에서 미리 생성
        self.list_url = reverse("restaurant-list")         # ← URL 변수 저장
        self.detail_url = reverse("restaurant-detail", ...)

    def test_restaurant_post_view(self):
        data = {"name": "새 식당", ...}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 2)  # ← setUp에서 1개 있어서 2
```

#### 가이드 코드
```python
class RestaurantModelTest(TestCase):
    def setUp(self):
        self.restaurant_info = {   # ← 변수명 _info
            "name": "Test Restaurant",   # ← 영어
            "description": "Test Description",  # ← description 포함
            ...
        }

    def test_create_restaurant(self):
        restaurant = Restaurant.objects.create(**self.restaurant_info)

        self.assertEqual(Restaurant.objects.count(), 1)  # ← count 확인 추가
        self.assertEqual(restaurant.name, self.restaurant_info["name"])
        self.assertEqual(restaurant.description, self.restaurant_info["description"])
        self.assertEqual(restaurant.__str__(), self.restaurant_info["name"])  # ← __str__ 확인
        # created_at 확인 없음
```

```python
class RestaurantViewTestCase(APITestCase):
    def setUp(self):
        # setUp에서 restaurant 미리 생성하지 않음
        self.restaurant_info = {...}

    def test_restaurant_post_view(self):
        url = reverse("restaurant-list")  # ← 테스트마다 직접 reverse()
        response = self.client.post(url, self.restaurant_info, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Restaurant.objects.count(), 1)  # ← setUp에서 생성 안 했으니 1
        self.assertEqual(Restaurant.objects.first().name, self.restaurant_info["name"])
```

#### 수정 이유

**변수명: `restaurant_data` → `restaurant_info`**

이름이 다를 뿐 기능은 동일합니다. 가이드 스타일을 따릅니다.

**setUp에서 객체 미리 생성 vs 각 테스트에서 생성**

처음 코드는 `setUp()`에서 `Restaurant`을 미리 생성해 놓고 모든 테스트에서 공유했습니다. 가이드는 각 테스트에서 필요할 때 직접 생성합니다.

| 방식 | 장점 | 단점 |
|------|------|------|
| setUp에서 미리 생성 | 코드 중복 감소 | 테스트 간 의존성 생길 수 있음, count 계산 복잡 |
| 각 테스트에서 직접 생성 | 테스트 독립성 보장 | 약간 중복 코드 |

특히 `test_restaurant_post_view`에서 처음 코드는 setUp에서 이미 1개를 만들어 `count() == 2`로 검증했는데, 이는 각 테스트의 초기 상태가 다를 수 있어 혼란스럽습니다.

**`response.data` vs `response.data.get("results")` (Pagination 관련)**

Chapter 13에서 `DEFAULT_PAGINATION_CLASS`를 설정하면 리스트 응답이 페이지네이션 형태로 바뀝니다:

```json
// 페이지네이션 이전
[{"id": 1, "name": "..."}, ...]

// 페이지네이션 이후
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [{"id": 1, "name": "..."}, ...]
}
```

가이드 테스트는 `response.data.get("results")[0].get("name")`으로 pagination을 고려해 작성되었습니다.

---

## 2. Chapter 13 구현 단계: 처음 코드 vs 가이드 코드 차이

`8c48b7f` 커밋에서 구현한 내용과 가이드와의 차이입니다.

---

### 2-1. `config/settings.py` — REST_FRAMEWORK 설정

#### 처음 작성 (chapter_12에 이미 작성)
```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}
```

#### Chapter 13에서 수정한 최종 코드
```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
}
```

#### 수정 이유

**`BasicAuthentication` 제거**

`BasicAuthentication`은 요청마다 `Authorization: Basic base64(email:password)` 헤더를 전송하는 방식으로, 실제 서비스에서는 보안상 문제가 있습니다(매 요청에 비밀번호 전송). `SessionAuthentication`만으로 충분합니다.

**`PageNumberPagination` 추가**

리스트 API가 모든 데이터를 한 번에 반환하면 데이터가 많을 때 성능 문제가 발생합니다. 페이지네이션을 global 설정으로 추가해 모든 list API에 자동 적용합니다. `PAGE_SIZE: 10`은 한 페이지에 10개씩 반환합니다.

**리스트 자료형 `[]` → 튜플 `()`**

`DEFAULT_AUTHENTICATION_CLASSES`와 `DEFAULT_PERMISSION_CLASSES` 값을 리스트 `[]`에서 튜플 `()`로 변경했습니다. 기능 차이는 없지만 "변경되지 않는 설정값"임을 표현하는 Python 관례입니다.

---

### 2-2. `config/urls.py` — router import 방식

#### 처음 작성 (chapter_12)
```python
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("restaurants.urls")),   # 문자열로 include
]
```

#### Chapter 13에서 수정한 최종 코드
```python
from restaurants.urls import router as restaurants_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("", include(restaurants_router.urls)),   # router 객체를 직접 import
    path("", include("reviews.urls")),
]
```

#### 수정 이유
`include("restaurants.urls")`는 `restaurants/urls.py` 모듈 전체를 포함합니다. 이 방식은 `urlpatterns` 변수가 있을 때 동작합니다.

`restaurants/urls.py`가 `DefaultRouter`를 사용해 `router.urls`를 반환하는 구조라면, `include(router.urls)`처럼 **router 객체의 `urls` 속성**을 직접 전달하는 것이 더 명시적입니다. `include("restaurants.urls")`도 동작하지만, `restaurants/urls.py`에 `urlpatterns = router.urls`가 없으면 빈 URL 목록이 등록됩니다.

---

### 2-3. `users/serializers.py` — 세 가지 Serializer 설계

#### 처음 구상 (가이드 확인 전)

처음에는 회원가입과 프로필 조회/수정을 하나의 `UserSerializer`로 처리하려 했습니다.

#### 가이드 코드 (세 가지 분리)

```python
# ① 회원가입 전용
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "nickname", "email", "password", "is_staff", "is_superuser"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        if password is None:
            raise serializers.ValidationError("Password is required.")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


# ② 프로필 조회/수정 전용
class UserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "nickname", "email", "password", "profile_image"]
        read_only_fields = ["id", "email"]

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get("nickname", instance.nickname)
        password = validated_data.get("password", None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


# ③ 로그인 전용 (ModelSerializer 아닌 Serializer)
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = authenticate(request=self.context.get("request"), **attrs)
        if not user:
            raise serializers.ValidationError(
                detail="Unable to log in with provided credentials.",
                code="authorization",
            )
        attrs["user"] = user
        return attrs
```

#### 설계 이유

| Serializer | 용도 | 핵심 특징 |
|------------|------|-----------|
| `UserSerializer` | 회원가입(POST) | `create()` 커스텀으로 비밀번호 해싱 처리 |
| `UserDetailSerializer` | 프로필 조회/수정(GET/PATCH) | `read_only_fields = ["id", "email"]`로 이메일 변경 불가, `update()` 커스텀 |
| `UserLoginSerializer` | 로그인(POST) | `ModelSerializer`가 아닌 일반 `Serializer`, `authenticate()`로 검증 |

**왜 `UserLoginSerializer`는 `Serializer`인가?**

로그인은 DB에 데이터를 생성/수정하지 않습니다. 단순히 email + password를 받아 유효성만 검사하면 되므로 모델과 연결된 `ModelSerializer` 대신 일반 `Serializer`를 사용합니다.

---

### 2-4. `users/views.py` — UserSignupView의 serializer_class

#### 처음 작성 및 chapter_13 최종 코드
```python
class UserSignupView(CreateAPIView):
    serializer_class = UserDetailSerializer   # ← UserDetailSerializer 사용
    permission_classes = [AllowAny]
```

#### 가이드가 의도한 코드
```python
class UserSignupView(CreateAPIView):
    serializer_class = UserSerializer         # ← UserSerializer 사용
    permission_classes = [AllowAny]
```

#### 수정 이유와 결과
이 차이는 chapter_13에서는 바로 발견되지 않았고, **chapter_14에서 테스트 실패로 발견**되었습니다.

`UserDetailSerializer`는 `read_only_fields = ["id", "email"]`로 이메일을 읽기 전용으로 처리합니다. 회원가입 시 이메일을 입력받아야 하는데, `read_only=True` 필드는 요청 데이터에서 무시되어 email이 빈 문자열(`''`)로 저장됩니다.

자세한 분석은 [오류 2: email이 빈 문자열로 반환](#오류-2-test_user_signup--email이-빈-문자열로-반환)을 참조하세요.

---

### 2-5. `reviews/views.py` — ReviewDetailView의 `get_object()`

#### 처음 작성
```python
class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Review.objects.get(
            id=self.kwargs.get("review_id"), user=self.request.user
        )
```

#### 가이드 코드
```python
class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            user=self.request.user
        )
```

#### 수정 이유
`Review.objects.get()`은 조건에 맞는 객체가 없으면 `Review.DoesNotExist` 예외를 발생시킵니다. 이 예외는 Django가 HTTP 500(Internal Server Error)로 처리합니다.

`get_object_or_404()`를 사용하면 같은 상황에서 HTTP 404(Not Found)를 반환합니다. 클라이언트 입장에서 "없는 리소스"는 404가 맞는 응답이며, 500은 서버 오류로 오해될 수 있습니다.

```python
# Review.objects.get() → Review.DoesNotExist → 500 Internal Server Error ❌
# get_object_or_404()  → Http404            → 404 Not Found              ✅
```

---

### 2-6. `restaurants/tests.py` — 인증 추가

#### 처음 작성 (chapter_12)
```python
class RestaurantViewTestCase(APITestCase):
    def setUp(self):
        # 인증 없음
        self.restaurant_info = {...}
```

#### Chapter 13에서 수정한 최종 코드
```python
class RestaurantViewTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="password1234"
        )
        self.client.login(email="test@example.com", password="password1234")
        self.restaurant_info = {...}
```

#### 수정 이유
Chapter 13에서 `DEFAULT_PERMISSION_CLASSES = [IsAuthenticatedOrReadOnly]`를 추가했습니다. 이 설정의 의미:

| HTTP 메서드 | 인증 필요 |
|------------|-----------|
| GET (읽기) | 불필요 |
| POST, PUT, PATCH, DELETE (쓰기) | **필요** |

`test_restaurant_post_view`, `test_restaurant_update_view`, `test_restaurant_delete_view`는 쓰기 요청을 합니다. 인증 없이 요청하면 `HTTP 403 Forbidden`이 반환되어 테스트가 실패합니다. `setUp()`에서 미리 로그인해 놓으면 해당 테스트 클래스의 모든 테스트에서 인증된 상태로 요청합니다.

---

## 3. 실제 실행 오류 & 트러블슈팅

---

### 오류 1: `RestaurantViewTestCase` — 인증 관련 403 오류

#### 오류 메시지
```
FAIL: test_restaurant_post_view (restaurants.tests.RestaurantViewTestCase)
AssertionError: 403 != 201

FAIL: test_restaurant_update_view (restaurants.tests.RestaurantViewTestCase)
AssertionError: 403 != 200

FAIL: test_restaurant_delete_view (restaurants.tests.RestaurantViewTestCase)
AssertionError: 403 != 204
```

#### 발생 상황
Chapter 13에서 `settings.py`의 `REST_FRAMEWORK`에 아래를 추가한 직후 발생:

```python
REST_FRAMEWORK = {
    ...
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
}
```

기존 `RestaurantViewTestCase`는 인증 없이 모든 요청을 보냈기 때문에, 쓰기 요청(POST/PUT/DELETE)이 모두 `403 Forbidden`으로 거부됩니다.

#### 원인 분석

```
Permission 체크 흐름:
요청 → IsAuthenticatedOrReadOnly.has_permission()
       ↓
       GET 요청?  → True (허용)
       그 외?     → request.user.is_authenticated?
                      → True  → 허용
                      → False → 403 Forbidden ← 테스트가 여기에 걸림
```

테스트 클라이언트는 기본적으로 비인증 상태입니다. `self.client.post()`는 비인증 POST이므로 `IsAuthenticatedOrReadOnly`가 거부합니다.

#### 해결 방법

`setUp()`에서 테스트용 유저를 생성하고 로그인:

```python
class RestaurantViewTestCase(APITestCase):
    def setUp(self):
        # 1. 테스트 유저 생성
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="password1234"
        )
        # 2. 로그인 (이후 모든 요청에 Session 인증 적용)
        self.client.login(email="test@example.com", password="password1234")

        self.restaurant_info = {...}
```

`self.client.login()`은 Django의 세션 인증을 사용합니다. 로그인 후 테스트 클라이언트의 모든 요청에 세션 쿠키가 자동으로 포함되어 인증된 요청으로 처리됩니다.

> **참고**: `APITestCase`의 `self.client`는 DRF의 `APIClient`입니다. JWT 인증을 사용한다면 `self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)`으로 인증합니다. Chapter 13은 SessionAuthentication을 사용하므로 `client.login()`이 적합합니다.

---

### 오류 2: `test_user_signup` — email이 빈 문자열로 반환

> **이 오류는 chapter_14에서 발견되었지만, 원인은 chapter_13 코드에 있습니다.**

#### 오류 메시지
```
FAIL: test_user_signup (users.tests.UserAPITestCase.test_user_signup)
AssertionError: '' != 'test@example.com'
```

#### 발생 상황
```python
def test_user_signup(self):
    response = self.client.post(reverse("user-signup"), self.data)

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # ✅ 통과
    self.assertEqual(User.objects.count(), 1)                        # ✅ 통과
    self.assertEqual(response.data.get("nickname"), "testuser")      # ✅ 통과
    self.assertEqual(response.data.get("email"), "test@example.com") # ❌ 실패
```

유저 생성은 성공했는데 email 값이 빈 문자열로 반환됩니다.

#### 원인 분석

**Step 1: `UserSignupView`가 어떤 serializer를 사용하는가?**
```python
class UserSignupView(CreateAPIView):
    serializer_class = UserDetailSerializer   # ← 이 serializer가 CREATE에 사용됨
```

**Step 2: `UserDetailSerializer`의 Meta 확인**
```python
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "nickname", "email", "password", "profile_image"]
        read_only_fields = ["id", "email"]   # ← email이 read_only!
```

**Step 3: `read_only=True` 필드의 동작**

DRF에서 `read_only=True`인 필드:
1. 클라이언트가 보낸 POST 데이터에서 **무시**됨
2. `validated_data`에 **포함되지 않음**
3. 응답(직렬화)에는 **포함**되지만, 모델 인스턴스의 실제 값을 읽어 반환

```python
# DRF ModelSerializer.create() 기본 동작
def create(self, validated_data):
    # validated_data = {'nickname': 'testuser', 'password': 'testpassword1234'}
    # email이 없음! read_only이므로 제외됨
    instance = ModelClass.objects.create(**validated_data)
    return instance
```

**Step 4: email 없이 User 생성 결과**
```python
User.objects.create(nickname='testuser', password='plaintext')
# EmailField는 빈 문자열('')을 기본값으로 허용
# → user.email = ''
```

**Step 5: 응답에서 email='' 반환**
```python
# 생성된 user.email = ''
# UserDetailSerializer(user).data 직렬화 시
# email 필드는 read_only → user.email 값 그대로 읽음
# response.data['email'] = '' ← '' != 'test@example.com'
```

#### 코드 흐름 전체 요약

```
POST /users/signup/ {"email": "test@example.com", "nickname": "testuser", "password": "..."}
    ↓
UserSignupView.create()
    ↓
UserDetailSerializer(data=request.data).is_valid()
    ↓  email이 read_only_fields에 있으므로 validated_data에서 제외됨
validated_data = {"nickname": "testuser", "password": "testpassword1234"}
    ↓
User.objects.create(**validated_data)  ← email 없이 생성!
    ↓
user.email = ""  (Django EmailField 기본값)
    ↓
UserDetailSerializer(user).data
    ↓
response.data = {"email": "", "nickname": "testuser", ...}
    ↓
AssertionError: "" != "test@example.com"
```

#### 해결 방법 ① — `read_only_fields`에서 email 제거

```python
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "nickname", "email", "password", "profile_image"]
        read_only_fields = ["id"]   # email 제거 ✅
```

`UserDetailSerializer`의 `update()` 메서드는 email을 업데이트하지 않으므로, `read_only_fields`에서 제거해도 PATCH 시 email이 변경되지 않습니다.

#### 해결 방법 ② — 근본 해결: `UserSignupView`에서 `UserSerializer` 사용

더 올바른 해결법은 처음부터 회원가입에는 `UserSerializer`를 사용하는 것입니다:

```python
class UserSignupView(CreateAPIView):
    serializer_class = UserSerializer   # 회원가입 전용 serializer ✅
    permission_classes = [AllowAny]
```

`UserSerializer`는 `read_only_fields`에 email이 없고, `create()` 메서드가 명시적으로 구현되어 있어 회원가입에 적합합니다.

---

### 오류 3: `UserSerializer.create()` — password 처리 문제

#### 코드
```python
class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop("password", None)     # ① password를 꺼냄
        if password is None:
            raise serializers.ValidationError("Password is required.")
        user = User.objects.create_user(**validated_data)   # ② password 없이 create_user 호출
        user.set_password(password)                          # ③ 이후 set_password 호출
        user.save()
        return user
```

#### 발생 가능한 문제

가이드의 `UserManager.create_user` 시그니처:
```python
def create_user(self, email, password, *args, **kwargs):
    ...
```

`password`는 두 번째 **위치 인수**입니다. ②에서 `User.objects.create_user(**validated_data)`를 호출하면:

```python
# validated_data = {"email": "...", "nickname": "..."}  (password가 이미 popped)
User.objects.create_user(email="...", nickname="...")
# ↓
# create_user(self, email, password, *args, **kwargs) 호출 시
# password 인수 없음 → TypeError: create_user() missing 1 required positional argument: 'password'
```

#### 왜 이 오류가 숨겨졌는가?

실제 실행 시 `UserSignupView`는 `UserDetailSerializer`를 사용했고, `UserSerializer`의 `create()`는 호출되지 않았습니다. 따라서 이 코드의 TypeError는 직접 드러나지 않았습니다.

#### 올바른 코드
```python
def create(self, validated_data):
    password = validated_data.pop("password", None)
    if password is None:
        raise serializers.ValidationError("Password is required.")
    # password를 create_user에 명시적으로 전달
    user = User.objects.create_user(password=password, **validated_data)
    return user
```

또는 더 간단하게:
```python
def create(self, validated_data):
    # pop 없이 그냥 전달 (create_user가 내부에서 set_password 처리)
    return User.objects.create_user(**validated_data)
```

---

### 오류 4: Pagination 추가 후 테스트 실패

#### 오류 메시지
```
TypeError: 'ReturnList' object is not subscriptable
# 또는
KeyError: 0
```

#### 발생 상황
`DEFAULT_PAGINATION_CLASS`를 추가하기 전 작성한 테스트 코드:

```python
def test_restaurant_list_view(self):
    response = self.client.get(url)
    self.assertEqual(response.data[0]["name"], "Test Restaurant")   # ❌ 인덱스 직접 접근
```

페이지네이션 설정 후 응답 형태가 변경됩니다:

```json
// 페이지네이션 이전 — 단순 리스트
[{"id": 1, "name": "Test Restaurant"}]

// 페이지네이션 이후 — 딕셔너리로 감싸짐
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [{"id": 1, "name": "Test Restaurant"}]
}
```

`response.data[0]`는 `response.data`가 리스트일 때 동작합니다. 딕셔너리가 되면 `KeyError: 0`이 발생합니다.

#### 해결 방법
```python
def test_restaurant_list_view(self):
    response = self.client.get(url)
    self.assertEqual(len(response.data.get("results")), 1)                        # ✅
    self.assertEqual(response.data.get("results")[0].get("name"), "Test Restaurant")  # ✅
```

---

## 4. 핵심 개념 정리

### DRF Permission 클래스 동작

```python
# IsAuthenticatedOrReadOnly의 실제 동작
class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:   # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_authenticated
```

`SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')` — 데이터를 변경하지 않는 안전한 HTTP 메서드

| 요청 방식 | 인증 필요 | 예시 |
|-----------|-----------|------|
| GET, HEAD, OPTIONS | ❌ | 목록 조회, 상세 조회 |
| POST, PUT, PATCH, DELETE | ✅ | 생성, 수정, 삭제 |

---

### Django Custom User Manager — create_user vs create_superuser

```python
class UserManager(BaseUserManager):
    def create_user(self, email, password, *args, **kwargs):
        # 일반 유저 생성 (is_staff=False, is_superuser=False)
        user = self.model(email=..., *args, **kwargs)
        user.set_password(password)   # 비밀번호 해싱
        user.save()
        return user

    def create_superuser(self, email, password, *args, **kwargs):
        # 슈퍼유저 생성 (is_staff=True, is_superuser=True)
        user = self.create_user(email=email, password=password, *args, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
```

**`set_password(raw_password)`** — 평문 비밀번호를 해시로 변환해 저장합니다.
`User.objects.create(password="plain")` 처럼 직접 필드에 할당하면 해시되지 않은 평문이 저장되므로, **반드시 `set_password()` 또는 `create_user()`를 사용**해야 합니다.

---

### DRF get_object_or_404 vs objects.get()

```python
from rest_framework.generics import get_object_or_404

# ❌ 권장하지 않음: DoesNotExist → 500
review = Review.objects.get(id=pk)

# ✅ 권장: DoesNotExist → Http404 → 404 응답
review = get_object_or_404(Review, id=pk)
```

DRF의 `get_object_or_404`는 `django.shortcuts.get_object_or_404`와 동일하게 동작하지만, DRF의 제네릭 뷰(`GenericAPIView`)와 함께 사용할 때는 DRF 버전을 import하는 것이 일관성이 있습니다.

---

### UserSerializer 설계 패턴 — 역할별 분리

| Serializer | 역할 | 커스텀 메서드 |
|------------|------|--------------|
| `UserSerializer` | 회원가입(CREATE) | `create()` — 비밀번호 해싱 처리 |
| `UserDetailSerializer` | 프로필(GET/PATCH) | `update()` — 닉네임/비밀번호만 수정 가능 |
| `UserLoginSerializer` | 로그인 검증 | `validate()` — `authenticate()` 호출 |

**같은 모델도 역할에 따라 serializer를 분리**하면:
- 각 serializer의 책임이 명확해집니다
- 하나의 serializer에 조건문이 늘어나는 것을 방지합니다
- 테스트가 쉬워집니다

---

### Pagination 설정과 응답 구조 변화

```python
# settings.py
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}
```

이 설정 이후 모든 ListAPIView의 응답 형태가 변경됩니다:

```python
# 테스트 코드 작성 시 반드시 results로 접근
response = self.client.get(url)
results = response.data.get("results")   # 실제 데이터 리스트
count = response.data.get("count")       # 전체 데이터 수
next_url = response.data.get("next")     # 다음 페이지 URL
prev_url = response.data.get("previous") # 이전 페이지 URL
```
