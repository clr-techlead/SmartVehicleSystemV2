🌐 English | [Versión en español](README.es.md)

# 🚗 Smart Vehicle System

![Tests](https://github.com/clr-techlead/SmartVehicleSystemV2/actions/workflows/tests.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)

**Author:** Camilo Andrés León Rubriche
**Institution:** Universidad Nacional Abierta y a Distancia — UNAD
**Course:** Programming

> Vehicle fleet simulator with a graphical interface, built in Python applying inheritance, polymorphism, and method overloading.

## Overview

A system that simulates different types of vehicles (electric car, motorcycle, truck) applying Object-Oriented Programming concepts: inheritance, polymorphism, and method overloading. It includes a Tkinter GUI where a fleet is built and an acceleration simulation is run based on terrain and turbo mode.

## Screenshots

| Simulation output | Fleet table |
|---|---|
| ![Simulation output with speed and battery](docs/screenshots/01_simulation_output.png) | ![Fleet table with type, brand, model, and speed](docs/screenshots/02_fleet_table.png) |

## Running it

```bash
python Ejercicio_1.py
```

Requirements: Python 3.10+ (uses only the standard library — `tkinter`, `logging`).

## Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

23 unit tests cover the base `Vehiculo` class, each subclass (`AutoElectrico`, `Moto`, `Camion`), polymorphism in `acelerar()`, and the `SistemaVehiculos` controller (add/remove/simulate fleet). They run automatically on every push via GitHub Actions (see badge above).

## Features

- Base class `Vehiculo` with inheritance to `AutoElectrico`, `Moto`, and `Camion`
- Polymorphism in the `acelerar()` (accelerate) method depending on vehicle type
- Simulated overloading of `acelerar()` via optional parameters (`turbo`, `terrain`)
- Dark-themed GUI (Tkinter + ttk)
- Event logging to `vehicle_log.txt`
- Simulation results exported to `simulation_report.txt`

## Architecture

```
SmartVehicleSystemV2/
│
├── Ejercicio_1.py             # Full application: models, inheritance/polymorphism, and UI (Tkinter)
├── tests/
│   └── test_vehiculos.py       # Unit tests (pytest)
├── .github/workflows/
│   └── tests.yml                # CI: runs the tests on every push
├── requirements.txt
├── LICENSE
├── vehicle_log.txt               # Event log (generated at runtime)
└── simulation_report.txt          # Latest simulation report (generated at runtime)
```

## Technologies

- Python 3
- tkinter / ttk — GUI
- logging — event logging
