import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re

class InterfazApp:
    def validar_caracter(self, valor):
            return re.fullmatch(r"[\d\-]{0,10}", valor) is not None

    def validar_fecha(self):
        fecha = self.fecha_entrada.get()
        try:
            datetime.strptime(fecha, "%d-%m-%Y")
            return True
            #messagebox.showinfo("Fecha válida", "La fecha tiene el formato correcto.")
        except ValueError:
            messagebox.showerror("Error", "La fecha debe tener el formato DD-MM-AAAA y ser válida.")
            return False
            


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

        vcmd = (root.register(self.validar_caracter), '%P')


        ttk.Label(root, text="Fecha de entrada (DD-MM-AAAA):").grid(row=0, column=0, sticky='w')
        ttk.Entry(root, textvariable=self.fecha_entrada, validate='key', validatecommand=vcmd).grid(row=0, column=1, sticky='ew')
        ttk.Button(root, text="Validar fecha", command=self.validar_fecha).grid(row=1, column=2, sticky='e')
       

        ttk.Label(root, text="Fecha de salida (DD-MM-AAAA):").grid(row=1, column=0, sticky='w')
        ttk.Entry(root, textvariable=self.fecha_salida).grid(row=1, column=1, sticky='ew')

        ttk.Label(root, text="Cantidad de adultos:").grid(row=2, column=0, sticky='w')
        ttk.Entry(root, textvariable=self.adultos).grid(row=2, column=1, sticky='ew')

        ttk.Label(root, text="Cantidad de niños:").grid(row=3, column=0, sticky='w')
        ttk.Entry(root, textvariable=self.niños).grid(row=3, column=1, sticky='ew')

        ttk.Button(root, text="Ejecutar comparación", command=self.ejecutar).grid(row=4, column=0, columnspan=2, sticky='ew')

        # Área de resultados (expansible)
        self.resultado = tk.Text(root, height=15, width=80)
        self.resultado.grid(row=5, column=0, columnspan=2, sticky='nsew')
    def ejecutar(self):
        if not self.validar_fecha():
                return
        # Acá luego llamarás a tu crawler y a la comparación
        datos = (
            self.fecha_entrada.get(),
            self.fecha_salida.get(),
            self.adultos.get(),
            self.niños.get()
        )
        self.resultado.insert(tk.END, f"Ejecutando scraping con: {datos}\n")
        # Acá llamás a tu lógica real luego

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazApp(root)
    root.mainloop()
