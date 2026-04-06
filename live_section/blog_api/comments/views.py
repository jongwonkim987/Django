from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # 인증 제한 베스트 프랙티스
    filter_backends = [filters.SearchFilter]  # SearchFilter 추가 (content 검색 예시)
    search_fields = ["content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # 생성 시 author 자동 설정 오버라이드
