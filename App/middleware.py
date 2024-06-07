from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import gettext as _


class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return render(request, '404.html', status=404)
        return response


class TranslationMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            content = response.content.decode('utf-8')
            content = content.replace("Easy Audit Application", _("Trazas"))
            content = content.replace("CRUD events", _("Eventos CRUD"))
            content = content.replace("Login events", _("Eventos de Sesiones"))
            content = content.replace("login events", _("Eventos de Sesiones"))
            content = content.replace("Request events", _("Accesos"))
            content = content.replace("request events", _("Registo de Accesos"))
            content = content.replace("Purge", _(""))
            content = content.replace("Can add", _("Puede añadir"))
            content = content.replace("Can change", _("Puede cambiar"))
            content = content.replace("Can delete", _("Puede eliminar"))
            content = content.replace("Can view", _("Puede ver"))
            content = content.replace('/admin/easyaudit/crudevent/purge/', _("/admin/easyaudit/crudevent/"))
            content = content.replace('/admin/easyaudit/loginevent/purge/', _("/admin/easyaudit/loginevent/"))
            content = content.replace('/admin/easyaudit/requestevent/purge/', _("/admin/easyaudit/requestevent/"))
            content = content.replace("Versión de Jazzmin", _(""))
            content = content.replace("3.0.0", _(""))
            content = content.replace("Object repr", _("Objeto"))
            content = content.replace("Content Type", _("Tipo"))
            content = content.replace("Object ID", _("ID"))
            content = content.replace("Please correct the error below", _("Existe un error en el formulario"))
            content = content.replace("No se ha establecido la clave.", _("********"))
            content = content.replace("First, enter a username and password. Then, you'll be able to edit more user options.",
                                      _("Primero, inserte el nombre de usuario y su contraseña. Luego estará listo para editar más opciones de usuario."))
            response.content = content.encode('utf-8')
        return response

