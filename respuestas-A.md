# Parte A - Respuestas

## A1 - Verbo correcto

(a) ver la lista de libros: GET, se usa para leer sin modificar.
(b) agregar un libro nuevo: POST, porque se crea un dato nuevo.
(c) borrar un libro: DELETE, se usa para borrar.
(d) cambiarle el precio a un libro: PATCH, porque se cambia solo un campo del libro.
(e) reemplazar un libro entero por otro: PUT, porque permite reemplazar un elemento por completo.
(f) cambiarle solo la disponibilidad, sin tocar el resto: PATCH, ya que modificamos solo un campo.

## A2 - Leer codigos de estado


200: Salio bien. Ejemplo: GET a /libros devuelve la lista con exito
201: Se creo algo. Ejemplo: POST a /libros guarda un libro nuevo correctamente.  
204: Todo bien, pero no hay nada que devolver. Ejemplo: DELETE a /libros/{titulo} borra el libro exitosamente.  
400: Pedido mal formado. Ejemplo: Mandar un POST con un formato que ni siquiera es un JSON valido.  
404: No encontrado. Ejemplo: GET a un titulo de libro que no existe.  405: Metodo no permitido. Ejemplo: Intentar un DELETE directamente a /libros, ruta que solo acepta GET o POST.  
422: Entidad no procesable. Ejemplo: POST a /libros donde falta el campo paginas o se envia texto en lugar de un numero.  
500: Error del servidor. Ejemplo: La API falla internamente al intentar guardar un dato debido a un error en el codigo

## A3 - Familias de codigos
Los codigos 2xx indican que la operacion salio bien, los 3xx senialan una redireccion hacia otro lugar, los 4xx marcan que el cliente se equivoco en su pedido, y los 5xx avisan que el servidor fallo internamente.

## A4 -
### A4.1
{ "titulo": "1984", "autor": "George Orwell", "paginas": 328, "disponible": true }

### A4.2
[
  { "titulo": "1984", "autor": "George Orwell", "paginas": 328, "disponible": true },
  { "titulo": "Fahrenheit 451", "autor": "Ray Bradbury", "paginas": 256, "disponible": false }
]

### A4.3
{
  "titulo": "Dune",
  "autor": "Frank Herbert",
  "paginas": 412,
  "disponible": true,
  "editorial": { "nombre": "Chilton Books", "pais": "Estados Unidos" }
}

## A5 -
Idempotentes (GET, PUT, DELETE): Hacer el pedido una o cien veces seguidas deja siempre el mismo resultado (ej. PUT siempre reemplaza por lo mismo).  
No idempotentes (POST): Si se manda un POST de "crear libro" dos veces seguidas por un problema de red, el sistema va a crear dos libros distintos (datos duplicados)

## A6 -
El header Content-Type: application/json le indica al servidor exactamente como debe interpretar el cuerpo del pedido. Si un cliente manda el body sin este header, el servidor podria no entender los datos, incluso si el JSON esta perfectamente escrito.

## A7 -
Listar todos los libros: GET /libros
Ver un libro puntual: GET /libros/{titulo}
Listar los libros de un autor puntual: GET /autores/{nombre}/libros
Crear un autor: POST /autores