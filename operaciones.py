# operaciones.py

from productos import productos
from excepciones import StockInsuficienteError, CantidadInvalidaError

carrito = []
historial_ventas = []

def agregar_al_carrito(nombre, cantidad):
    if not cantidad.isdigit() or int(cantidad) <= 0:
        raise CantidadInvalidaError("Cantidad inválida.")

    cantidad = int(cantidad)
    if productos[nombre]["stock"] < cantidad:
        raise StockInsuficienteError("No hay suficiente stock.")

    total = productos[nombre]["precio"] * cantidad
    carrito.append({"nombre": nombre, "cantidad": cantidad, "precio_total": total})
    productos[nombre]["stock"] -= cantidad

def calcular_total():
    return sum(item["precio_total"] for item in carrito)

def finalizar_compra():
    if not carrito:
        return None
    historial_ventas.extend(carrito)
    resumen = [(item["nombre"], item["cantidad"], item["precio_total"]) for item in carrito]
    carrito.clear()
    return resumen

def calcular_ganancia_total():
    return sum(item["precio_total"] for item in historial_ventas)

def obtener_historial():
    return [(item["nombre"], item["cantidad"], item["precio_total"]) for item in historial_ventas]
