import tkinter as tk
from tkinter import ttk, messagebox
from productos import productos
from operaciones import agregar_al_carrito, calcular_total, finalizar_compra, obtener_historial, calcular_ganancia_total, carrito
from excepciones import StockInsuficienteError, CantidadInvalidaError

root = tk.Tk()
root.title("Fruber - Caja Registradora")
root.geometry("1024x600")
root.minsize(900, 550)
root.configure(bg="#f5f5f5")

# --- Config responsive ---
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# --- Panel de Productos (izquierda) ---
frame_izq = tk.Frame(root, bg="#e3f2fd", width=280)
frame_izq.grid(row=0, column=0, sticky="ns")

label_productos = tk.Label(frame_izq, text="Productos", bg="#e3f2fd", font=("Arial", 16, "bold"))
label_productos.pack(pady=10)

entry_cantidad = tk.Entry(frame_izq, justify="center", font=("Arial", 12))
entry_cantidad.insert(0, "1")
entry_cantidad.pack(pady=5)

botones_producto = []

def crear_botones():
    for btn in botones_producto:
        btn.destroy()
    botones_producto.clear()
    for nombre in productos:
        texto = f"{nombre}\n${productos[nombre]['precio']} ({productos[nombre]['stock']})"
        btn = tk.Button(frame_izq, text=texto, width=22, height=2,
                        bg="#bbdefb", font=("Arial", 10),
                        command=lambda n=nombre: agregar_producto(n))
        btn.pack(pady=3)
        botones_producto.append(btn)

def agregar_producto(nombre):
    try:
        cantidad = entry_cantidad.get()
        agregar_al_carrito(nombre, cantidad)
        actualizar_ticket()
        entry_cantidad.delete(0, tk.END)
        entry_cantidad.insert(0, "1")
        crear_botones()
    except (StockInsuficienteError, CantidadInvalidaError) as e:
        messagebox.showerror("Error", str(e))

crear_botones()

# --- Panel de Ticket (centro) ---
frame_ticket = tk.Frame(root, bg="#ffffff")
frame_ticket.grid(row=0, column=1, sticky="nsew")
frame_ticket.grid_rowconfigure(1, weight=1)
frame_ticket.grid_columnconfigure(0, weight=1)

label_ticket = tk.Label(frame_ticket, text="Resumen de Compra", font=("Arial", 16), bg="#ffffff")
label_ticket.grid(row=0, column=0, pady=10)

tree = ttk.Treeview(frame_ticket, columns=("Producto", "Cantidad", "Subtotal"), show="headings")
tree.heading("Producto", text="Producto")
tree.heading("Cantidad", text="Cantidad")
tree.heading("Subtotal", text="Subtotal")
tree.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

# --- Panel de pagos y descuentos ---
frame_pago = tk.Frame(frame_ticket, bg="#f9f9f9")
frame_pago.grid(row=2, column=0, sticky="ew", padx=20, pady=5)

label_total = tk.Label(frame_pago, text="Total: $0.00", font=("Arial", 14), bg="#f9f9f9")
label_total.grid(row=0, column=0, sticky="w")

# Descuento
tk.Label(frame_pago, text="Cupón / % Desc:", bg="#f9f9f9").grid(row=1, column=0, sticky="e")
entry_descuento = tk.Entry(frame_pago, width=10)
entry_descuento.grid(row=1, column=1, padx=5)

# Método de pago
tk.Label(frame_pago, text="Método Pago:", bg="#f9f9f9").grid(row=2, column=0, sticky="e")
combo_pago = ttk.Combobox(frame_pago, values=["Efectivo", "Tarjeta", "Transferencia"])
combo_pago.set("Efectivo")
combo_pago.grid(row=2, column=1, padx=5)

# Pagó con
tk.Label(frame_pago, text="Pagó con:", bg="#f9f9f9").grid(row=3, column=0, sticky="e")
entry_pagocon = tk.Entry(frame_pago, width=10)
entry_pagocon.grid(row=3, column=1, padx=5)

label_cambio = tk.Label(frame_pago, text="Cambio: $0.00", font=("Arial", 12), bg="#f9f9f9")
label_cambio.grid(row=4, column=0, columnspan=2, pady=5)

def actualizar_ticket():
    for item in tree.get_children():
        tree.delete(item)
    for item in carrito:
        tree.insert("", "end", values=(item["nombre"], item["cantidad"], f"${item["precio_total"]:.2f}"))
    total = calcular_total()
    label_total.config(text=f"Total: ${total:.2f}")

# --- Panel de Funciones (derecha) ---
frame_funciones = tk.Frame(root, bg="#eeeeee", width=200)
frame_funciones.grid(row=0, column=2, sticky="ns")

frame_funciones.grid_propagate(False)
label_func = tk.Label(frame_funciones, text="Acciones", font=("Arial", 16), bg="#eeeeee")
label_func.pack(pady=15)

def finalizar():
    try:
        total = calcular_total()
        desc = entry_descuento.get()
        if desc:
            if desc.endswith('%'):
                porcentaje = float(desc.strip('%')) / 100
                total -= total * porcentaje
            else:
                total -= float(desc)

        pago = float(entry_pagocon.get()) if entry_pagocon.get() else 0.0
        cambio = pago - total

        if cambio < 0:
            messagebox.showwarning("Pago insuficiente", "El monto pagado no cubre el total.")
            return

        resumen = finalizar_compra()
        if resumen:
            texto = "\n".join([f"{r[0]} x{r[1]} - ${r[2]:.2f}" for r in resumen])
            texto += f"\n\nDescuento aplicado: {desc or 'Ninguno'}"
            texto += f"\nMétodo de pago: {combo_pago.get()}"
            texto += f"\nPagó con: ${pago:.2f}"
            texto += f"\nCambio: ${cambio:.2f}"
            label_cambio.config(text=f"Cambio: ${cambio:.2f}")
            messagebox.showinfo("Compra Finalizada", f"Resumen:\n{texto}")
            actualizar_ticket()
            crear_botones()
            entry_descuento.delete(0, tk.END)
            entry_pagocon.delete(0, tk.END)
        else:
            messagebox.showwarning("Vacío", "No hay productos en el carrito.")
    except ValueError:
        messagebox.showerror("Error", "Verifica los campos de descuento o pago.")

def ver_historial():
    historial = obtener_historial()
    ganancia = calcular_ganancia_total()
    win = tk.Toplevel(root)
    win.title("Historial de Ventas")

    tree_hist = ttk.Treeview(win, columns=("Producto", "Cantidad", "Subtotal"), show="headings")
    tree_hist.heading("Producto", text="Producto")
    tree_hist.heading("Cantidad", text="Cantidad")
    tree_hist.heading("Subtotal", text="Subtotal")
    tree_hist.pack(padx=10, pady=10, fill="both", expand=True)

    for item in historial:
        tree_hist.insert("", "end", values=(item[0], item[1], f"${item[2]:.2f}"))

    tk.Label(win, text=f"Ganancia Total: ${ganancia:.2f}", font=("Arial", 12)).pack(pady=10)

tk.Button(frame_funciones, text="Finalizar Compra", command=finalizar, bg="#4caf50", fg="white",
          font=("Arial", 12), width=18, height=2).pack(pady=10)

tk.Button(frame_funciones, text="Ver Historial", command=ver_historial, bg="#2196f3", fg="white",
          font=("Arial", 12), width=18, height=2).pack(pady=10)

root.mainloop()