from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_libros():
    respuesta = client.get("/libros")
    assert respuesta.status_code == 200

def test_post_libro_invalido():
    respuesta = client.post("/libros", json={"titulo": "Incompleto"})
    assert respuesta.status_code == 422

def test_post_libro_valido():
    libro = {
        "titulo": "Test",
        "paginas": 100,
        "editorial": {"nombre": "Test", "pais": "Test"}
    }
    respuesta = client.post("/libros", json=libro)
    assert respuesta.status_code in (200, 201)

def test_post_libro_paginas_invalidas():
    libro = {
        "titulo": "Test2",
        "paginas": 0,
        "editorial": {"nombre": "Test", "pais": "Test"}
    }
    respuesta = client.post("/libros", json=libro)
    assert respuesta.status_code == 422

def test_post_y_luego_get():
    libro = {
        "titulo": "Libro Encadenado",
        "paginas": 200,
        "editorial": {"nombre": "Test", "pais": "Test"}
    }
    client.post("/libros", json=libro)
    respuesta = client.get("/libros")
    titulos = [l["titulo"] for l in respuesta.json()]
    assert "Libro Encadenado" in titulos