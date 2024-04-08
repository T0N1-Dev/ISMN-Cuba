from django.contrib import admin

from App.models import (Editor, Musical_Publication, Especialista, Registered_Data, Rango_Prefijo_Editor,
                        Rango_Prefijo_Publicacion, PrefijoEditor, PrefijoPublicacion, Solicitud)


class EditorInline(admin.StackedInline):
    model = Editor
    verbose_name_plural = "editores"


@admin.register(Editor)
class EditorAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'prefijo']
    search_fields = ['user', 'phone', 'prefijo']
    list_per_page = 8


class EspecialistaInline(admin.StackedInline):
    model = Especialista
    verbose_name_plural = "especialistas"


@admin.register(Especialista)
class EspecialistaAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'directions']
    search_fields = ['user', 'phone', 'directions']
    list_per_page = 8


class Musical_Publication_Admin(admin.ModelAdmin):
    list_display = ['name', 'autor', 'editor', 'ismn', 'imagen', 'gender']
    search_fields = ['name', 'autor', 'editor', 'ismn', 'gender']
    list_per_page = 8


class Prefijo_Editor_Admin(admin.ModelAdmin):
    list_display = ['value', 'lote', 'rango']


class SolicitudAdmin(admin.ModelAdmin):
    list_display = ['editor', 'tipo', 'created_at', 'status']
    search_fields = ['editor', 'tipo', 'created_at', 'status']
    list_per_page = 8


admin.site.register(Registered_Data)
admin.site.register(Musical_Publication, Musical_Publication_Admin)
admin.site.register(Rango_Prefijo_Editor)
admin.site.register(Rango_Prefijo_Publicacion)
admin.site.register(PrefijoEditor, Prefijo_Editor_Admin)
admin.site.register(PrefijoPublicacion)
admin.site.register(Solicitud, SolicitudAdmin)
