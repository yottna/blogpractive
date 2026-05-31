from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Blog, Comment
from .serializers import BlogSerializer, BlogDetailSerializer, CommentSerializer

# 1. [GET] 전체 게시글 목록 조회 & [POST] 게시글 생성
class BlogListView(APIView):
    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. [GET] 상세조회 & [PATCH] 수정 & [DELETE] 삭제 (⭐여기에 기능 추가!⭐)
class BlogDetailView(APIView):
    def get_object(self, blog_id):
        try:
            return Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return None

    # [GET] 상세조회
    def get(self, request, blog_id):
        blog = self.get_object(blog_id)
        if blog is None:
            return Response({"detail": "해당 게시글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        serializer = BlogDetailSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # [PATCH] 게시글 수정
    def patch(self, request, blog_id):
        blog = self.get_object(blog_id)
        if blog is None:
            return Response({"detail": "해당 게시글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        # partial=True를 줘야 일부 필드(예: title만)만 넘겨도 수정이 잘 됩니다!
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # [DELETE] 게시글 삭제
    def delete(self, request, blog_id):
        blog = self.get_object(blog_id)
        if blog is None:
            return Response({"detail": "해당 게시글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 3. [GET] 댓글 목록 조회 & [POST] 댓글 작성
class CommentListView(APIView):
    def get(self, request, blog_id):
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response({"detail": "해당 게시글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            
        comments = Comment.objects.filter(blog=blog)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, blog_id):
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return Response({"detail": "해당 게시글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(blog=blog)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)