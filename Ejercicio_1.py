# ---------------------------------------------------------
# SMART VEHICLE SYSTEM - FINAL PROJECT
# Author: Camilo Andres Leon Rubriche
# Course: Programming
# University: UNAD
# Description:
# This system simulates different types of vehicles using
# Object-Oriented Programming concepts such as inheritance,
# polymorphism and method overloading. Includes a GUI built
# with Tkinter for user interaction.
# ---------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
import logging

# -------------------------
# LOG CONFIGURATION
# -------------------------

# Guarda eventos importantes (agregar/eliminar vehículos, simulaciones) en un archivo .txt
logging.basicConfig(filename="vehicle_log.txt", level=logging.INFO)


# -------------------------
# BASE CLASS
# -------------------------

# Clase base de la que heredan todos los tipos de vehículos (herencia)
class Vehiculo:

    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
        self.velocidad_actual = 0  # todos los vehículos arrancan detenidos

    def acelerar(self, turbo=False, terrain="normal"):
        """Simulates acceleration with optional parameters (overloading concept)"""
        incremento = 10  # incremento base de velocidad por aceleración

        # Modo turbo duplica el incremento
        if turbo:
            incremento *= 2

        # El terreno ajusta el incremento: montaña frena, autopista impulsa
        if terrain == "mountain":
            incremento *= 0.7
        elif terrain == "highway":
            incremento *= 1.2

        self.velocidad_actual += incremento

    def detener(self):
        """Stops the vehicle"""
        self.velocidad_actual = 0

    def resetear(self):
        """Resets vehicle state so each simulation run starts from zero"""
        self.velocidad_actual = 0

    def obtener_informacion(self):
        # Devuelve un resumen del estado actual del vehículo como texto
        return f"{self.marca} {self.modelo} | Speed: {round(self.velocidad_actual, 2)}"


# -------------------------
# CHILD CLASSES
# -------------------------

# Hereda de Vehiculo y agrega el atributo batería (polimorfismo: sobreescribe acelerar)
class AutoElectrico(Vehiculo):

    def __init__(self, marca, modelo):
        super().__init__(marca, modelo)
        self.bateria = 100  # batería comienza al 100%

    def acelerar(self, turbo=False, terrain="normal"):
        super().acelerar(turbo, terrain)  # ejecuta la lógica base de aceleración
        self.bateria -= 2                 # cada aceleración consume 2% de batería

    def resetear(self):
        super().resetear()       # reinicia la velocidad
        self.bateria = 100       # también recarga la batería al simular de nuevo

    def obtener_informacion(self):
        # Añade el nivel de batería al resumen heredado del padre
        return f"{super().obtener_informacion()} | Battery: {self.bateria}%"


# Moto: vehículo ágil, ignora turbo y terreno, acelera siempre la misma cantidad
class Moto(Vehiculo):

    INCREMENTO = 15  # fixed speed increment — motorcycles ignore turbo/terrain

    def acelerar(self, turbo=False, terrain="normal"):
        # Sobreescribe el método del padre: no aplica modificadores, solo suma fijo
        self.velocidad_actual += self.INCREMENTO

    def detener(self):
        """Motorcycles stop instantly (lightweight vehicle)"""
        self.velocidad_actual = 0  # freno instantáneo por ser liviana


# Camión: vehículo pesado, acelera poco y no puede frenar de golpe
class Camion(Vehiculo):

    INCREMENTO = 5   # fixed speed increment — trucks ignore turbo/terrain

    def acelerar(self, turbo=False, terrain="normal"):
        # Sobreescribe el método del padre: incremento pequeño por ser pesado
        self.velocidad_actual += self.INCREMENTO

    def detener(self):
        """Trucks apply gradual braking before stopping (heavy vehicle)"""
        # Freno gradual: reduce la velocidad a la mitad en lugar de parar de inmediato
        self.velocidad_actual = round(self.velocidad_actual * 0.5, 2)


# -------------------------
# VEHICLE REGISTRY
# Single source of truth: name → class.
# All other mappings (combobox options, treeview labels) are derived from this.
# -------------------------

VEHICLE_REGISTRY = {
    "Electric Car": AutoElectrico,
    "Motorcycle":   Moto,
    "Truck":        Camion,
}

