from django.contrib import admin
from .models import GeneralPost, ProblemPost, Like, Comment, ExamplePost
from .forms import PostForm
# Register your models here.


class ProblemPostModelForm(admin.ModelAdmin):
    list_display = ['__str__', 'num_likes', 'author', 'timestamp']
    fields = ('liked', 'author', 'report', 'problem_reported')
    list_display_links = ('__str__', 'author')
    list_filter = ('timestamp',)

    ordering = ('timestamp',)
    search_fields = ('author__user__username',)

    class Meta:
        model = ProblemPost


class GeneralPostModelForm(admin.ModelAdmin):
    list_display = ['__str__', 'num_likes', 'author', 'timestamp']
    exclude = ('liked',)

    class Meta:
        model = GeneralPost


admin.site.register(GeneralPost, GeneralPostModelForm)
admin.site.register(ProblemPost, ProblemPostModelForm)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(ExamplePost)
