from commerce.models import *
import random

def run():
    User.objects.filter(is_superuser=False).delete()
    FormaDePago.objects.all().delete()
    Producto.objects.all().delete()
    Cotizacion.objects.all().delete()
    Venta.objects.all().delete()
    ProductoCotizado.objects.all().delete()

    users = [User.objects.get(username='lautaro')]

    for i in range(random.randint(5, 10)):
        users.append(User.objects.create_user(
            username=f'usuario {i}',
            password='password',
        ))

    formas_de_pago = []
    for i in range(10):
        forma_de_pago = FormaDePago.objects.create(
            valor=random.random() * 20,
            multiplicador=random.choice([FormaDePago.Multiplicador.positivo.value, FormaDePago.Multiplicador.negativo.value]),
        )
        formas_de_pago.append(forma_de_pago)

    productos = []
    for i in range(random.randint(10, 20)):
        producto = Producto.objects.create(
            nombre=f'Producto {i}',
            precio=random.random() * 100 + 1,
        )
        productos.append(producto)

    cotizaciones = []
    for i in range(random.randint(5, 10)):
        creado = random.choice(users)
        para = random.choice(list(filter(lambda user: user.id != creado.id, users)))
        cotizacion = Cotizacion.objects.create(creado=creado, para=para)
        [cotizacion.formas_de_pago.add(forma) for forma in random.choices(formas_de_pago)]
        cotizacion.save()
        cotizaciones.append(cotizacion)
    
    for cotizacion in cotizaciones:
        for i in range(random.randint(5, 10)):
            producto = random.choice(productos)
            producto_cotizado = ProductoCotizado.objects.create(
                cotizacion=cotizacion,
                precio=producto.precio,
                cantidad=random.randint(1, 5),
                nombre=producto.nombre,
            )
            
        creado = random.choice(users)
        para = random.choice(list(filter(lambda user: user.id != creado.id, users)))
        venta = Venta.objects.create(
            creado=creado,
            para=para,
            cotizacion=cotizacion,
            forma_de_pago=random.choice(formas_de_pago),
        )

if __name__ == '__main__':
    run()