from django.contrib import admin
from App.models import Editor, Musical_Publication, Registered_Data, Especialista
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class EditorInline(admin.StackedInline):
    model = Editor
    verbose_name_plural = "editores"


class UserAdmin(BaseUserAdmin):
    inlines = [EditorInline]


class Musical_Publication_Admin(admin.ModelAdmin):
    list_display = ['name', 'autor', 'ismn', 'imagen', 'gender']
    search_fields = ['name', 'autor', 'ismn', 'gender']
    list_per_page = 8


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Registered_Data)
admin.site.register(Editor)
admin.site.register(Especialista)
admin.site.register(Musical_Publication, Musical_Publication_Admin)

