from django.contrib import admin
from App.models import CustomUser, Editor, Musical_Publication, Registered_Data


class UserAdminConfig(admin.ModelAdmin):
    list_display = ['email', 'user_name', 'first_name', 'phone', 'is_staff', 'is_active']
    search_fields = ['email', 'user_name', 'first_name', 'phone']
    list_per_page = 8


class EditorAdmin(admin.ModelAdmin):
    list_display = ['gender', 'created_at']
    search_fields = ['gender']
    list_per_page = 8


class Musical_Publication_Admin(admin.ModelAdmin):
    list_display = ['name', 'autor', 'ismn', 'imagen', 'gender']
    search_fields = ['name', 'autor', 'ismn', 'gender']
    list_per_page = 8


admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(Registered_Data)
admin.site.register(Editor, EditorAdmin)
admin.site.register(Musical_Publication, Musical_Publication_Admin)

