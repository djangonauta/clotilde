from django import urls

from . import views

app_name = 'automacoes'

urlpatterns = [
    urls.path('iniciar/', views.iniciar, name='iniciar'),
    urls.path('verificar/<str:id_automacao>/', views.verificar, name='verificar'),
    urls.path('cancelar/<str:id_processo>/', views.cancelar, name='cancelar'),
    urls.path('pausar/<str:id_processo>/', views.pausar, name='pausar'),
    urls.path('continuar/<str:id_processo>/', views.continuar, name='continuar'),
]