# Mapeo inverso: dado el objeto clase, obtiene su nombre legible (e.g. AutoElectrico → "Electric Car")
TYPE_LABEL        = {cls: name for name, cls in VEHICLE_REGISTRY.items()}
# Lista de opciones para el menú desplegable de la GUI
COMBOBOX_OPTIONS  = [f"  {name}" for name in VEHICLE_REGISTRY]


# -------------------------
# SYSTEM CONTROLLER
# -------------------------

class SistemaVehiculos:

    def __init__(self):
        self.vehiculos = []

    def agregar_vehiculo(self, tipo, marca, modelo):
        # Valida los campos antes de crear el vehículo
        if not tipo:
            raise ValueError("Please select a vehicle type")
        if not marca or not modelo:
            raise ValueError("Fields cannot be empty")
        if tipo not in VEHICLE_REGISTRY:
            raise ValueError("Invalid vehicle type")

        # Instancia dinámicamente la clase correcta según el tipo seleccionado
        v = VEHICLE_REGISTRY[tipo](marca, modelo)
        self.vehiculos.append(v)
        logging.info(f"Vehicle added: {marca} {modelo}")
        return v

    def eliminar_vehiculo(self, index):
        # Elimina el vehículo en la posición dada si el índice es válido
        if 0 <= index < len(self.vehiculos):
            removed = self.vehiculos.pop(index)
            logging.info(f"Vehicle removed: {removed.marca} {removed.modelo}")

    def simular(self, turbo=True, terrain="highway"):
        lines = []
        for v in self.vehiculos:
            v.resetear()                              # reinicia para que la simulación sea consistente
            v.acelerar(turbo=turbo, terrain=terrain)  # condiciones elegidas por el usuario
            lines.append(v.obtener_informacion())     # recoge el resultado de cada vehículo

        resultado = "\n".join(lines)
        self.exportar_reporte(resultado)  # guarda el resultado en un archivo
        logging.info("Simulation executed")
        return resultado

    def exportar_reporte(self, texto):
        # Escribe los resultados de la simulación en un archivo de texto plano
        with open("simulation_report.txt", "w") as f:
            f.write(texto)


# -------------------------
# GUI - MODERN DARK THEME
# -------------------------

# Color Palette
BG      = "#0b0c1a"
PANEL   = "#13142a"
CARD    = "#1e1f38"
ACCENT  = "#7c6fff"
CYAN    = "#00d4ff"
TEXT    = "#e8e8f4"
SUBTEXT = "#6b6b99"
SUCCESS = "#00e676"
WARNING = "#ff6b6b"
BTN_SIM = "#00b894"
BTN_CLR = "#4a4a6a"
BTN_DEL = "#c0392b"


