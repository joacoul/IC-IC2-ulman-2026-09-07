# F2 Defensa conceptual de MQTT

**Que es pub/sub?**
Es un modelo de comunicacion asincronico. En lugar de que un cliente pregunte constantemente por un dato (como en una API tradicional), funciona como una radio: un dispositivo "publica" (transmite) un mensaje y cualquiera que este interesado se "suscribe" (sintoniza) para escucharlo. El que publica y el que escucha ni siquiera necesitan conocerse.

**Que es un broker?**
Es el intermediario o el cartero del sistema. Recibe todos los mensajes de los que publican y se encarga de repartirlos a los suscriptores correctos. Gracias al broker, los dispositivos finales no tienen que gestionar conexiones complejas entre ellos.

**Que es un topic?**
Es el canal o la etiqueta que clasifica el mensaje. Se escribe como una ruta (por ejemplo, `casa/cocina/temperatura`). El broker usa los topics para saber a quien tiene que entregarle cada dato.

**Que son los wildcards?**
Son comodines que permiten suscribirse a varios topics al mismo tiempo sin tener que escribirlos uno por uno. 
* El `+` reemplaza un solo nivel (ej: `casa/+/temperatura` lee la temperatura de cualquier ambiente).
* El `#` reemplaza todos los niveles restantes (ej: `casa/cocina/#` lee absolutamente todo lo que pase en la cocina, sin importar el tipo de sensor).

**Por que MQTT sirve mas que el polling para muchos sensores?**
El polling implica preguntar todo el tiempo "¿hay algo nuevo?". Si hay 1000 sensores preguntando cada un segundo, el servidor recibe 1000 consultas por segundo, saturando la red y procesando peticiones incluso cuando los valores no cambiaron. 
Con MQTT (pub/sub), la conexion queda abierta en segundo plano gastando muy poca energia, y el sensor solo manda un mensaje al broker en el milisegundo exacto en que ocurre un evento. Escala infinitamente mejor, ahorra recursos y la respuesta es instantanea.