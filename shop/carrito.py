from django.conf import settings
from decimal import Decimal

from shop.models import Producto

class Carrito(object):

    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get(settings.CARRITO_SESSION_ID)
        if not carrito:
            carrito = self.session[settings.CARRITO_SESSION_ID] = {}
        self.carrito = carrito

    def save(self):
        self.session[settings.CARRITO_SESSION_ID] = self.carrito
        self.session.modified = True

    def add(self, producto, cantidad = 1, update_cantidad = False):
        producto_id = str(producto.id)
        if producto_id not in self.carrito:
            self.carrito[producto_id] = {'cantidad': 0, 'precio': (str(producto.get_precio()))}
        if update_cantidad:
            self.carrito[producto_id]['cantidad'] = cantidad
        else:
            self.carrito[producto_id]['cantidad'] += cantidad
        self.save()

    def remove(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.save()

    def clear(self):
        self.session[settings.CARRITO_SESSION_ID] = {}
        self.session.modified = True

    def contains(self, producto):
        for id in self.carrito.keys():
            if producto.id == producto:
                return True
        return False

    def __iter__(self):
        productos_id = self.carrito.keys()
        productos = Producto.objects.filter(id__in = productos_id)
        for producto in productos:
            self.carrito[str(producto.id)]['producto'] = producto

        for item in self.carrito.values():
            item['valor'] = str(Decimal(item['precio'])*item['cantidad'])
            yield item

    def __len__(self):
        return sum(item['cantidad'] for item in self.carrito.values())

    def get_total(self):
        return sum(Decimal(item['precio'])*item['cantidad'] for item in self.carrito.values())