class Interfaz:

    def __init__(self, root):
        self.sistema = SistemaVehiculos()  # controlador con la lógica del sistema

        root.title("Smart Vehicle System")
        root.geometry("860x580")
        root.configure(bg=BG)
        root.resizable(False, False)
        root.bind("<Return>", lambda _: self.agregar())  # Enter también agrega vehículo

        self._configure_styles()
        self._build_header(root)
        self._build_body(root)
        self._build_statusbar(root)

    # ------------------------------------------------------------------
    # STYLE SETUP
    # ------------------------------------------------------------------

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Dark.TCombobox",
            fieldbackground=CARD, background=CARD,
            foreground=TEXT, selectbackground=ACCENT,
            selectforeground=TEXT, borderwidth=0, arrowcolor=CYAN,
        )
        style.map(
            "Dark.TCombobox",
            fieldbackground=[("readonly", CARD)],
            foreground=[("readonly", TEXT)],
        )

        style.configure("Dark.TNotebook", background=BG, borderwidth=0, tabmargins=0)
        style.configure(
            "Dark.TNotebook.Tab",
            background=CARD, foreground=SUBTEXT,
            font=("Segoe UI", 9, "bold"), padding=(14, 7), borderwidth=0,
        )
        style.map(
            "Dark.TNotebook.Tab",
            background=[("selected", PANEL)],
            foreground=[("selected", ACCENT)],
        )

        style.configure(
            "Dark.Treeview",
            background=CARD, foreground=TEXT, fieldbackground=CARD,
            borderwidth=0, rowheight=28, font=("Segoe UI", 9),
        )
        style.configure(
            "Dark.Treeview.Heading",
            background=PANEL, foreground=ACCENT,
            font=("Segoe UI", 8, "bold"), borderwidth=0, relief="flat",
        )
        style.map(
            "Dark.Treeview",
            background=[("selected", ACCENT)],
            foreground=[("selected", TEXT)],
        )

    # ------------------------------------------------------------------
    # LAYOUT BUILDERS
    # ------------------------------------------------------------------

    def _build_header(self, root):
        header = tk.Frame(root, bg=PANEL, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Frame(header, bg=ACCENT, height=3).pack(fill="x", side="top")

        inner = tk.Frame(header, bg=PANEL)
        inner.pack(fill="both", expand=True, padx=30)

        tk.Label(inner, text="SMART VEHICLE SYSTEM",
                 font=("Segoe UI", 18, "bold"), bg=PANEL, fg=CYAN
                 ).pack(side="left", pady=14)

        tk.Label(inner, text="  //  Simulation Dashboard",
                 font=("Segoe UI", 10), bg=PANEL, fg=SUBTEXT
                 ).pack(side="left", pady=20)

        tk.Label(inner, text="UNAD  v1.2",
                 font=("Segoe UI", 8, "bold"), bg=ACCENT, fg=TEXT, padx=8, pady=3
                 ).pack(side="right", pady=20)

    def _build_body(self, root):
        body = tk.Frame(root, bg=BG)
        body.pack(fill="both", expand=True, padx=18, pady=14)
        self._build_left_panel(body)
        self._build_right_panel(body)

    def _build_left_panel(self, parent):
        left = tk.Frame(parent, bg=PANEL, width=260)
        left.pack(side="left", fill="y", padx=(0, 12))
        left.pack_propagate(False)

        self._section_title(left, "ADD VEHICLE")

        tk.Label(left, text="Vehicle Type",
                 font=("Segoe UI", 8, "bold"), bg=PANEL, fg=SUBTEXT,
                 ).pack(padx=20, anchor="w", pady=(8, 2))

        self.tipo_var = tk.StringVar()
        self.tipo = ttk.Combobox(
            left, textvariable=self.tipo_var,
            values=COMBOBOX_OPTIONS,
            state="readonly", style="Dark.TCombobox", font=("Segoe UI", 10),
        )
        self.tipo.pack(padx=20, fill="x", pady=(0, 10))

        tk.Label(left, text="Brand",
                 font=("Segoe UI", 8, "bold"), bg=PANEL, fg=SUBTEXT,
                 ).pack(padx=20, anchor="w", pady=(0, 2))
        self.marca = self._create_entry(left)

        tk.Label(left, text="Model",
                 font=("Segoe UI", 8, "bold"), bg=PANEL, fg=SUBTEXT,
                 ).pack(padx=20, anchor="w", pady=(8, 2))
        self.modelo = self._create_entry(left)

        tk.Frame(left, bg=CARD, height=1).pack(fill="x", padx=20, pady=(14, 6))

        tk.Label(left, text="SIM CONDITIONS",
                 font=("Segoe UI", 7, "bold"), bg=PANEL, fg=SUBTEXT,
                 ).pack(padx=20, anchor="w", pady=(0, 4))

        tk.Label(left, text="Terrain",
                 font=("Segoe UI", 8, "bold"), bg=PANEL, fg=SUBTEXT,
                 ).pack(padx=20, anchor="w", pady=(0, 2))
        self.terrain_var = tk.StringVar(value="  highway")
        self.terrain_cb = ttk.Combobox(
            left, textvariable=self.terrain_var,
            values=["  normal", "  mountain", "  highway"],
            state="readonly", style="Dark.TCombobox", font=("Segoe UI", 10),
        )
        self.terrain_cb.pack(padx=20, fill="x", pady=(0, 6))

        self.turbo_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            left, text="  Turbo mode", variable=self.turbo_var,
            bg=PANEL, fg=TEXT, selectcolor=CARD,
            activebackground=PANEL, activeforeground=CYAN,
            font=("Segoe UI", 9), cursor="hand2",
        ).pack(padx=20, anchor="w", pady=(0, 8))

        tk.Frame(left, bg=CARD, height=1).pack(fill="x", padx=20, pady=(0, 6))

        self._create_button(left, "  ADD VEHICLE",    self.agregar, ACCENT)
        self._create_button(left, "  RUN SIMULATION", self.simular, BTN_SIM)
        self._create_button(left, "  CLEAR OUTPUT",   self.limpiar, BTN_CLR)

        self.counter_label = tk.Label(
            left, text="Fleet: 0 vehicles",
            font=("Segoe UI", 8), bg=PANEL, fg=SUBTEXT,
        )
        self.counter_label.pack(pady=(12, 0))

    def _build_right_panel(self, parent):
        right = tk.Frame(parent, bg=PANEL)
        right.pack(side="left", fill="both", expand=True)

        self._section_title(right, "DASHBOARD")

        self.notebook = ttk.Notebook(right, style="Dark.TNotebook")
        self.notebook.pack(padx=20, pady=(0, 16), fill="both", expand=True)

        fleet_tab = tk.Frame(self.notebook, bg=CARD)
        self.notebook.add(fleet_tab, text="  FLEET  ")
        self._build_fleet_tab(fleet_tab)

        output_tab = tk.Frame(self.notebook, bg=CARD)
        self.notebook.add(output_tab, text="  OUTPUT  ")
        self._build_output_tab(output_tab)

    def _build_fleet_tab(self, parent):
        cols = ("type", "brand", "model", "speed")
        self.tree = ttk.Treeview(
            parent, columns=cols, show="headings",
            style="Dark.Treeview", selectmode="browse",
        )
        for col, label, width in [
            ("type",  "Type",         110),
            ("brand", "Brand",        110),
            ("model", "Model",        110),
            ("speed", "Speed (km/h)", 110),
        ]:
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width, anchor="center")

        scrollbar = tk.Scrollbar(parent, command=self.tree.yview, bg=PANEL, troughcolor=BG)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        btn_bar = tk.Frame(parent, bg=CARD)
        btn_bar.pack(fill="x", pady=(6, 8), padx=8)

        self._create_button(
            btn_bar, "  REMOVE SELECTED", self.eliminar_seleccionado, BTN_DEL,
            side="left", padx=4, pady=4, ipadx=6,
        )

    def _build_output_tab(self, parent):
        self.output = tk.Text(
            parent, font=("Consolas", 10),
            bg=CARD, fg=CYAN, insertbackground=TEXT,
            selectbackground=ACCENT, selectforeground=TEXT,
            relief="flat", borderwidth=0, padx=14, pady=14, wrap="word",
        )
        scrollbar = tk.Scrollbar(parent, command=self.output.yview, bg=PANEL, troughcolor=BG)
        self.output.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.output.pack(fill="both", expand=True)
        self._set_placeholder()

    def _build_statusbar(self, root):
        bar = tk.Frame(root, bg=CARD, height=24)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)

        self.status_dot = tk.Label(bar, text="●", font=("Segoe UI", 9), bg=CARD, fg=SUCCESS)
        self.status_dot.pack(side="left", padx=(12, 4), pady=4)

        self.status_label = tk.Label(
            bar, text="System ready  —  Press Enter or click Add Vehicle",
            font=("Segoe UI", 8), bg=CARD, fg=SUBTEXT,
        )
        self.status_label.pack(side="left", pady=4)

        tk.Label(
            bar, text="Smart Vehicle System  |  UNAD  |  Programming",
            font=("Segoe UI", 8), bg=CARD, fg=SUBTEXT,
        ).pack(side="right", padx=12, pady=4)

    # ------------------------------------------------------------------
    # WIDGET HELPERS
    # ------------------------------------------------------------------

    def _section_title(self, parent, text):
        tk.Label(parent, text=text, font=("Segoe UI", 9, "bold"),
                 bg=PANEL, fg=ACCENT).pack(padx=20, pady=(16, 4), anchor="w")
        tk.Frame(parent, bg=ACCENT, height=2).pack(fill="x", padx=20, pady=(0, 8))

    def _create_entry(self, parent):
        entry = tk.Entry(
            parent, font=("Segoe UI", 10),
            bg=CARD, fg=TEXT, insertbackground=CYAN,
            relief="flat", borderwidth=0,
        )
        entry.pack(padx=20, ipady=6, fill="x")
        return entry

    def _create_button(self, parent, text, command, color, **pack_kw):
        """Creates a styled button. Pass pack_kw to override default full-width packing."""
        btn = tk.Button(
            parent, text=text, command=command,
            font=("Segoe UI", 9, "bold"),
            bg=color, fg=TEXT,
            activebackground=self._lighten(color), activeforeground=TEXT,
            relief="flat", cursor="hand2", borderwidth=0, pady=7,
        )
        if pack_kw:
            btn.pack(**pack_kw)
        else:
            btn.pack(padx=20, pady=3, fill="x")

        light = self._lighten(color)
        btn.bind("<Enter>", lambda _, b=btn, c=light:  b.configure(bg=c))
        btn.bind("<Leave>", lambda _, b=btn, c=color:  b.configure(bg=c))
        return btn

    @staticmethod
    def _lighten(hex_color, amount=30):
        # Aclara un color hexadecimal sumando 'amount' a cada canal RGB (efecto hover)
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"#{min(255, r+amount):02x}{min(255, g+amount):02x}{min(255, b+amount):02x}"

    def _set_placeholder(self):
        self.output.configure(state="normal", fg=SUBTEXT)
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "  Add vehicles and press 'Run Simulation' to see results here...")

    def _set_status(self, msg, color=SUCCESS):
        self.status_dot.configure(fg=color)
        self.status_label.configure(text=msg)

    def _update_counter(self):
        n = len(self.sistema.vehiculos)
        self.counter_label.configure(
            text=f"Fleet: {n} vehicle{'s' if n != 1 else ''}"
        )

    def _refresh_treeview(self):
        # Borra y reconstruye la tabla con el estado actual de la flota
        self.tree.delete(*self.tree.get_children())
        for v in self.sistema.vehiculos:
            speed = round(v.velocidad_actual, 2) if v.velocidad_actual > 0 else "—"
            self.tree.insert("", "end", values=(TYPE_LABEL[type(v)], v.marca, v.modelo, speed))

    # ------------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------------

    def agregar(self):
        try:
            tipo   = self.tipo_var.get().strip()
            marca  = self.marca.get().strip()
            modelo = self.modelo.get().strip()

            v = self.sistema.agregar_vehiculo(tipo, marca, modelo)

            self._update_counter()
            self._set_status(f"Added: {marca} {modelo}  ({TYPE_LABEL[type(v)]})")
            self._refresh_treeview()
            self.notebook.select(0)

            self.marca.delete(0, tk.END)
            self.modelo.delete(0, tk.END)

        except Exception as e:
            self._set_status(f"Error: {e}", WARNING)
            messagebox.showerror("Error", str(e))

    def eliminar_seleccionado(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a vehicle from the list first.")
            return

        index = self.tree.index(selected[0])
        v = self.sistema.vehiculos[index]
        if messagebox.askyesno("Remove vehicle", f"Remove {v.marca} {v.modelo} from the fleet?"):
            self.sistema.eliminar_vehiculo(index)
            self._update_counter()
            self._refresh_treeview()
            self._set_status(f"Removed: {v.marca} {v.modelo}", WARNING)

    def simular(self):
        if not self.sistema.vehiculos:
            self.output.configure(state="normal", fg=WARNING)
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, "  No vehicles in the fleet. Add at least one vehicle first.")
            self._set_status("Simulation skipped — fleet is empty", WARNING)
            self.notebook.select(1)
            return

        terrain  = self.terrain_var.get().strip()
        turbo    = self.turbo_var.get()
        resultado = self.sistema.simular(turbo=turbo, terrain=terrain)

        self.output.configure(state="normal", fg=CYAN)
        self.output.delete(1.0, tk.END)
        for i, line in enumerate(resultado.split("\n"), 1):
            self.output.insert(tk.END, f"  [{i:02d}]  {line}\n\n")

        self._refresh_treeview()
        self._set_status("Simulation complete — report saved to simulation_report.txt")
        self.notebook.select(1)

    def limpiar(self):
        self._set_placeholder()
        self._set_status("Output cleared")
        self.notebook.select(1)


# -------------------------
# MAIN
# -------------------------

if __name__ == "__main__":
    root = tk.Tk()          # crea la ventana principal de Tkinter
    app = Interfaz(root)    # construye toda la interfaz gráfica
    root.mainloop()         # inicia el bucle de eventos de la GUI
