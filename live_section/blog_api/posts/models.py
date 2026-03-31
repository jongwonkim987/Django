from django.db import models

from users.models import CustomUser  # 세션 1의 CustomUser 참조


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # 최신순 정렬 베스트 프랙티스
        indexes = [
            models.Index(fields=["author", "created_at"])
        ]  # 쿼리 최적화 인덱스 추가

    def __str__(self):
        return self.title
