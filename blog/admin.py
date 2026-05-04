from django.contrib import admin
from .models import Blog # 같은 폴더(.) 내에 있는 models모듈에서 Blog를 import해오겠다는 의미입니다. 

class BlogAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(Blog, BlogAdmin)
# Register your models here.
