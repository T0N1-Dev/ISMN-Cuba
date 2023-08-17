from django.contrib import admin
from App.models import Editor, Musical_Publication, Registered_Data

class EditorAdmin(admin.ModelAdmin):
    list_display = ['name','phone','email','gender','created_at']
    search_fields = ['name', 'phone', 'email', 'gender']
    list_per_page = 8

class Musical_Publication_Admin(admin.ModelAdmin):
    list_display = ['name','autor','ismn','imagen','gender']
    search_fields = ['name', 'autor', 'ismn', 'gender']
    list_per_page = 8

admin.site.register(Registered_Data)
admin.site.register(Editor, EditorAdmin)
admin.site.register(Musical_Publication, Musical_Publication_Admin)

