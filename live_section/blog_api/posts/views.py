from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # 인증 제한 베스트 프랙티스

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # 생성 시 author 자동 설정 오버라이드
