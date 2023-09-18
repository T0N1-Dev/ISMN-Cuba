from django.contrib import admin
from App.models import Editor, Musical_Publication, Registered_Data, Especialista, \
    Musical_Publication_Prefijo, Editor_Prefijo
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class EditorPrefijoInline(admin.StackedInline):
    model = Editor_Prefijo
    verbose_name_plural = "prefijos_editores"


class EditorInline(admin.StackedInline):
    model = Editor
    verbose_name_plural = "editores"


class EspecialistaInline(admin.StackedInline):
    model = Especialista
    verbose_name_plural = "especialistas"


class UserAdmin(BaseUserAdmin):
    inlines = [EditorInline, EspecialistaInline]


class EditorAdmin(admin.ModelAdmin):
    inlines = [EditorPrefijoInline]


class MusicalPublicationInline(admin.StackedInline):
    model = Musical_Publication_Prefijo
    verbose_name_plural = "prefijos_publicaciones"


class Musical_Publication_Admin(admin.ModelAdmin):
    list_display = ['name', 'autor', 'ismn', 'imagen', 'gender']
    search_fields = ['name', 'autor', 'ismn', 'gender']
    list_per_page = 8
    inlines = [MusicalPublicationInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Registered_Data)
admin.site.register(Editor, EditorAdmin)
admin.site.register(Especialista)
admin.site.register(Musical_Publication, Musical_Publication_Admin)

