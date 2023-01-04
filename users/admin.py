from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'photo')
    list_display_links = ('pk', 'user',)
    list_editable = ('photo',)
    search_fields = (
        'user__email',
        'user__username',
        'user__first_name',
        'user__last_name',
    )
    list_filter = (
        'user__is_active',
        'user__is_staff',
        'date_modified',
    )
    fieldsets = (
        ('Profile', {
            'fields': (('user', 'photo', ),),
        }),
        ('Extra info', {
            'fields': (('date_modified'),),
        })
    )
    readonly_fields = ('date_modified',)


class ProfileInline(admin.StackedInline):

    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'


class UserAdmin(BaseUserAdmin):

    inlines = (ProfileInline,)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff'
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)