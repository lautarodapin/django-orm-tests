from typing import Optional
from django.db import models
from django.db.models import ForeignKey, Model
from django.contrib.auth.models import User
from django.db.models.aggregates import Aggregate, Count, Sum
from django.db.models.deletion import CASCADE
from django.db.models.enums import Choices
from django.db.models.expressions import Case, F, Value, When, Window
from django.db.models.fields import CharField, DateTimeField, FloatField, PositiveSmallIntegerField, SmallIntegerField
from django.db.models.fields.related import ManyToManyField
from django.db.models.functions.datetime import TruncDate
from django.db.models.functions.window import DenseRank
from django.db.models.query import QuerySet

class GroupConcat(Aggregate):
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s)'
    allow_distinct = True
    def __init__(self, expression, distinct=False, **extra):
        super().__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=CharField(),
            **extra)

class WithChoices(Case):
    def __init__(self, choices, field, output_field=CharField(), **extra) -> None:
        whens = [When(**{field: k, 'then': Value(str(v))}) for k, v in dict(choices).items()]
        super().__init__(*whens, output_field=output_field, **extra)


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

class CotizacionQueryset(QuerySet):
    total = Sum(F('productos__precio') * F('productos__cantidad'))
    ranking = Window(expression=DenseRank(), order_by=[F('total').desc()])
    cantidad = Count('id')
    creadores = GroupConcat('creado__username', distinct=True)
    productos = GroupConcat('productos__nombre', distinct=True)
    def ranking_productos(self):
        return (
            self
            .prefetch_related('productos')
            .select_related('creado')
            .values('productos__nombre')
            .annotate(
                cantidad=self.cantidad,
                total=self.total,
                ranking=self.ranking,
                creadores=self.creadores,
            )
            .order_by('ranking')
        )

    def ranking_cotizaciones_por_creadores(self):
        return (
            self
            .prefetch_related('productos')
            .select_related('creado')
            .values('creado__username')
            .annotate(
                cantidad=self.cantidad,
                total=self.total,
                ranking=self.ranking,
                creadores=self.creadores,
                productos=self.productos,
            )
            .order_by('ranking')
        )

    def cotizaciones_por_dia(self):
        return (
            self
            .annotate(date=TruncDate('fake_date'))
            .values('date')
            .annotate(count=self.cantidad)
            .order_by('-date')
        )

class Cotizacion(Model):
    objects = CotizacionQueryset.as_manager()

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
