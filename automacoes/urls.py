from django import urls

from . import views

app_name = 'automacoes'

urlpatterns = [
    urls.path('teste/', views.automacao_teste, name='automacao_teste'),
    urls.path('verificar/<str:id_automacao>/', views.verificar, name='verificar'),
]
