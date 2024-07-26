from django.urls import path
from . import views

urlpatterns = [
    path('',views.index ,name='index'),
    path('demande_non_traite/',views.non_traite ,name='non_traite'),
    path('demande_traite/',views.traite ,name='traite'),
     path('demande_valide/',views.valide ,name='valide'),
    path('valider_demande/',views.valide_dm ,name='valide_dm'),
    path('demande_<int:id>/',views.dm_details,name='dm_details'),
    path('demande_<int:id>/valide',views.dm_details_valide,name='dm_details_valide'),
    path('pdf_<int:id>/',views.view_credit_request,name='dm_pdf'),
    path('ajax/get_data/<int:id>/', views.get_data, name='get_data'),
    path('ajax/get_valide1/<int:id>/', views.get_valide1, name='get_valide1'),
    path('ajax/get_valide2/<int:id>/', views.get_valide2, name='get_valide2'),
    #path('analyse_<int:id>/',views.analyse,name='analyse')

]
