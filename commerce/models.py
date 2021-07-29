from django.db import models
from django.db.models import ForeignKey, Model
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.enums import Choices
from django.db.models.fields import CharField, DateTimeField, FloatField, PositiveSmallIntegerField, SmallIntegerField
from django.db.models.fields.related import ManyToManyField


class FormaDePago(Model):
    class Multiplicador(Choices):
        positivo = 1
        negativo = -1

    multiplicador = SmallIntegerField(choices=Multiplicador.choices, default=Multiplicador.positivo)
    valor = FloatField()

    class Meta:
        unique_together = ['multiplicador', 'valor']

class Producto(Model):
    nombre = CharField(max_length=255)
    precio = FloatField()

    def __str__(self) -> str:
        return self.nombre

class Cotizacion(Model):
    fake_date = DateTimeField()
    creado = ForeignKey(User, CASCADE, related_name='cotizaciones')
    para = ForeignKey(User, CASCADE, related_name='cotizaciones_recibidas')
    formas_de_pago = ManyToManyField(FormaDePago, related_name='cotizaciones')


class ProductoCotizado(Model):
    cotizacion = ForeignKey(Cotizacion, CASCADE, related_name='productos')
    precio = FloatField()
    cantidad = PositiveSmallIntegerField()
    nombre = CharField(max_length=255)

    def __str__(self) -> str:
        return self.nombre

class Venta(Model):
    fake_date = DateTimeField()
    creado = ForeignKey(User, CASCADE, related_name='ventas')
    para = ForeignKey(User, CASCADE, related_name='ventas_recibidas')
    cotizacion = ForeignKey(Cotizacion, CASCADE, related_name='ventas')
    forma_de_pago = ForeignKey(FormaDePago, CASCADE, related_name='+')
