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
            content = content.replace("Purge", _("Eliminar"))
            content = content.replace("Can add", _("Puede añadir"))
            content = content.replace("Can change", _("Puede cambiar"))
            content = content.replace("Can delete", _("Puede eliminar"))
            content = content.replace("Can view", _("Puede ver"))
            response.content = content.encode('utf-8')
        return response

