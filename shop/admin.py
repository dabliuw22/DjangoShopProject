from django.contrib import admin

from shop import models

# Register your models here.
@admin.register(models.Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_filter = ('nombre',)

@admin.register(models.Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais',)
    list_filter = ('nombre', 'pais',)

@admin.register(models.Producto)
class Producto(admin.ModelAdmin):
    list_display = ('nombre', 'stock', 'precio', 'descuento',)

@admin.register(models.Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha', 'servida',)

@admin.register(models.DetalleOrden)
class DetalleOrdenAdmin(admin.ModelAdmin):
    list_display = ('orden', 'producto', 'producto', 'cantidad', 'precio', 'valor',)