from django.contrib import admin
from .models import Post, PostsComment
from django.utils.safestring import mark_safe

from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    post = forms.CharField(label="Текст", widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class PostCommentInlines(admin.TabularInline):
    model = PostsComment
    extra = 1
    readonly_fields = ("user", "profile")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "url", "draft")
    list_editable = ("draft",)
    list_filter = ("user",)
    actions = ["publish", "unpublish"]
    inlines = (PostCommentInlines,)
    save_on_top = True
    save_as = True
    readonly_fields = ("get_image",)

    form = PostAdminForm

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image_header.url} width="100" height="100"')

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = "Опубликовать"
    publish.allowed_permission = ('change',)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permission = ('change',)

    get_image.short_description = "Изображение"

    def get_form(self, request, obj=None, **kwargs):
        # self.exclude = ('url',)
        form = super(PostAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        form.base_fields['profile'].initial = request.user.profile
        return form
