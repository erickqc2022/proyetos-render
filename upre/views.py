
import csv
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Municipio,Upre_proy
from decimal import Decimal, InvalidOperation
from django.db import DataError
from django.http import JsonResponse
from django.db.models import Q
# Create your views here.

@csrf_exempt
def cargar_datos_mun(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'El archivo debe ser CSV')
            return render(request, 'principal/cargar.html')

        try:
            file_data = csv_file.read().decode('utf-8-sig')
            lines = file_data.splitlines()
            reader = csv.DictReader(lines, delimiter=';')
            
            for row in reader:
                try:
                    # Limpiar espacios en blanco y truncar campos si es necesario
                    row = {k.strip(): v.strip() for k, v in row.items() if k is not None}
                    
                    # Truncar campos si es necesario
                    departamento = row.get('DEPARTAMENTO', '')[:20]
                    provincia = row.get('PROVINCIA', '')[:20]
                    municipio = row.get('MUNICIPIO', '')[:50]
                    alcalde = row.get('ALCALDE', '')[:30]
                    sigla = row.get('SIGLA', '')[:15]
                    celular = row.get('CELULAR', '')[:20]
                    linea = row.get('LINEA', '')[:2]
                    e2016 = row.get('ELECCIONES2016', '')[:10]
                    e2019 = row.get('ELECCIONES2019', '')[:10]
                    e2020 = row.get('ELECCIONES2020', '')[:10]
                    
                    # Crear el registro en la base de datos
                    Municipio.objects.create(
                        departamento=departamento,
                        provin = provincia,
                        muni= municipio,
                        alcalde=alcalde,
                        sigla=sigla,
                        celular=celular,
                        linea=linea,
                        e2016=e2016,
                        e2019=e2019,
                        e2020=e2020,
                    )
                except KeyError as e:
                    messages.warning(request, f'Columna faltante en la fila: {e}')
                except DataError as e:
                    messages.warning(request, f'Error de datos: {str(e)}. Fila: {row}')
                except Exception as e:
                    messages.warning(request, f'Error al procesar fila: {row}. Error: {str(e)}')

            messages.success(request, 'Archivo CSV cargado exitosamente')
        except Exception as e:
            messages.error(request, f'Error al procesar el archivo: {str(e)}')

    return render(request, 'cargado_municipios.html')


@csrf_exempt
def cargar_datos_upre(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'El archivo debe ser CSV')
            return render(request, 'cargado_pupre.html')

        try:
            file_data = csv_file.read().decode('utf-8-sig')
            lines = file_data.splitlines()
            reader = csv.DictReader(lines, delimiter=';')
            
            for row in reader:
                try:
                    # Limpiar espacios en blanco y truncar campos si es necesario
                    row = {k.strip(): v.strip() for k, v in row.items() if k is not None}
                    
                    # Verificar y convertir el monto correctamente
                    monto_str = row.get('MONTO', '').replace('.', '').replace(',', '.')
                    if monto_str:  # Si hay un valor en el monto
                        try:
                            monto = Decimal(monto_str)
                        except InvalidOperation:
                            monto = Decimal('0')
                    else:
                        monto = Decimal('0')  # Si el campo de monto está vacío, usar 0
                    
                    # Truncar campos si es necesario
                    departamento = row.get('DEPARTAMENTO', '')[:20]
                    municipio = row.get('MUNICIPIO', '')[:55]
                    proyecto = row.get('PROYECTO', '')[:200]
                    remitente = row.get('REMITENTE', '')[:200]
                    beneficiario = row.get('BENEFICIARIO', '')[:100]
                    estado = row.get('ESTADO', '')[:50]
                    
                    # Crear el registro en la base de datos
                    Upre_proy.objects.create(
                        depto=departamento,
                        mun=municipio,
                        nombre_p=proyecto,
                        estado=estado,
                        remitente=remitente,
                        beneficiario=beneficiario,
                        monto_p=monto
                    )
                except KeyError as e:
                    messages.warning(request, f'Columna faltante en la fila: {e}')
                except DataError as e:
                    messages.warning(request, f'Error de datos: {str(e)}. Fila: {row}')
                except Exception as e:
                    messages.warning(request, f'Error al procesar fila: {row}. Error: {str(e)}')

            messages.success(request, 'Archivo CSV cargado exitosamente')
        except Exception as e:
            messages.error(request, f'Error al procesar el archivo: {str(e)}')

    return render(request, 'cargado_pupre.html')

