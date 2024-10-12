import sqlite3
from tkinter import *
from tkinter import ttk


class SistemaExpertoGimnasio:
    def __init__(self):
        self.bd = 'sistema_experto_gimnasio.db'


   
    def conectar_bd(self):
        return sqlite3.connect(self.bd)


    def guardar_hechos(self, hechos):
        conexion = self.conectar_bd()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO Hechos (nombre, objetivo, tipo_ejercicio, nivel, edad, altura, peso, condicion_medica)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            hechos["nombre"],
            hechos["objetivo"],
            hechos["tipo_ejercicio"],
            hechos["nivel"],
            hechos["edad"],
            hechos["altura"],
            hechos["peso"],
            hechos["condicion_medica"]
        ))
        conexion.commit()
        conexion.close()




    def obtener_conclusiones(self, hechos):
        conexion = self.conectar_bd()
        cursor = conexion.cursor()
        cursor.execute('''
            SELECT C.conclusion FROM Reglas R
            JOIN Conclusiones C ON R.id = C.id_regla
            WHERE (R.objetivo IS NULL OR R.objetivo = ?)
            AND (R.tipo_ejercicio IS NULL OR R.tipo_ejercicio = ?)
            AND (R.nivel IS NULL OR R.nivel = ?)
            AND (R.condicion_medica IS NULL OR R.condicion_medica = ?)
        ''', (
            hechos["objetivo"],
            hechos["tipo_ejercicio"],
            hechos["nivel"],
            hechos["condicion_medica"]
        ))
        conclusiones = cursor.fetchall()
        conexion.close()


        return [conclusion[0] for conclusion in conclusiones]




def ingresar_hechos():
    hechos = {}
    hechos["nombre"] = nombre_entry.get()
    hechos["objetivo"] = objetivo_entry.get().lower()
    hechos["tipo_ejercicio"] = tipo_ejercicio_entry.get().lower()
    hechos["nivel"] = nivel_entry.get().lower()
    hechos["edad"] = int(edad_entry.get())
    hechos["altura"] = int(altura_entry.get())
    hechos["peso"] = int(peso_entry.get())
    hechos["condicion_medica"] = condicion_medica_entry.get().lower() or None




    sistema = SistemaExpertoGimnasio()
    sistema.guardar_hechos(hechos)
    conclusiones = sistema.obtener_conclusiones(hechos)




    if conclusiones:
        conclusiones_label.config(text=f"Recomendaciones: {', '.join(conclusiones)}", fg="green")
    else:
        conclusiones_label.config(text="No se encontraron recomendaciones, pero los hechos han sido guardados.", fg="red")




root = Tk()
root.title("Sistema Experto de Ejercicios")
root.geometry("500x500")
root.configure(bg="#f0f4f5")




title_label = Label(root, text="Sistema Experto - Gimnasio", font=("Arial", 20, "bold"), bg="#f0f4f5", fg="#333333")
title_label.pack(pady=20)




form_frame = Frame(root, bg="#f0f4f5")
form_frame.pack(pady=10, padx=20)




label_style = {"bg": "#f0f4f5", "fg": "#333333", "font": ("Arial", 12)}
entry_style = {"width": 30, "font": ("Arial", 12)}



Label(form_frame, text="Nombre", **label_style).grid(row=0, column=0, sticky=W, pady=5)
nombre_entry = Entry(form_frame, **entry_style)
nombre_entry.grid(row=0, column=1, pady=5)


Label(form_frame, text="Objetivo", **label_style).grid(row=1, column=0, sticky=W, pady=5)
objetivo_entry = Entry(form_frame, **entry_style)
objetivo_entry.grid(row=1, column=1, pady=5)


Label(form_frame, text="Tipo de Ejercicio", **label_style).grid(row=2, column=0, sticky=W, pady=5)
tipo_ejercicio_entry = Entry(form_frame, **entry_style)
tipo_ejercicio_entry.grid(row=2, column=1, pady=5)


Label(form_frame, text="Nivel", **label_style).grid(row=3, column=0, sticky=W, pady=5)
nivel_entry = Entry(form_frame, **entry_style)
nivel_entry.grid(row=3, column=1, pady=5)


Label(form_frame, text="Edad", **label_style).grid(row=4, column=0, sticky=W, pady=5)
edad_entry = Entry(form_frame, **entry_style)
edad_entry.grid(row=4, column=1, pady=5)


Label(form_frame, text="Altura (cm)", **label_style).grid(row=5, column=0, sticky=W, pady=5)
altura_entry = Entry(form_frame, **entry_style)
altura_entry.grid(row=5, column=1, pady=5)


Label(form_frame, text="Peso (kg)", **label_style).grid(row=6, column=0, sticky=W, pady=5)
peso_entry = Entry(form_frame, **entry_style)
peso_entry.grid(row=6, column=1, pady=5)


Label(form_frame, text="Condición Médica (Opcional)", **label_style).grid(row=7, column=0, sticky=W, pady=5)
condicion_medica_entry = Entry(form_frame, **entry_style)
condicion_medica_entry.grid(row=7, column=1, pady=5)




enviar_button = Button(root, text="Generar Recomendaciones", command=ingresar_hechos, bg="#4caf50", fg="white", font=("Arial", 14), width=25)
enviar_button.pack(pady=20)




conclusiones_label = Label(root, text="", font=("Arial", 12, "bold"), bg="#f0f4f5")
conclusiones_label.pack(pady=10)


root.mainloop()

