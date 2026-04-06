from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"  # 모든 필드 포함, 필요 시 명시적 지정 추천
        read_only_fields = ["author", "created_at", "updated_at"]  # 읽기 전용 필드 설정

    def validate_content(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("댓글 내용은 10자 이상이어야 합니다.")
        return value  # 추가 validation 베스트 프랙티스
