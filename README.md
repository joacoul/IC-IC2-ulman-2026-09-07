# IC-IC2-ulman-2026-09-07

Ejercicios de la Clase 2 — Ingeniería en Computación 2. API de libros con FastAPI, cliente con `requests`, y tests con `pytest`/`TestClient`.

## Cómo levantar el proyecto

1. Crear y activar el entorno virtual:
```bash
   python -m venv .venv
   source .venv/Scripts/activate
```
2. Instalar dependencias:
```bash
   pip install -r requirements.txt
```
3. Levantar la API:
```bash
   uvicorn main:app --reload
```
4. Documentación interactiva: `http://127.0.0.1:8000/docs`

## Cómo correr el cliente

Con la API levantada en otra terminal:
```bash
python cliente.py
```

## Cómo correr los tests

```bash
pytest
```

## F3 — Errores de contrato

### 422 — Validación fallida en la API
Un POST con el body `{"titulo":"Incompleto"}` (sin `paginas` ni `editorial`) devolvió:
```json
{"detail":[{"type":"missing","loc":["body","paginas"],"msg":"Field required","input":{"titulo":"Incompleto"}},{"type":"missing","loc":["body","editorial"],"msg":"Field required","input":{"titulo":"Incompleto"}}]}
```
FastAPI detecta y lista **todos** los campos faltantes en una sola respuesta, no solo el primero.

### 404 — Recurso no encontrado desde el cliente
Al pedir `GET /libros/NoExiste` (un título que no existe), la API respondió:
```
HTTP/1.1 404 Not Found
{"detail":"Libro no encontrado"}
```

### ConnectionError — API apagada
Con uvicorn apagado, el cliente lanzó `requests.exceptions.ConnectionError`, causado por un `ConnectionRefusedError` — el sistema operativo rechazó la conexión porque no había nada escuchando en el puerto 8000.

## F4 — /docs vs. curl

Probé GET, POST válido y POST inválido en ambas herramientas, con resultados idénticos en status code y body.

**Similitud:** ambas hablan HTTP puro contra la misma API — el servidor no distingue si el pedido vino de `/docs` o de `curl`, el contrato es el mismo.
**Diferencia:** `/docs` arma el JSON con un formulario visual y te muestra la respuesta ya formateada; con `curl` hay que escribir el JSON a mano con `-d` y el header `-H "Content-Type: application/json"` explícito, pero es scriptable (se puede meter en un archivo `.sh` y repetirlo).
**Cuándo usaría cada uno:** `/docs` para explorar y probar rápido mientras desarrollo; `curl` (o una colección de Postman) para dejar un flujo documentado y repetible, o para automatizar pruebas desde una terminal sin abrir el navegador.