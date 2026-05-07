#! /usr/bin/env python3
from parser import parser
import lexico
from semantico import AnalizadorSemantico
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import pprint



class RedireccionConsola:
    def __init__(self, widget_texto):
        self.widget = widget_texto
    def write(self, string):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert(tk.END, string)
        self.widget.see(tk.END)
        self.widget.config(state=tk.DISABLED)
    def flush(self):
        pass


class interfazGrafica:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MiniLang (Fase 2)")
        self.root.geometry("926x700")
        self.root.configure(bg="#201F1F")

        self.archivoActual = None
        self.FONDO = "#201F1F"
        self.BarraLAT = "#252526"
        self.BarraARRIBA = "#121212"
        self.BarraARRIBAB = "#3F3F3F"
        self.BarraOPCIONES = "#343333"
        self.ExplTexto = "#cccccc"

        self.barraOpc = tk.Frame(self.root, bg=self.BarraOPCIONES, width=50)
        self.barraOpc.pack(side="left", fill="y")
        tk.Button(self.barraOpc, text="archivos", bg=self.BarraOPCIONES, fg="white", relief="flat", command=self.abrirArchivo).pack(pady=10, fill="x")
        tk.Button(self.barraOpc, text="verificar", bg=self.BarraOPCIONES, fg="#5efff2", relief="flat", command=self.analizar).pack(pady=10, fill="x")

        self.barraL = tk.Frame(self.root, bg=self.BarraLAT, width=140)
        self.barraL.pack(side="left", fill="y")
        self.barraL.pack_propagate(False)
        tk.Label(self.barraL, text="EXPLORER", bg=self.BarraLAT, fg=self.ExplTexto, font=("Consolas", 9, "bold")).pack(pady=10, padx=5)
        self.archivoMuestra = tk.Label(self.barraL, text=" ", bg=self.BarraLAT, fg="#858585", font=("Consolas",9))
        self.archivoMuestra.pack(pady=5)

        self.barraA = tk.Frame(self.root, bg=self.BarraARRIBA, height=23)
        self.barraA.pack(side="top", fill="x")

        self.barraAB = tk.Frame(self.root, bg=self.BarraARRIBAB, height=5)
        self.barraAB.pack(side="top", fill="x")

        self.cuadroTexto = tk.Frame(self.root, bg=self.FONDO)
        self.cuadroTexto.pack(side="right", expand=True, fill="both")
        self.editor = tk.Text(self.cuadroTexto, bg=self.FONDO, fg="#e3dada", insertbackground="white", relief="flat", font=("Consolas", 11), padx=10, pady=10, undo=True, wrap=tk.NONE)
        self.editor.pack(expand=True, fill="both")

        self.consolaMensaje = tk.Text(self.cuadroTexto, bg="#111111", fg="#fffb00", height=10, relief="flat", font=("Consolas", 10), padx=10, pady=10)
        self.consolaMensaje.pack(side="bottom", fill="x")

        sys.stdout=RedireccionConsola( self.consolaMensaje)
        
        print("C:/users/personaprueba/downloads/minilang> subir un archivo .mlng y luego presione analizar")

        self.root.mainloop()

    def terminal(self, mensaje):
        self.consolaMensaje.config(state=tk.NORMAL)
        self.consolaMensaje.insert(tk.END, f">{mensaje}\n")
        self.consolaMensaje.config(state=tk.DISABLED)
        self.consolaMensaje.see(tk.END)

    def abrirArchivo(self):
        initial_dir = os.path.join(os.getcwd(), "pruebas")
        if not os.path.exists(initial_dir): initial_dir = os.getcwd()
        filepath = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Minilang", "*.mlng"),("Legacy", "*.mlng")])
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.editor.delete(1.0, tk.END)
                self.editor.insert(1.0, f.read())
            self.archivoActual = filepath
            self.archivoMuestra.config(text=os.path.basename(filepath), fg="#e5e9ee")
            print(f"Archivo cargado: {filepath}")

    def analizar(self):
        
        codigo = self.editor.get(1.0, tk.END)
        if not codigo.endswith('\n'):
            codigo += '\n'
        codigo += '\n' 
        lexico.lexer.lineno=1
        lexico.pila_indentacion=[0]
        lexico.dedents_pendientes=[]
        lexico.inicio_linea = True
        lexico.linea_token = False
        hay_error = False

        self.consolaMensaje.config(state=tk.NORMAL)
        self.consolaMensaje.delete(1.0, tk.END)
        self.consolaMensaje.config(state=tk.DISABLED)
        try:
            resultado = parser.parse(codigo, lexer=lexico.lexer)
            semantico = AnalizadorSemantico()
            semantico.analizar(resultado)
            print("\nAnálisis semántico completado.")
            semantico.tabla_simbolos.imprimir()
            if self.archivoActual:
                nombreSinExte = os.path.splitext(os.path.basename(self.archivoActual))[0]
                if not os.path.exists("salidas"): os.makedirs("salidas")
                rutaOut = os.path.join("salidas", nombreSinExte + ".out")
            
                # Obtenemos todo lo que se imprimió en la consola (los tokens con línea/col)
                contenidocompleto = self.consolaMensaje.get(1.0, tk.END).strip()
                with open(rutaOut, "w", encoding="utf-8") as archivoout:
                    archivoout.write("--- ANÁLISIS LÉXICO (TOKENS) ---\n")
                    archivoout.write(contenidocompleto)
                    archivoout.write("\n\n--- ÁRBOL DE SINTAXIS (AST) ---\n")
                
                    # Usamos pformat para convertir el árbol en un string con sangría (indent)
                    arbol_formateado = pprint.pformat(resultado, indent=4, width=80)
                    archivoout.write(arbol_formateado)
                    archivoout.write("\n\n--- ANÁLISIS SEMÁNTICO (TABLA DE SÍMBOLOS) ---\n")
                    for nombre, simbolo in semantico.tabla_simbolos.tabla.items():
                        archivoout.write(
f"""
Nombre      : {nombre}
Tipo        : {simbolo['tipo']}
Valor       : {simbolo['valor']}
Constante   : {simbolo['constante']}

"""
)
            
                print(f"\n[INFO] Archivo de salida guardado en: {rutaOut}")

            if not hay_error:
                print("\n" + "="*30)
                print("ESTRUCTURA DEL ÁRBOL (AST)")
                print("="*30)
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(resultado)
            else:
                print("Se encontraron errores")
        
        except Exception as e:
            print(f"Ocurrio un error inesperado: {e}")

if __name__ == "__main__":
    interfazGrafica()
