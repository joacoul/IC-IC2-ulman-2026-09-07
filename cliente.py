import requests

BASE_URL = "http://127.0.0.1:8000"

def listar_libros():
    respuesta = requests.get(f"{BASE_URL}/libros")
    print(respuesta.json())

def crear_libro():
    libro_nuevo = {
        "titulo": "Rayuela",
        "paginas": 600,
        "editorial": {"nombre": "Sudamericana", "pais": "Argentina"},
        "disponible": True
    }
    respuesta = requests.post(f"{BASE_URL}/libros", json=libro_nuevo)
    print(respuesta.status_code)
    print(respuesta.json())

def crear_libro_con_chequeo(libro):
    respuesta = requests.post(f"{BASE_URL}/libros", json=libro)
    if respuesta.status_code in (200, 201):
        print("ok")
    elif respuesta.status_code == 422:
        print("dato inválido")
    elif respuesta.status_code == 404:
        print("no existe")
    else:
        print(f"algo raro: {respuesta.status_code}")

def actualizar_libro(titulo_viejo, libro_nuevo):
    respuesta = requests.put(f"{BASE_URL}/libros/{titulo_viejo}", json=libro_nuevo)
    print(respuesta.status_code)
    print(respuesta.json())

def borrar_libro(titulo):
    respuesta = requests.delete(f"{BASE_URL}/libros/{titulo}")
    print(respuesta.status_code)

def listar_libros_seguro():
    try:
        respuesta = requests.get(f"{BASE_URL}/libros")
        print(respuesta.json())
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar con la API")

def probar_timeout():
    try:
        requests.get("http://10.255.255.1/", timeout=1)
    except requests.exceptions.Timeout:
        print("El pedido tardo demasiado, se cancelo")

sesion = requests.Session()

def listar_libros_con_sesion():
    respuesta = sesion.get(f"{BASE_URL}/libros")
    print(respuesta.json())

if __name__ == "__main__":
    crear_libro_con_chequeo({"titulo": "Test", "paginas": 0, "editorial": {"nombre": "x", "pais": "x"}})
    crear_libro()
    borrar_libro("Rayuela")
    listar_libros()
    listar_libros_seguro()
    listar_libros_con_sesion()
    probar_timeout()