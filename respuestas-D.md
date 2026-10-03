# Parte D MQTT, solo el concepto

### D1 Ver el mensaje viajar
Al realizar la prueba en el broker publico, se observa que el mensaje viaja casi instantaneamente. Al publicar desde la terminal A hacia el topic `unraf/demo/saludo`, la terminal B (que estaba suscrita a ese mismo topic) recibe y muestra el mensaje inmediatamente. 

### D2 Publicar sin suscriptores
Si se publica en un topic sin haber suscriptores, no ocurre ningun error visible en el publicador, pero el mensaje se pierde en el vacio. Al suscribirse despues de que el mensaje fue enviado, no se recibe nada. Sin embargo, al publicar de nuevo habiendo una suscripcion activa, el mensaje si llega.
**Conclusion:** En MQTT, el publicador esta totalmente desacoplado; no sabe ni importa si hay 0, 1 o 1000 clientes escuchando. Por defecto, los mensajes publicados sin suscriptores activos se descartan.

### D3 Pub/sub vs request/response
**Diferencias:**
*   **Request/Response (HTTP/API):** Es sincronico y acoplado. El cliente pide un dato especifico al servidor, espera, y el servidor responde directamente.
*   **Pub/Sub (MQTT):** Es asincronico y desacoplado. El cliente publica un dato al *broker* y este lo reparte a quienes hayan avisado previamente que les interesa, sin que el publicador y los suscriptores se conozcan.

**Ejemplos:**
*   *Cuando usar Request/Response:* Para iniciar sesion en una app. Se envia usuario/contrasenia y se espera un "OK" o "Error" en ese mismo momento.
*   *Cuando usar Pub/Sub:* Para un chat en vivo o una red de sensores de temperatura. Los datos fluyen constantemente a todos los interesados sin que tengan que preguntar continuamente.

### D4 Topics y jerarquia
Para recibir todo lo de la cocina, la suscripcion deberia ser: `casa/cocina/#` (o tambien sirve `casa/cocina/+` si los sensores solo tienen un nivel mas).

**Wildcards de MQTT:**
*   **`+` (Un solo nivel):** Reemplaza un unico nivel en la jerarquia. Por ejemplo, `casa/+/temp` capta la temperatura de la cocina, del banio y del patio, pero ignora la humedad.
*   **`#` (Multiples niveles):** Reemplaza todos los niveles restantes (debe ir al final). Por ejemplo, `casa/cocina/#` capta `casa/cocina/temp`, `casa/cocina/hum`, e incluso `casa/cocina/heladera/puerta`.

### D5 Disenia tus topics
**Esquema propuesto:**
Se utiliza el esquema `hogar/<ambiente>/<tipo_sensor>`

*Ambientes:* `cocina`, `living`, `dormitorio`
*Sensores:* `temperatura`, `movimiento`

Ejemplos de topics de publicacion: `hogar/cocina/temperatura`, `hogar/living/movimiento`.

**Justificacion y uso de wildcards:**
Esta jerarquia (de general a especifico) permite cumplir con todos los requisitos:
1.  **Suscribirse a todo:** `hogar/#` (Atrapa absolutamente todo lo que pase en la casa).
2.  **Suscribirse a un ambiente:** `hogar/living/#` (Atrapa temperatura y movimiento, pero solo del living).
3.  **Suscribirse a un tipo de sensor:** `hogar/+/temperatura` (Atrapa la temperatura de los 3 ambientes, ignorando los sensores de movimiento).

### D6 QoS, la idea
*   **QoS 0 ("At most once"):** El mensaje se envia y no se espera confirmacion. Si se pierde, se perdio.
*   **QoS 1 ("At least once"):** Se garantiza que llega, pero si la confirmacion de recepcion falla, se reenvia, por lo que podria llegar duplicado.
*   **QoS 2 ("Exactly once"):** Utiliza un sistema de 4 pasos para garantizar que llegue una sola vez, sin duplicados ni perdidas. Es el mas lento pero el mas seguro.

**Casos de uso:**
*   *Sensor de temperatura (cada 2 seg):* Se usaria **QoS 0**. Si se pierde un mensaje en la red, no es critico porque en 2 segundos llega el valor actualizado. No justifica el sobrecargo de red para confirmar entregas.
*   *Comando "Abrir la puerta":* Se usaria **QoS 2** (o al menos QoS 1). Es una accion critica puntual. Si el mensaje se pierde, la puerta no se abre. No es tolerable perderlo.

### D7 Mensajes retenidos (retained)
Un mensaje "retained" es aquel que el *broker* decide guardar (retener) como el "ultimo valor conocido" para ese topic. 
*   **Diferencia con D2:** En D2 se vio que al suscribirse tarde, el mensaje se pierde. Si el mensaje se publica con la bandera `retained = true`, el broker lo guarda. Al suscribirse mas tarde, el broker envia inmediatamente ese ultimo mensaje retenido.
*   **Quien se beneficia:** Una aplicacion de celular o un dashboard de monitoreo. Al abrir la app, no es necesario esperar a que el sensor vuelva a publicar para conocer el estado actual; gracias al mensaje retenido, el ultimo estado conocido esta disponible al instante.

### D8 MQTT vs. preguntar todo el tiempo (polling)
**Comparacion:**
El modelo *polling* (request/response repetitivo) requiere que el cliente inicie una conexion constante. Pub/Sub (MQTT) mantiene una conexion abierta de bajo consumo y el servidor notifica solo cuando hay novedades (Push).

**Carga del servidor y tiempos (Ejemplo numerico):**
*   **Polling (1000 sensores cada 1 seg):** El servidor de la API recibe 1000 peticiones HTTP por segundo (86.4 millones al dia), incluso si la temperatura no cambio en horas. Esto consume mucha CPU, ancho de banda y bateria. Ademas, si algo ocurre en el milisegundo 1, el cliente recien se entera en el segundo 1 (cuando vuelve a preguntar).
*   **Pub/Sub (1000 sensores):** Los sensores solo mandan un mensaje si cambia el valor o en intervalos largos. Si ocurre un evento, el sensor publica inmediatamente. El evento llega al suscriptor en escasos milisegundos. El servidor pasa de procesar 1000 requests/segundo a estar inactivo casi todo el tiempo, reaccionando instantaneamente solo ante eventos reales. Pub/sub escala infinitamente mejor.