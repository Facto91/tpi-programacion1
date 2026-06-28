# Gestión de Datos de Países en Python

**Trabajo Práctico Integrador — Programación 1**
Tecnicatura Universitaria en Programación — UTN

---

## Descripción

Aplicación de consola desarrollada en Python 3 que permite gestionar un dataset de países. El sistema lee y escribe datos desde un archivo CSV, y ofrece funcionalidades de búsqueda, filtrado, ordenamiento y estadísticas sobre los datos cargados.

---

## Integrantes

| Nombre | Legajo |
|--------|--------|
| [Nombre Integrante 1] | [Legajo] |
| [Nombre Integrante 2] | [Legajo] |

---

## Requisitos

- Python 3.x
- No requiere librerías externas (solo módulos estándar: `csv`, `os`)

---

## Estructura del proyecto

```
/
├── main.py        # Código fuente principal
├── paises.csv     # Dataset base de países
└── README.md      # Este archivo
```

---

## Cómo ejecutar el programa

1. Clonar o descargar el repositorio.
2. Asegurarse de que `main.py` y `paises.csv` estén en la misma carpeta.
3. Abrir una terminal en esa carpeta y ejecutar:

```bash
python main.py
```

---

## Funcionalidades

| Opción | Descripción |
|--------|-------------|
| 1 | Agregar un nuevo país al dataset |
| 2 | Actualizar población y/o superficie de un país existente |
| 3 | Buscar país por nombre (coincidencia parcial o exacta) |
| 4 | Filtrar países por continente, rango de población o rango de superficie |
| 5 | Ordenar países por nombre, población o superficie (asc/desc) |
| 6 | Mostrar estadísticas generales del dataset |
| 0 | Salir del programa |

---

## Formato del CSV

El archivo `paises.csv` debe respetar el siguiente formato:

```
nombre,poblacion,superficie,continente
Argentina,45376763,2780400,América
Japón,125800000,377975,Asia
```

Campos:
- `nombre`: string
- `poblacion`: entero positivo (habitantes)
- `superficie`: entero positivo (km²)
- `continente`: uno de — América, Europa, Asia, África, Oceanía

---

## Ejemplos de uso

### Agregar un país
```
Ingrese una opción: 1

--- AGREGAR PAÍS ---
Nombre del país: Uruguay
Población: 3518552
Superficie en km²: 176215
Continentes disponibles: América, Europa, Asia, África, Oceanía
Continente: América

País 'Uruguay' agregado correctamente.
Datos guardados correctamente.
```

### Buscar por nombre
```
Ingrese una opción: 3

--- BUSCAR PAÍS POR NOMBRE ---
Ingrese el nombre o parte del nombre a buscar: bra

Se encontraron 1 resultado(s):

Nombre                  Población   Superficie (km²) Continente
----------------------------------------------------------------------
Brasil              213,993,437        8,515,767 América
```

### Filtrar por continente
```
Ingrese una opción: 4

--- FILTRAR POR ---
 1. Continente
 2. Rango de población
 3. Rango de superficie
 0. Volver

Ingrese una opción: 1

--- FILTRAR POR CONTINENTE ---
Continentes disponibles: América, Europa, Asia, África, Oceanía
Ingrese el continente: Europa

Países en Europa (6):

Nombre                  Población   Superficie (km²) Continente
----------------------------------------------------------------------
Alemania             83,149,300          357,022 Europa
Francia              67,391,582          551,695 Europa
...
```

### Estadísticas
```
Ingrese una opción: 6

--- ESTADÍSTICAS ---

Total de países en el dataset:      21

País con MAYOR población:           China (1,439,323,776 hab.)
País con MENOR población:           Australia (25,499,884 hab.)

Promedio de población:              234,485,541 hab.
Promedio de superficie:             3,877,674 km²

Cantidad de países por continente:
------------------------------
  África          3 país/es
  América         6 país/es
  Asia            5 país/es
  Europa          6 país/es
  Oceanía         1 país/es
```

---

## Video demostrativo

[Insertar enlace al video aquí]

## Documentación en PDF

[Insertar enlace al PDF aquí]
