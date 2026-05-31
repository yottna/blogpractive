from rest_framework import serializers
from blog.models import Blog, Comment

# 1. 댓글 전용 시리얼라이저 (⭐500 에러 완벽 해결 버전⭐)
class CommentSerializer(serializers.ModelSerializer):
    blog_id = serializers.IntegerField(source='blog.id', read_only=True)
    
    # 🔴 포스트맨에서 "comment"로 보내면, 모델의 content(또는 comment) 필드에 알아서 쏙 들어가게 매핑합니다.
    # 만약 본인 모델의 댓글 내용 필드명이 'comment'라면 아래 줄을 지우거나 source='comment'로 두시면 됩니다.
    comment = serializers.CharField(source='content', required=False) 

    class Meta:
        model = Comment
        fields = ['id', 'blog_id', 'created_at', 'comment']

    def create(self, validated_data):
        # 만약 모델 필드명이 content인데 validated_data에 comment로 들어온 경우를 대비한 안전장치
        if 'content' not in validated_data and 'comment' in validated_data:
            validated_data['content'] = validated_data.pop('comment')
        
        # 만약 모델 필드명이 comment인 경우 장고가 알아서 처리할 수 있도록 안전하게 처리
        try:
            return Comment.objects.create(**validated_data)
        except TypeError:
            if 'content' in validated_data:
                validated_data['comment'] = validated_data.pop('content')
            return Comment.objects.create(**validated_data)


# 2. 전체 목록 & 글 작성용
class BlogSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(source='date', format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Blog
        fields = ["id", "title", "body", "created_at"]


# 3. 상세 페이지용 (댓글 포함)
class BlogDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(source='date', format="%Y-%m-%d", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ["id", "title", "body", "created_at", "comments"]