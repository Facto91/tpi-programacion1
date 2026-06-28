# ============================================================
# TPI - Gestión de Datos de Países en Python
# Programación 1 - UTN TUP
# ============================================================

import csv
import os

# Nombre del archivo CSV con el dataset
ARCHIVO_CSV = "paises.csv"


def normalizar(texto):
    """Elimina tildes y convierte a minúsculas para comparar texto sin distinción de acentos."""
    import unicodedata
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower()


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def mostrar_menu():
    """Muestra el menú principal de opciones."""
    print("\n" + "=" * 50)
    print("   GESTIÓN DE DATOS DE PAÍSES")
    print("=" * 50)
    print(" 1. Agregar un país")
    print(" 2. Actualizar datos de un país")
    print(" 3. Buscar país por nombre")
    print(" 4. Filtrar países")
    print(" 5. Ordenar países")
    print(" 6. Mostrar estadísticas")
    print(" 0. Salir")
    print("=" * 50)


def mostrar_submenu_filtros():
    """Muestra el submenú de filtros."""
    print("\n--- FILTRAR POR ---")
    print(" 1. Continente")
    print(" 2. Rango de población")
    print(" 3. Rango de superficie")
    print(" 0. Volver")


def mostrar_submenu_ordenamiento():
    """Muestra el submenú de ordenamiento."""
    print("\n--- ORDENAR POR ---")
    print(" 1. Nombre")
    print(" 2. Población")
    print(" 3. Superficie")
    print(" 0. Volver")


# ============================================================
# FUNCIONES DEL SISTEMA
# ============================================================

