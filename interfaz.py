import tkinter as tk
from tkinter import ttk

# --- Ventana principal ---
root = tk.Tk()
root.title("Caja Registradora")
root.geometry("900x500")
root.configure(bg="#f0f0f0")

# --- Panel izquierdo: Categorías / Productos ---
frame_productos = tk.Frame(root, bg="#e0e0e0", width=200)
frame_productos.pack(side="left", fill="y")

productos = ["Café", "Pan", "Refresco", "Sándwich", "Galleta"]

for p in productos:
    btn = tk.Button(frame_productos, text=p, width=20, height=2, bg="#d1ecf1", fg="#333")
    btn.pack(padx=10, pady=5)

# --- Panel central: Ticket de compra ---
frame_ticket = tk.Frame(root, bg="#ffffff", width=400)
frame_ticket.pack(side="left", fill="both", expand=True)

label_ticket = tk.Label(frame_ticket, text="Ticket de Compra", font=("Arial", 14), bg="#ffffff")
label_ticket.pack(pady=10)

tree = ttk.Treeview(frame_ticket, columns=("Producto", "Precio"), show="headings")
tree.heading("Producto", text="Producto")
tree.heading("Precio", text="Precio")
tree.pack(padx=20, pady=10, fill="both", expand=True)

label_total = tk.Label(frame_ticket, text="Total: $0.00", font=("Arial", 12), bg="#ffffff")
label_total.pack(pady=10)

# --- Panel derecho: Funciones / Teclado ---
frame_funciones = tk.Frame(root, bg="#f9f9f9", width=200)
frame_funciones.pack(side="right", fill="y")

funciones = ["Cobrar", "Cancelar", "Eliminar", "Nuevo"]

for f in funciones:
    btn = tk.Button(frame_funciones, text=f, width=15, height=2, bg="#ffc107", fg="#000")
    btn.pack(padx=10, pady=10)

# Teclado numérico (opcional)
teclado_frame = tk.Frame(frame_funciones, bg="#f9f9f9")
teclado_frame.pack(pady=10)

for i in range(1, 10):
    btn = tk.Button(teclado_frame, text=str(i), width=5, height=2)
    btn.grid(row=(i-1)//3, column=(i-1)%3, padx=2, pady=2)

btn0 = tk.Button(teclado_frame, text="0", width=5, height=2)
btn0.grid(row=3, column=1, padx=2, pady=2)

# --- Loop ---
root.mainloop()
