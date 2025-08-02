import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re

from models.hotel import *
from Core.controller import *


class InterfazApp:
    def validar_caracter(self, valor):
            return re.fullmatch(r"[\d\-]{0,10}", valor) is not None

    def validar_fecha(self):
        campos = [("entrada", self.fecha_entrada.get()), ("salida", self.fecha_salida.get())]
        for nombre, fecha in campos:
            try:
                datetime.strptime(fecha, "%d-%m-%Y")
            except ValueError:
                messagebox.showerror("Error", f"La fecha de {nombre} debe tener el formato DD-MM-AAAA y ser válida.")
                return False
        return True
    
    def validar_orden_fechas(self):
        fecha_entrada = datetime.strptime(self.fecha_entrada.get(), "%d-%m-%Y")
        fecha_salida = datetime.strptime(self.fecha_salida.get(), "%d-%m-%Y")

        if fecha_salida <= fecha_entrada:
            messagebox.showerror("Error", "La fecha de salida debe ser posterior a la fecha de entrada.")
            print("false")
            return False
        return True
            


    def __init__(self, root):
        self.root = root
        self.root.title("Comparador de precios - Alvear Hotel")

        # Permite que las columnas se expandan
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=2)

        # Permite que la fila de resultados se expanda
        root.grid_rowconfigure(5, weight=1)

        # Campos de entrada
        self.seleccion_hotel = tk.StringVar()
        self.seleccion_habitacion_excel = tk.StringVar()
        self.fecha_entrada = tk.StringVar()
        self.fecha_salida = tk.StringVar()
        self.adultos = tk.IntVar()
        self.niños = tk.IntVar()
        self.habitacion = tk.StringVar()
        self.combo= tk.StringVar()

        vcmd = (root.register(self.validar_caracter), '%P')

        ttk.Label(root, text="Selección hotel:").grid(row=0, column=0, sticky='w', padx=4, pady=2)
        hotel_cb = ttk.Combobox(
            root,
            textvariable=self.seleccion_hotel,
            values=["Hotel A", "Hotel B"],
            state="readonly"
        )
        hotel_cb.current(0)
        hotel_cb.grid(row=0, column=1, sticky='ew', padx=4, pady=2)

        # --- FILA 1: Selección de habitación Excel ---
        ttk.Label(root, text="Selección habitación Excel:").grid(row=1, column=0, sticky='w', padx=4, pady=2)
        self.habit_excel_cb = ttk.Combobox(
            root,
            textvariable=self.seleccion_habitacion_excel,
            state="readonly"
        )
        self.habit_excel_cb.grid(row=1, column=1, sticky='ew', padx=4, pady=2)
        self.habit_excel_cb.bind("<<ComboboxSelected>>", self.on_habitacion_excel_cambiada)
        self.cargar_habitaciones_excel()

        ttk.Label(root, text="Precio de la habitación").grid(row=0, column=2, sticky='w', padx=4, pady=2)
        self.precio_var = tk.StringVar(value="(ninguna seleccionada)")
        self.label_precio = ttk.Label(root, textvariable=self.precio_var)
        self.label_precio.grid(row=1, column=2, sticky='w', padx=4, pady=2)

        # --- FILA 2: Fecha de entrada ---
        ttk.Label(root, text="Fecha de entrada (DD-MM-AAAA):").grid(row=2, column=0, sticky='w', padx=4, pady=2)
        ttk.Entry(root, textvariable=self.fecha_entrada, validate='key', validatecommand=vcmd).grid(row=2, column=1, sticky='ew', padx=4, pady=2)

        # --- FILA 3: Fecha de salida ---
        ttk.Label(root, text="Fecha de salida (DD-MM-AAAA):").grid(row=3, column=0, sticky='w', padx=4, pady=2)
        ttk.Entry(root, textvariable=self.fecha_salida, validate='key', validatecommand=vcmd).grid(row=3, column=1, sticky='ew', padx=4, pady=2)

        # --- FILA 4: Adultos ---
        ttk.Label(root, text="Cantidad de adultos:").grid(row=4, column=0, sticky='w', padx=4, pady=2)
        ttk.Entry(root, textvariable=self.adultos).grid(row=4, column=1, sticky='ew', padx=4, pady=2)

        # --- FILA 5: Niños ---
        ttk.Label(root, text="Cantidad de niños:").grid(row=5, column=0, sticky='w', padx=4, pady=2)
        ttk.Entry(root, textvariable=self.niños).grid(row=5, column=1, sticky='ew', padx=4, pady=2)


        # --- BOTÓN de ejecución ---
        ttk.Button(root, text="Ejecutar comparación", command=self.ejecutar).grid(
            row=8, column=0, columnspan=2, sticky='ew', padx=4, pady=6
        )

        # Área de resultados (expansible)
        self.resultado = tk.Text(root, height=15, width=80)
        self.resultado.grid(row=9, column=0, columnspan=2, sticky='nsew', padx=4, pady=2)

        # Hacer que la columna 1 se expanda por 3
        root.columnconfigure(1, weight=3)
        root.rowconfigure(9, weight=1)

    def cargar_habitaciones_excel(self):
        # accede a lo que ya tiene el gestor
        self.habitaciones_excel = dar_habitaciones_excel()
        #self.mapa_por_nombre = {h.nombre: h for h in self.habitaciones_excel}
        #self.habit_excel_cb['values'] = list(self.mapa_por_nombre.keys())
        self.habit_excel_cb['values'] = [HabitacionExcel.nombre for HabitacionExcel in self.habitaciones_excel]
        if self.habitaciones_excel:
            self.habit_excel_cb.current(0)
            self.on_habitacion_excel_cambiada(None)

    def on_habitacion_excel_cambiada(self, event):
        seleccionado = self.seleccion_habitacion_excel.get()
        try:
            idx = self.habit_excel_cb['values'].index(seleccionado)
            habitacion = self.habitaciones_excel[idx]
            print()
            print(habitacion.row_idx, habitacion.precio)
        except ValueError:
            # no encontrado
            pass
       
        # seleccionado = self.seleccion_habitacion_excel.get()
        # # Buscamos el objeto correspondiente (primer match)
        # match = next((h for h in self.habit_excel_cb if h == seleccionado), None)
        # if match:
        #     for self.habitaciones.excel.nombre in self.habitaciones_excel
        #     precio = match.precio
        #     # Formateo simple
        #     self.precio_var.set(f"${precio:,.2f}")
        # else:
        #     self.precio_var.set("No disponible")

            
    def ejecutar(self):
        if not self.validar_fecha():
            return
        
        if not self.validar_orden_fechas():
            return
    
    
        datos = (
            self.fecha_entrada.get(),
            self.fecha_salida.get(),
            self.adultos.get(),
            self.niños.get(),
            self.combo.get(),
            self.habitacion.get()
        )
        self.resultado.insert(tk.END, f"Ejecutando scraping con: {datos}\n")
        # Acá llamás a tu lógica real luego

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazApp(root)
    root.mainloop()