# Paso 3: lectura/escritura CSV
def cargar_paises():
    """
    Lee el archivo CSV y devuelve una lista de diccionarios con los datos de cada país.
    Cada diccionario tiene las claves: nombre, poblacion, superficie, continente.
    Devuelve una lista vacía si el archivo no existe, o None si hay un error de formato.
    """
    paises = []

    # Verificar si el archivo existe
    if not os.path.exists(ARCHIVO_CSV):
        print(f"Advertencia: no se encontró '{ARCHIVO_CSV}'. Se iniciará con lista vacía.")
        return paises

    try:
        with open(ARCHIVO_CSV, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            # Verificar que el CSV tenga las columnas correctas
            columnas_esperadas = {"nombre", "poblacion", "superficie", "continente"}
            if not columnas_esperadas.issubset(set(lector.fieldnames)):
                print("Error: el archivo CSV no tiene el formato correcto.")
                print(f"Columnas esperadas: {columnas_esperadas}")
                return None

            for numero_fila, fila in enumerate(lector, start=2):
                try:
                    # Verificar que ningún campo esté vacío
                    if not all(fila[col].strip() for col in columnas_esperadas):
                        print(f"Advertencia: fila {numero_fila} tiene campos vacíos y fue omitida.")
                        continue

                    pais = {
                        "nombre": fila["nombre"].strip(),
                        "poblacion": int(fila["poblacion"].strip()),
                        "superficie": int(fila["superficie"].strip()),
                        "continente": fila["continente"].strip()
                    }
                    paises.append(pais)

                except ValueError:
                    print(f"Advertencia: fila {numero_fila} tiene valores numéricos inválidos y fue omitida.")
                    continue

    except Exception as e:
        print(f"Error inesperado al leer el archivo: {e}")
        return None

    return paises


def guardar_paises(paises):
    """
    Guarda la lista de países en el archivo CSV.
    Sobreescribe el contenido existente con los datos actuales.
    """
    try:
        with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as archivo:
            campos = ["nombre", "poblacion", "superficie", "continente"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(paises)
        print("Datos guardados correctamente.")

    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

# Paso 4: agregar/actualizar
def agregar_pais(paises):
    """
    Solicita al usuario los datos de un nuevo país y lo agrega a la lista.
    No se permiten campos vacíos ni valores numéricos inválidos.
    No se permite agregar un país que ya existe (por nombre).
    Devuelve True si el país fue agregado, False si se canceló o hubo error.
    """
    print("\n--- AGREGAR PAÍS ---")

    # Nombre
    while True:
        nombre = input("Nombre del país: ").strip()
        if not nombre:
            print("Error: el nombre no puede estar vacío.")
            continue
        # Verificar si ya existe
        if any(normalizar(p["nombre"]) == normalizar(nombre) for p in paises):
            print(f"Error: ya existe un país con el nombre '{nombre}'.")
            return False
        break

    # Población
    while True:
        valor = input("Población: ").strip()
        if not valor:
            print("Error: la población no puede estar vacía.")
            continue
        try:
            poblacion = int(valor)
            if poblacion <= 0:
                print("Error: la población debe ser un número entero positivo.")
                continue
            break
        except ValueError:
            print("Error: ingrese un número entero válido para la población.")

    # Superficie
    while True:
        valor = input("Superficie en km²: ").strip()
        if not valor:
            print("Error: la superficie no puede estar vacía.")
            continue
        try:
            superficie = int(valor)
            if superficie <= 0:
                print("Error: la superficie debe ser un número entero positivo.")
                continue
            break
        except ValueError:
            print("Error: ingrese un número entero válido para la superficie.")

    # Continente
    continentes_validos = ["América", "Europa", "Asia", "África", "Oceanía"]
    while True:
        print(f"Continentes disponibles: {', '.join(continentes_validos)}")
        continente = input("Continente: ").strip()
        if not continente:
            print("Error: el continente no puede estar vacío.")
            continue
        if continente not in continentes_validos:
            print(f"Error: continente inválido. Debe ser uno de: {', '.join(continentes_validos)}")
            continue
        break

    # Agregar el nuevo país a la lista
    nuevo_pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }
    paises.append(nuevo_pais)
    print(f"\nPaís '{nombre}' agregado correctamente.")
    return True


def actualizar_pais(paises):
    """
    Busca un país por nombre exacto y permite actualizar su población y superficie.
    Devuelve True si se actualizó algo, False si se canceló o no se encontró el país.
    """
    print("\n--- ACTUALIZAR PAÍS ---")

    nombre = input("Ingrese el nombre exacto del país a actualizar: ").strip()
    if not nombre:
        print("Error: debe ingresar un nombre.")
        return False

    # Buscar el país en la lista
    pais_encontrado = None
    for p in paises:
        if normalizar(p["nombre"]) == normalizar(nombre):
            pais_encontrado = p
            break

    if pais_encontrado is None:
        print(f"Error: no se encontró ningún país con el nombre '{nombre}'.")
        return False

    print(f"\nDatos actuales de {pais_encontrado['nombre']}:")
    print(f"  Población : {pais_encontrado['poblacion']:,}")
    print(f"  Superficie: {pais_encontrado['superficie']:,} km²")

    # Nueva población
    while True:
        valor = input("\nNueva población (Enter para mantener el valor actual): ").strip()
        if valor == "":
            break
        try:
            nueva_poblacion = int(valor)
            if nueva_poblacion <= 0:
                print("Error: la población debe ser un número entero positivo.")
                continue
            pais_encontrado["poblacion"] = nueva_poblacion
            break
        except ValueError:
            print("Error: ingrese un número entero válido.")

    # Nueva superficie
    while True:
        valor = input("Nueva superficie en km² (Enter para mantener el valor actual): ").strip()
        if valor == "":
            break
        try:
            nueva_superficie = int(valor)
            if nueva_superficie <= 0:
                print("Error: la superficie debe ser un número entero positivo.")
                continue
            pais_encontrado["superficie"] = nueva_superficie
            break
        except ValueError:
            print("Error: ingrese un número entero válido.")

    print(f"\nDatos de '{pais_encontrado['nombre']}' actualizados correctamente.")
    return True

# Paso 5: búsqueda y filtros
def buscar_pais(paises):
    """
    Busca países por nombre con coincidencia parcial o exacta (sin distinguir mayúsculas).
    Muestra todos los resultados que coincidan.
    """
    print("\n--- BUSCAR PAÍS POR NOMBRE ---")

    termino = input("Ingrese el nombre o parte del nombre a buscar: ").strip()
    if not termino:
        print("Error: debe ingresar un término de búsqueda.")
        return

    resultados = [p for p in paises if normalizar(termino) in normalizar(p["nombre"])]

    if not resultados:
        print(f"No se encontraron países que coincidan con '{termino}'.")
        return

    print(f"\nSe encontraron {len(resultados)} resultado(s):")
    mostrar_tabla(resultados)


def filtrar_paises(paises):
    """
    Muestra el submenú de filtros y ejecuta el filtro seleccionado.
    """
    opcion = input("\nIngrese una opción: ").strip()

    if opcion == "1":
        filtrar_por_continente(paises)
    elif opcion == "2":
        filtrar_por_poblacion(paises)
    elif opcion == "3":
        filtrar_por_superficie(paises)
    elif opcion == "0":
        return
    else:
        print("Opción inválida.")


def filtrar_por_continente(paises):
    """Filtra y muestra los países que pertenecen al continente indicado."""
    print("\n--- FILTRAR POR CONTINENTE ---")

    continentes_validos = ["América", "Europa", "Asia", "África", "Oceanía"]
    print(f"Continentes disponibles: {', '.join(continentes_validos)}")

    continente = input("Ingrese el continente: ").strip()
    if not continente:
        print("Error: debe ingresar un continente.")
        return

    resultados = [p for p in paises if normalizar(p["continente"]) == normalizar(continente)]

    if not resultados:
        print(f"No se encontraron países en el continente '{continente}'.")
        return

    print(f"\nPaíses en {continente} ({len(resultados)}):")
    mostrar_tabla(resultados)


def filtrar_por_poblacion(paises):
    """Filtra y muestra los países cuya población está dentro del rango indicado."""
    print("\n--- FILTRAR POR RANGO DE POBLACIÓN ---")

    while True:
        valor = input("Población mínima: ").strip()
        if not valor:
            print("Error: debe ingresar un valor.")
            continue
        try:
            minimo = int(valor)
            if minimo < 0:
                print("Error: el valor mínimo no puede ser negativo.")
                continue
            break
        except ValueError:
            print("Error: ingrese un número entero válido.")

    while True:
        valor = input("Población máxima: ").strip()
        if not valor:
            print("Error: debe ingresar un valor.")
            continue
        try:
            maximo = int(valor)
            if maximo < minimo:
                print("Error: el máximo debe ser mayor o igual al mínimo.")
                continue
            break
        except ValueError:
            print("Error: ingrese un número entero válido.")

    resultados = [p for p in paises if minimo <= p["poblacion"] <= maximo]

    if not resultados:
        print(f"No se encontraron países con población entre {minimo:,} y {maximo:,}.")
        return

    print(f"\nPaíses con población entre {minimo:,} y {maximo:,} ({len(resultados)}):")
    mostrar_tabla(resultados)


def filtrar_por_superficie(paises):
    """Filtra y muestra los países cuya superficie está dentro del rango indicado."""
    print("\n--- FILTRAR POR RANGO DE SUPERFICIE ---")

    while True:
        valor = input("Superficie mínima (km²): ").strip()
        if not valor:
            print("Error: debe ingresar un valor.")
            continue
        try:
            minimo = int(valor)
            if minimo < 0:
                print("Error: el valor mínimo no puede ser negativo.")
                continue
            break
        except ValueError:
            print("Error: ingrese un número entero válido.")

    while True:
        valor = input("Superficie máxima (km²): ").strip()
        if not valor:
            print("Error: debe ingresar un valor.")
            continue
        try:
            maximo = int(valor)
            if maximo < minimo:
                print("Error: el máximo debe ser mayor o igual al mínimo.")
                continue
            break
        except ValueError:
            print("Error: ingrese un número entero válido.")

    resultados = [p for p in paises if minimo <= p["superficie"] <= maximo]

    if not resultados:
        print(f"No se encontraron países con superficie entre {minimo:,} y {maximo:,} km².")
        return

    print(f"\nPaíses con superficie entre {minimo:,} y {maximo:,} km² ({len(resultados)}):")
    mostrar_tabla(resultados)


def mostrar_tabla(paises):
    """
    Muestra una lista de países en formato de tabla en consola.
    """
    print(f"\n{'Nombre':<20} {'Población':>15} {'Superficie (km²)':>18} {'Continente':<12}")
    print("-" * 70)
    for p in paises:
        print(f"{p['nombre']:<20} {p['poblacion']:>15,} {p['superficie']:>18,} {p['continente']:<12}")

# Paso 6: ordenamiento
def ordenar_paises(paises):
    """
    Muestra el submenú de ordenamiento, solicita criterio y dirección,
    y muestra la lista de países ordenada.
    """
    opcion = input("\nIngrese una opción: ").strip()

    if opcion == "0":
        return

    if opcion not in ("1", "2", "3"):
        print("Opción inválida.")
        return

    # Determinar el campo de ordenamiento
    if opcion == "1":
        campo = "nombre"
        etiqueta = "Nombre"
    elif opcion == "2":
        campo = "poblacion"
        etiqueta = "Población"
    else:
        campo = "superficie"
        etiqueta = "Superficie"

    # Dirección de ordenamiento (solo para población y superficie)
    if opcion in ("2", "3"):
        print("\n--- DIRECCIÓN ---")
        print(" 1. Ascendente")
        print(" 2. Descendente")
        direccion = input("Ingrese una opción: ").strip()
        if direccion not in ("1", "2"):
            print("Opción inválida. Se usará ascendente por defecto.")
            direccion = "1"
        descendente = direccion == "2"
        etiqueta_dir = "descendente" if descendente else "ascendente"
    else:
        # El nombre siempre se ordena ascendente (A-Z)
        descendente = False
        etiqueta_dir = "A-Z"

    # Ordenar usando sorted() sin modificar la lista original
    paises_ordenados = sorted(paises, key=lambda p: p[campo], reverse=descendente)

    print(f"\nPaíses ordenados por {etiqueta} ({etiqueta_dir}):")
    mostrar_tabla(paises_ordenados)

# Paso 7: estadísticas
def mostrar_estadisticas(paises):
    """
    Calcula y muestra las estadísticas principales del dataset:
    - País con mayor y menor población
    - Promedio de población
    - Promedio de superficie
    - Cantidad de países por continente
    """
    print("\n--- ESTADÍSTICAS ---")

    if not paises:
        print("No hay países cargados para calcular estadísticas.")
        return

    # País con mayor y menor población
    pais_mayor_pob = max(paises, key=lambda p: p["poblacion"])
    pais_menor_pob = min(paises, key=lambda p: p["poblacion"])

    # Promedio de población y superficie
    promedio_poblacion = sum(p["poblacion"] for p in paises) / len(paises)
    promedio_superficie = sum(p["superficie"] for p in paises) / len(paises)

    # Cantidad de países por continente
    paises_por_continente = {}
    for p in paises:
        continente = p["continente"]
        if continente in paises_por_continente:
            paises_por_continente[continente] += 1
        else:
            paises_por_continente[continente] = 1

    # Mostrar resultados
    print(f"\n{'Total de países en el dataset:':<35} {len(paises)}")

    print(f"\n{'País con MAYOR población:':<35} {pais_mayor_pob['nombre']} ({pais_mayor_pob['poblacion']:,} hab.)")
    print(f"{'País con MENOR población:':<35} {pais_menor_pob['nombre']} ({pais_menor_pob['poblacion']:,} hab.)")

    print(f"\n{'Promedio de población:':<35} {promedio_poblacion:,.0f} hab.")
    print(f"{'Promedio de superficie:':<35} {promedio_superficie:,.0f} km²")

    print("\nCantidad de países por continente:")
    print("-" * 30)
    for continente, cantidad in sorted(paises_por_continente.items()):
        print(f"  {continente:<15} {cantidad} país/es")


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():
    """Función principal que ejecuta el programa."""
    print("\nCargando datos...")
    paises = cargar_paises()

    if paises is None:
        print("Error al cargar el archivo CSV. Verifique que existe el archivo:", ARCHIVO_CSV)
        return

    print(f"Se cargaron {len(paises)} países correctamente.")

    while True:
        mostrar_menu()
        opcion = input("\nIngrese una opción: ").strip()

        if opcion == "1":
            if agregar_pais(paises):
                guardar_paises(paises)

        elif opcion == "2":
            if actualizar_pais(paises):
                guardar_paises(paises)

        elif opcion == "3":
            buscar_pais(paises)

        elif opcion == "4":
            mostrar_submenu_filtros()
            filtrar_paises(paises)

        elif opcion == "5":
            mostrar_submenu_ordenamiento()
            ordenar_paises(paises)

        elif opcion == "6":
            mostrar_estadisticas(paises)

        elif opcion == "0":
            print("\nSaliendo del programa. ¡Hasta luego!")
            break

        else:
            print("\nOpción inválida. Por favor ingrese un número del menú.")


# ============================================================
# PUNTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    main()
