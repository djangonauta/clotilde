from django import urls

from . import views

app_name = 'automacoes'

urlpatterns = [
    urls.path('seeu/', urls.include('automacoes.seeu.urls')),
    urls.path('verificar/<str:id_automacao>/', views.verificar_automacao, name='verificar_automacao'),
    urls.path('pausar/<str:id_processo>/', views.pausar_processo, name='pausar_processo'),
    urls.path('continuar/<str:id_processo>/', views.continuar_processo, name='continuar_processo'),
    urls.path('cancelar/<str:id_processo>/', views.cancelar_processo, name='cancelar_processo'),
]
