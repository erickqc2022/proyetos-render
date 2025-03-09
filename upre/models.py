from django.db import models

# Create your models here.
class Municipio(models.Model):
    departamento=models.CharField(max_length=20)
    provin = models.CharField(max_length=25)
    muni= models.CharField(max_length=50)
    alcalde=models.CharField(max_length=30)
    sigla=models.CharField(max_length=15)
    celular=models.CharField(max_length=20)
    linea=models.CharField(max_length=2)
    e2016=models.CharField(max_length=10)
    e2019=models.CharField(max_length=10)
    e2020=models.CharField(max_length=10)

class Upre_proy(models.Model):
    depto = models.CharField(max_length=20)
    mun = models.CharField(max_length=55)
    nombre_p= models.CharField(max_length=300)
    estado=models.CharField(max_length=50)
    remitente= models.CharField(max_length=400)
    beneficiario=models.CharField(max_length=150)
    monto_p = models.DecimalField(max_digits=12, decimal_places=2)

class Proyecto(models.Model):
    id_proy= models.CharField(max_length=5)
    depto= models.CharField(max_length=20)
    provin = models.CharField(max_length=20)
    muni= models.CharField(max_length=20)
    entidad_resp = models.CharField(max_length=100)
    entidad_financiera = models.CharField(max_length=100)
    entidad_ejec = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    proyecto = models.CharField(max_length=300)
    estado = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=12, decimal_places=2)