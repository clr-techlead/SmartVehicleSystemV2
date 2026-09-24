# Smart Vehicle System

**Autor:** Camilo Andrés León Rubriche
**Institución:** Universidad Nacional Abierta y a Distancia — UNAD
**Curso:** Programación

## Descripción

Sistema que simula distintos tipos de vehículos (auto eléctrico, moto, camión) aplicando conceptos de Programación Orientada a Objetos: herencia, polimorfismo y sobrecarga de métodos. Incluye una interfaz gráfica construida con Tkinter.

## Ejecución

```bash
python Ejercicio_1.py
```

## Características

- Clase base `Vehiculo` con herencia hacia `AutoElectrico`, `Moto` y `Camion`
- Polimorfismo en el método `acelerar()` según el tipo de vehículo
- Interfaz gráfica con tema oscuro (Tkinter + ttk)
- Registro de eventos en `vehicle_log.txt`
- Exportación de resultados de simulación a `simulation_report.txt`
