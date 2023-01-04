from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Architect, Archstyle, Category, Building, BuildingImages, BuildingComment, Street


class BuildingAdminForm(forms.ModelForm):
    text = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Building
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


@admin.register(Archstyle)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_display_links = ("name",)


@admin.register(Architect)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "get_image")
    list_display_links = ("name",)
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_display_links = ("name",)


class CommentInlines(admin.TabularInline):
    model = BuildingComment
    extra = 1
    readonly_fields = ("user", "profile")


class BuildingImagesInline(admin.TabularInline):
    model = BuildingImages
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="100"')

    get_image.short_description = "Изображение"


@admin.register(Building)
class BuildingAdmin (admin.ModelAdmin):
    list_display = ("title", "url", "draft")
    list_filter = ("category",)
    search_fields = ("title", "category__name")
    inlines = (CommentInlines, BuildingImagesInline)
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    form = BuildingAdminForm
    actions = ["publish", "unpublish"]
    readonly_fields = ("get_image",)

    fieldsets = (
        (None, {
            "fields": (("title", "year", "url", "draft"),)
        }),
        (None, {
            "fields": ("text", ("image", "get_image"))
        }),
        (None, {
            "fields": (("street", "housenumber", "letter"),)
        }),
        (None, {
            "fields": (("architect", "archstyle", "category"),)
        }),
        (None, {
            "fields": (("lat", "lag"),)
        }),

    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="100"')

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


admin.site.site_title = 'Админ-панель'
admin.site.site_header = 'Админ-панель'
