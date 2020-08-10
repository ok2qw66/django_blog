from django.contrib import admin

from .models import Post, Comment


# ModelAdmin 상속
class PostAdmin(admin.ModelAdmin):
    # template 화면 상에 뿌려지는 항목을 지정 / count_text : 같은 이름의 함수를 실행
    list_display = ['id', 'title', 'count_text']
    # link 를 걸 위치 지정(지정하지 않으면 처음 항목에 mapping)
    list_display_links = ['title']

    def count_text(self, obj):
        return '{}글자'.format(len(obj.text))
    # 지정안하면 함수 이름대로 나옴.. count text 로 나옴
    count_text.short_description = 'text 글자 수'


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