def inicio(request):
    
    return render(request, 'principal.html')

def municipos_l(request):
    # Obtener todos los departamentos distintos
    departamentos = Municipio.objects.values_list('departamento', flat=True).distinct()
    # Obtener todos los proyectos inicialmente (o aplicar algún filtro por defecto si es necesario)
    municipios = Municipio.objects.all() 

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Solicitud AJAX para filtros en cascada
        tipo_filtro = request.POST.get('tipo')
        valor_filtro = request.POST.get('valor')

        if tipo_filtro == 'departamento':
            provincias = Municipio.objects.filter(departamento=valor_filtro).values_list('provin', flat=True).distinct()
            return JsonResponse({'provincias': list(provincias)})
        elif tipo_filtro == 'provincia':
            municipios = Municipio.objects.filter(provincia=valor_filtro).values_list('muni', flat=True).distinct()
            return JsonResponse({'municipios': list(municipios)})

    context = {
        'departamentos': departamentos,
        'municipios': municipios,  
    }
    return render(request, 'listado_m.html', context)

def obtener_provincias(request):
    departamento = request.GET.get('departamento')
    
    # Verifica que el departamento no esté vacío
    if departamento:
        provincias = Municipio.objects.filter(departamento=departamento).values_list('provin', flat=True).distinct().order_by('provin')
        return JsonResponse({'provincias': list(provincias)})
    else:
        return JsonResponse({'provincias': []})

def obtener_municipios(request):
    provincia = request.GET.get('provincia')
    departamento = request.GET.get('departamento')  # Añadir el parámetro de departamento
    
    # Verifica que la provincia y el departamento no estén vacíos
    if provincia and departamento:
        municipios = Municipio.objects.filter(
            provin=provincia,
            departamento=departamento  # Añadir filtro por departamento
        ).values_list('muni', flat=True).distinct().order_by('muni')
        return JsonResponse({'municipios': list(municipios)})
    else:
        return JsonResponse({'municipios': []})

def actualizar_tabla_m(request):
    departamento = request.GET.get('departamento')
    provincia = request.GET.get('provincia')
    municipio = request.GET.get('municipio')
    busqueda = request.GET.get('busqueda')

    municipios = Municipio.objects.all()

    if departamento:
        municipios = municipios.filter(departamento=departamento)
    if provincia:
        municipios = municipios.filter(provin=provincia)
    if municipio:
        municipios = municipios.filter(muni=municipio)
    
    if busqueda:
        municipios = municipios.filter(
            Q(muni__icontains=busqueda) 
        )

    # Agrupar y enumerar proyectos por municipio
    

    return render(request, 'tabla_m.html', {'municipios': municipios})

def proyectos_municipio(request, departamento, municipio):
    import unicodedata
    from difflib import SequenceMatcher
    
    def normalize_text(text):
        text = str(text)
        normalized = unicodedata.normalize('NFD', text)
        normalized = ''.join([c for c in normalized if not unicodedata.combining(c)])
        return normalized.lower()
    
    def similarity_ratio(a, b):
        return SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()
    
    # Primero intentar coincidencia exacta
    proyectos = Upre_proy.objects.filter(depto=departamento, mun=municipio)
    
    # Si no hay resultados, buscar por similitud
    if not proyectos.exists():
        # Obtener todos los proyectos del departamento
        departamento_proyectos = Upre_proy.objects.filter(depto__iexact=departamento)
        
        # Lista para almacenar proyectos coincidentes
        proyectos_list = []
        
        # Buscar municipios similares (umbral de similitud 0.8 = 80%)
        similarity_threshold = 0.8
        municipio_norm = normalize_text(municipio)
        
        for p in departamento_proyectos:
            # Calcular ratio de similitud
            similarity = similarity_ratio(p.mun, municipio)
            
            # Si supera el umbral, considerar coincidencia
            if similarity >= similarity_threshold:
                proyectos_list.append(p)
        
        # Si encontramos coincidencias por similitud
        if proyectos_list:
            proyectos = proyectos_list
    
    info_municipio = {
        'departamento': departamento,
        'muni': municipio
    }
    
    return render(request, 'listado_u.html', {
        'info_municipio': info_municipio,
        'proyectos': proyectos
    })