import base64
import sys
from typing import List
from argparse import ArgumentParser, Namespace

import requests


def parse_args(args: List[str]) -> Namespace:
    parser = ArgumentParser(description="Gestor de tareas CLI")
    parser.add_argument("-u", "--username", type=str, required=False)
    parser.add_argument("-p", "--password", type=str, required=False)
    return parser.parse_args(args)


def get_auth_header(username: str, password: str) -> str:
    encoded_auth_string = f"{username}:{password}".encode("ascii")
    b64_auth_string = base64.b64encode(encoded_auth_string)
    return f"Basic {b64_auth_string.decode('ascii')}"


def get_httpbin_auth(username: str, password: str) -> bool:
    endpoint = f"https://httpbin.org/basic-auth/{username}/{password}"
    headers = {
        "Accept": "application/json",
        "Authorization": get_auth_header(username, password),
    }
    response = requests.get(endpoint, headers=headers)
    return response.ok


def autenticar(user_cli: str, pass_cli: str) -> bool:
    intentos = 0
    max_intentos = 3

    while intentos < max_intentos:
        if intentos == 0 and user_cli and pass_cli:
            username = user_cli
            password = pass_cli
        else:
            username = input("Ingrese su nombre de usuario: ").strip()
            password = input("Ingrese su contraseña: ").strip()

        intentos += 1

        if username and password and get_httpbin_auth(username, password):
            print("Autenticación exitosa.")
            return True

        print(f"Error: Credenciales incorrectas. Intento {intentos} de {max_intentos}.")

    print("Error: Se ha superado el máximo de intentos. Acceso denegado.")
    return False


def agregar_tarea(tareas: List[dict]) -> None:
    titulo = input("Ingrese el título de la tarea: ").strip()
    if titulo:
        tareas.append({"titulo": titulo, "estado": "pendiente"})
        print(f"Tarea '{titulo}' agregada.")
    else:
        print("Error: El título de la tarea no puede estar vacío.")


def listar_tareas(tareas: List[dict]) -> None:
    if not tareas:
        print("No hay tareas registradas.")
        return

    for i, tarea in enumerate(tareas, start=1):
        print(f"{i}. {tarea['titulo']} [{tarea['estado']}]")


def eliminar_tarea(tareas: List[dict]) -> None:
    titulo = input("Ingrese el título de la tarea a eliminar: ").strip()
    for tarea in tareas:
        if tarea["titulo"] == titulo:
            tareas.remove(tarea)
            print(f"Tarea '{titulo}' eliminada.")
            return

    print(f"Error: No existe ninguna tarea con el título '{titulo}'.")


def menu_tareas() -> None:
    tareas: List[dict] = []

    while True:
        print("\n--- Menú de Gestión de Tareas ---")
        print("1. Agregar tarea")
        print("2. Listar tareas")
        print("3. Eliminar tarea")
        print("4. Salir")

        opcion = input("Elija una opción (1-4): ").strip()

        if opcion == "1":
            agregar_tarea(tareas)
        elif opcion == "2":
            listar_tareas(tareas)
        elif opcion == "3":
            eliminar_tarea(tareas)
        elif opcion == "4":
            print("Saliendo del programa.")
            break
        else:
            print("Error: Opción no válida. Elija un número del 1 al 4.")


def main(args: List[str]) -> None:
    parsed_args = parse_args(args)
    if autenticar(parsed_args.username, parsed_args.password):
        menu_tareas()


if __name__ == "__main__":
    main(sys.argv[1:])
