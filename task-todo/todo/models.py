from io import BytesIO
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image as PilImage

User = get_user_model()


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    completed_image = models.ImageField(
        upload_to='todo/completed/',
        null=True,
        blank=True,
    )
    thumbnail = models.ImageField(
        upload_to='todo/thumbnails/',
        null=True,
        blank=True,
        default='defaults/default_thumbnail.png',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.completed_image:
            # 1. Pillow Image 객체 생성
            img = PilImage.open(self.completed_image)

            # 2. thumbnail 메서드로 썸네일 이미지 생성 (300x300 이내)
            img.thumbnail((300, 300))

            # 3. Path 라이브러리로 이미지 경로 가져오기
            image_path = Path(self.completed_image.name)

            # 4. 이름·확장자 가져오고 썸네일 이름·경로 만들기
            stem = image_path.stem
            suffix = image_path.suffix.lower()
            thumb_name = f'{stem}_thumbnail{suffix}'

            # 5. 확장자로 file_type 설정
            if suffix in ['.jpg', '.jpeg']:
                file_type = 'JPEG'
            elif suffix == '.png':
                file_type = 'PNG'
            elif suffix == '.gif':
                file_type = 'GIF'
            elif suffix == '.webp':
                file_type = 'WEBP'
            else:
                file_type = 'JPEG'

            # JPEG는 RGBA 미지원 → RGB 변환
            if file_type == 'JPEG' and img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # 6. BytesIO로 이미지 파일을 bytes 형태로 메모리에 임시 저장
            temp_file = BytesIO()
            img.save(temp_file, format=file_type)
            temp_file.seek(0)

            # 7. 메모리에 저장된 임시파일·file_type으로 이미지 객체 저장 (save=False: 중복 저장 방지)
            self.thumbnail.save(thumb_name, ContentFile(temp_file.read()), save=False)

            # 8. 임시 파일 닫아 메모리 리소스 해제
            temp_file.close()

        # 9. Todo 객체 저장
        super().save(*args, **kwargs)


class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}: {self.message}'
