from rest_framework import serializers

from comments.serializers import CommentSerializer  # CommentSerializer 임포트

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(
        many=True, read_only=True
    )  # nested serializers 베스트 프랙티스

    class Meta:
        model = Post
        fields = "__all__"  # 모든 필드 포함, 필요 시 명시적 지정 추천
        read_only_fields = [
            "author",
            "created_at",
            "updated_at",
        ]  # 읽기 전용 필드 설정

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("제목은 5자 이상이어야 합니다.")
        return value  # 추가 validation 베스트 프랙티스
