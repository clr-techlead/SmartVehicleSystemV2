"""
Pruebas unitarias para el modelo de dominio de Smart Vehicle System.

Solo se prueban las clases de lógica (Vehiculo, AutoElectrico, Moto, Camion,
SistemaVehiculos) — la interfaz gráfica (Tkinter) queda fuera de las pruebas
automatizadas.
"""
import pytest

from Ejercicio_1 import Vehiculo, AutoElectrico, Moto, Camion, SistemaVehiculos


# ---------------------------------------------------------------------
# Vehiculo (clase base) y polimorfismo en acelerar()
# ---------------------------------------------------------------------

class TestVehiculoBase:

    def test_arranca_detenido(self):
        v = Vehiculo("Toyota", "Corolla")
        assert v.velocidad_actual == 0

    def test_acelerar_incremento_base(self):
        v = Vehiculo("Toyota", "Corolla")
        v.acelerar()
        assert v.velocidad_actual == 10

    def test_acelerar_turbo_duplica_incremento(self):
        v = Vehiculo("Toyota", "Corolla")
        v.acelerar(turbo=True)
        assert v.velocidad_actual == 20

    def test_acelerar_terreno_montana_reduce_incremento(self):
        v = Vehiculo("Toyota", "Corolla")
        v.acelerar(terrain="mountain")
        assert v.velocidad_actual == pytest.approx(7.0)

    def test_acelerar_terreno_autopista_aumenta_incremento(self):
        v = Vehiculo("Toyota", "Corolla")
        v.acelerar(terrain="highway")
        assert v.velocidad_actual == pytest.approx(12.0)

    def test_detener_regresa_a_cero(self):
        v = Vehiculo("Toyota", "Corolla")
        v.acelerar()
        v.detener()
        assert v.velocidad_actual == 0


class TestAutoElectrico:

    def test_bateria_inicial(self):
        auto = AutoElectrico("Tesla", "Model 3")
        assert auto.bateria == 100

    def test_acelerar_consume_bateria(self):
        auto = AutoElectrico("Tesla", "Model 3")
        auto.acelerar()
        assert auto.bateria == 98

    def test_resetear_recarga_bateria_y_velocidad(self):
        auto = AutoElectrico("Tesla", "Model 3")
        auto.acelerar()
        auto.acelerar()
        auto.resetear()
        assert auto.bateria == 100
        assert auto.velocidad_actual == 0

    def test_obtener_informacion_incluye_bateria(self):
        auto = AutoElectrico("Tesla", "Model 3")
        assert "Battery: 100%" in auto.obtener_informacion()


class TestMoto:

    def test_ignora_turbo_y_terreno(self):
        moto = Moto("Yamaha", "MT-07")
        moto.acelerar(turbo=True, terrain="mountain")
        assert moto.velocidad_actual == Moto.INCREMENTO

    def test_detener_es_instantaneo(self):
        moto = Moto("Yamaha", "MT-07")
        moto.acelerar()
        moto.detener()
        assert moto.velocidad_actual == 0


class TestCamion:

    def test_ignora_turbo_y_terreno(self):
        camion = Camion("Volvo", "FH16")
        camion.acelerar(turbo=True, terrain="highway")
        assert camion.velocidad_actual == Camion.INCREMENTO

    def test_frenado_gradual_reduce_a_la_mitad(self):
        camion = Camion("Volvo", "FH16")
        camion.acelerar()
        camion.acelerar()
        velocidad_antes = camion.velocidad_actual
        camion.detener()
        assert camion.velocidad_actual == pytest.approx(velocidad_antes * 0.5)


class TestPolimorfismo:

    def test_cada_tipo_de_vehiculo_acelera_distinto(self):
        """Mismo método, mismos parámetros, resultado distinto según la
        subclase — el núcleo del polimorfismo demostrado en el proyecto."""
        auto = AutoElectrico("Tesla", "Model 3")
        moto = Moto("Yamaha", "MT-07")
        camion = Camion("Volvo", "FH16")

        for v in (auto, moto, camion):
            v.acelerar(turbo=True, terrain="highway")

        assert auto.velocidad_actual == 24  # 10 * 2 * 1.2
        assert moto.velocidad_actual == 15  # incremento fijo, ignora turbo/terreno
        assert camion.velocidad_actual == 5  # incremento fijo, ignora turbo/terreno


# ---------------------------------------------------------------------
# SistemaVehiculos (controlador / flota)
# ---------------------------------------------------------------------

class TestSistemaVehiculos:

    def test_agregar_vehiculo_valido(self):
        sistema = SistemaVehiculos()
        v = sistema.agregar_vehiculo("Electric Car", "Tesla", "Model 3")
        assert len(sistema.vehiculos) == 1
        assert isinstance(v, AutoElectrico)

    def test_agregar_vehiculo_sin_tipo_lanza_error(self):
        sistema = SistemaVehiculos()
        with pytest.raises(ValueError):
            sistema.agregar_vehiculo("", "Tesla", "Model 3")

    def test_agregar_vehiculo_con_campos_vacios_lanza_error(self):
        sistema = SistemaVehiculos()
        with pytest.raises(ValueError):
            sistema.agregar_vehiculo("Motorcycle", "", "MT-07")

    def test_agregar_vehiculo_tipo_invalido_lanza_error(self):
        sistema = SistemaVehiculos()
        with pytest.raises(ValueError):
            sistema.agregar_vehiculo("Spaceship", "Tesla", "Model 3")

    def test_eliminar_vehiculo_por_indice(self):
        sistema = SistemaVehiculos()
        sistema.agregar_vehiculo("Motorcycle", "Yamaha", "MT-07")
        sistema.eliminar_vehiculo(0)
        assert len(sistema.vehiculos) == 0

    def test_eliminar_vehiculo_indice_invalido_no_lanza_error(self):
        sistema = SistemaVehiculos()
        sistema.eliminar_vehiculo(99)  # no debe fallar, solo no hacer nada
        assert len(sistema.vehiculos) == 0

    def test_simular_devuelve_info_de_cada_vehiculo(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)  # aísla la escritura de simulation_report.txt
        sistema = SistemaVehiculos()
        sistema.agregar_vehiculo("Electric Car", "Tesla", "Model 3")
        sistema.agregar_vehiculo("Truck", "Volvo", "FH16")

        resultado = sistema.simular(turbo=True, terrain="highway")

        assert "Tesla Model 3" in resultado
        assert "Volvo FH16" in resultado

    def test_simular_exporta_reporte_a_archivo(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        sistema = SistemaVehiculos()
        sistema.agregar_vehiculo("Motorcycle", "Yamaha", "MT-07")

        sistema.simular()

        reporte = tmp_path / "simulation_report.txt"
        assert reporte.exists()
        assert "Yamaha MT-07" in reporte.read_text()
