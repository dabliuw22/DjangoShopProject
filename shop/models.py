from decimal import Decimal

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pais(models.Model):
    nombre = models.CharField(max_length = 50)

    def __str__(self):
        return "{}".format(self.nombre)

class Ciudad(models.Model):
    nombre = models.CharField(max_length = 50)
    pais = models.ForeignKey(Pais, on_delete = models.CASCADE)

    def __str__(self):
        return "{}".format(self.nombre)

class Producto(models.Model):
    nombre = models.CharField(max_length = 50)
    stock = models.PositiveIntegerField(default = 0)
    imagen = models.ImageField(upload_to = 'img', null = True, blank = True)
    precio = models.DecimalField(max_digits = 10, decimal_places = 1)
    descuento = models.DecimalField(max_digits = 2, decimal_places = 1)

    def __str__(self):
        return "{}".format(self.nombre)

    def get_precio(self):
        return Decimal(self.precio*(1-self.descuento))

class Orden(models.Model):
    usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    fecha = models.DateTimeField(auto_now_add = True)
    productos = models.ManyToManyField(Producto, through = 'DetalleOrden')
    ciudad = models.ForeignKey(Ciudad, on_delete = models.CASCADE)
    direccion = models.CharField(max_length = 100)
    servida = models.BooleanField(default = False)

    def get_total(self):
        #return DetalleOrden.objects.filter(orden = self).aggregate(total = models.Sum('valor'))
        return Decimal(sum(detalle.get_valor() for detalle in self.detalles.all()))

    def get_detalles_orden(self):
        return self.detalles.all()

    def save(self, *args, **kwargs):
        self.fecha = timezone.now()
        super(Orden, self).save(*args, **kwargs)

    def __str__(self):
        return 'Orden {}'.format(self.usuario.id)

class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete = models.CASCADE, related_name = 'detalles')
    producto = models.ForeignKey(Producto, on_delete = models.CASCADE)
    cantidad = models.PositiveIntegerField(default = 1)
    descuento = models.FloatField(default = 0.0)
    precio = models.DecimalField(default = 0, max_digits = 10, decimal_places = 2)
    valor = models.DecimalField(default = 0, max_digits = 20, decimal_places = 2)

    def get_valor(self):
        return self.precio*self.cantidad

    def save(self, *args, **kwargs):
        self.descuento = self.producto.descuento
        self.precio = self.producto.precio*(1-self.descuento)
        self.valor = self.get_valor()
        super(DetalleOrden, self).save(*args, **kwargs)