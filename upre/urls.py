from django.urls import path
from upre.views import inicio,municipos_l,cargar_datos_mun,actualizar_tabla_m,obtener_municipios,obtener_provincias,cargar_datos_upre,proyectos_municipio
urlpatterns = [
    path('', inicio, name='inicio'),
    path('obtener_provincias/', obtener_provincias, name='obtener_provincias'),
    path('obtener_municipios/', obtener_municipios, name='obtener_municipios'),
    path('gam_gaioc/', municipos_l, name='proyect'),
    path('cargar-datamun/', cargar_datos_mun, name='cargar_datos_m'),
    path('cargar-datapre/', cargar_datos_upre, name='cargar_datos_p'),
    path('actualizar_tabla_m/', actualizar_tabla_m, name='actualizar_tabla_m'),
    path('proyectos/departamento/<str:departamento>/municipio/<str:municipio>/', 
     proyectos_municipio, 
     name='proyectos_municipio'),


]