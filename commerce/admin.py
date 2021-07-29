from django.contrib import admin
from .models import FormaDePago, Producto, Cotizacion, ProductoCotizado, Venta


@admin.register(FormaDePago)
class FormaDePagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'multiplicador', 'valor')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio')


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ('id',)
    raw_id_fields = ('formas_de_pago',)


@admin.register(ProductoCotizado)
class ProductoCotizadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cotizacion', 'precio', 'cantidad', 'nombre')
    list_filter = ('cotizacion',)


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cotizacion', 'forma_de_pago')
    list_filter = ('cotizacion', 'forma_de_pago')