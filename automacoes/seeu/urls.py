from django import urls

from . import views

app_name = 'seeu'

urlpatterns = [
    urls.path('intimar-pessoalmente-a-partir-despacho/',
              views.intimar_pessoalmente_a_partir_despacho,
              name='intimar_pessoalmente_a_partir_despacho'),
]
