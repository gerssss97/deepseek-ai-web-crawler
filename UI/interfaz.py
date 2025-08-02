import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re

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
        self.fecha_entrada = tk.StringVar()
        self.fecha_salida = tk.StringVar()
        self.adultos = tk.IntVar()
        self.niños = tk.IntVar()
        self.habitacion = tk.StringVar()
        self.combo= tk.StringVar()

        vcmd = (root.register(self.validar_caracter), '%P')


        ttk.Label(root, text="Fecha de entrada (DD-MM-AAAA):").grid(row=0, column=0, sticky='w')
        ttk.Entry(root, textvariable=self.fecha_entrada, validate='key', validatecommand=vcmd).grid(row=0, column=1, sticky='ew')
        ttk.Button(root, text="Validar fecha", command=self.validar_fecha).grid(row=1, column=2, sticky='e')
       

        ttk.Label(root, text="Fecha de salida (DD-MM-AAAA):").grid(row=1, column=0, sticky='w')
        ttk.Entry(root, textvariable=self.fecha_salida, validate='key', validatecommand=vcmd).grid(row=1, column=1, sticky='ew')
        ttk.Button(root, text="Validar orden fecha", command=self.validar_orden_fechas).grid(row=0, column=2, sticky='e')

        ttk.Label(root, text="Cantidad de adultos:").grid(row=2, column=0, sticky='w')
        ttk.Entry(root, textvariable=self.adultos).grid(row=2, column=1, sticky='ew')

        ttk.Label(root, text="Cantidad de niños:").grid(row=3, column=0, sticky='w')
        ttk.Entry(root, textvariable=self.niños).grid(row=3, column=1, sticky='ew')
        
        ttk.Label(root, text="Seleccione la habitacion del hotel").grid(row=3, column=0, sticky='w')
        ttk.Entry(root, textvariable=self.habitacion).grid(row=3, column=1, sticky='ew')
        
        ttk.Label(root, text="Seleccione el combo").grid(row=3, column=0, sticky='w')
        ttk.Entry(root, textvariable=self.combo).grid(row=3, column=1, sticky='ew')

        ttk.Button(root, text="Ejecutar comparación", command=self.ejecutar).grid(row=4, column=0, columnspan=2, sticky='ew')

        # Área de resultados (expansible)
        self.resultado = tk.Text(root, height=15, width=80)
        self.resultado.grid(row=5, column=0, columnspan=2, sticky='nsew')
    
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
