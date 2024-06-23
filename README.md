# curso_blockchain_uma_24_vuln2
Vulnerabilidad 2 (Pseudoaleatoriedad) (Parte del curso de Extensión
Universitaria en Tecnologías Blockchain de la Universidad de Málaga 2024).

# Principios de aleatoriedad

En general, salvo errores de operación, no existe aleatoriedad dentro de una máquina.
Por eso, las máquinas recurren a fuentes externas (como Internet o sensores) para
obtener entropía.

Esta fuente de entropía permite a la máquina simular un generador de aleatoriedad
seguro por un tiempo y espacio limitados (pseudoaleatoriedad).

# Determinismo en Ethereum, ¿por qué es un problema?

La Ethereum Virtual Machine es una Maquina de Turing Universal determinista.
Además, la blockchain de Ethereum es una base de datos publica, en la que la
información no está cifrada en general.
La blockchain de Ethereum es una MTU determinista distribuida.
Por otra parte, el código fuente de Ethereum es open source.
Además, el código fuente de los contratos es también open source (o se puede debuggear).

Al combinar todo esto obtenemos en suma un comportamiento predecible y conocible
De hecho, esta es una de las fortalezas de Ethereum, pero en este caso también debilidad
ya que estamos tratando de implementar algún tipo de sorteo.

Esto permite al atacante precomputar parámetros adecuados y podría, bajo
determinadas circunstancias, aprovechar esto para obtener NFTs más
fácilmente.

# Descripción General del contrato

El contrato ANormalLottery es un contrato de lotería que simula la distribución de premios utilizando una pseudo-aleatoriedad y actualiza estadísticas de la distribución de premios utilizando el algoritmo en línea de Welford. Los usuarios interactúan con el contrato para generar números pseudo-aleatorios y actualizar sus premios.

## Funciones Principales del Contrato

- generatePseudoRandom: Genera un número pseudo-aleatorio basado en el hash del bloque anterior, la marca de tiempo y la dirección del usuario
- lottery: ejecuta la lotería y actualiza la distribución normal. Si el número aleatorio es menor a 128 y el usuario no está por encima del umbral de la distribución normal, se actualiza el mensaje del usuario a "W" y se incrementa su conteo de premios.
- updateStatistics: Actualiza las estadísticas de la distribución de premios usando el algoritmo en línea de Welford.
- mean: Calcula la media de los premios otorgados.
- variance: Calcula la varianza de los premios otorgados.
- standardDeviation: Calcula la desviación estándar de los premios otorgados.
- readMessage: Devuelve el mensaje asociado a un usuario.
- readNumber: Devuelve el último número aleatorio generado.
- getAwardsCount: Devuelve el conteo de premios de un usuario.
- isAboveThreshold: Verifica si un usuario está por encima del umbral basado en la media y la desviación estándar de los premios.

# Descripción del Script de Pruebas

Este script realiza diversas pruebas para validar la lógica del contrato ANormalLottery, especialmente las estadísticas de premios, usando múltiples usuarios y simulando diversas iteraciones de la función de pseudo-aleatoriedad.
Pasos del Script

- Compilación y Despliegue del Contrato:
    - Compila el contrato ANormalLottery.sol usando solc versión 0.8.13.
    - Despliega el contrato en una blockchain de prueba.
- Transacciones de Prueba:
    - Actualiza y lee mensajes de prueba para validar la funcionalidad básica del contrato.
- Test lotería:
    - Ejecuta la función lottery una vez.
- Pruebas de Lógica Estadística:
    - Ejecuta la función lottery tantas veces como sea necesario hasta obtener un premio.

# Descripción del Proceso de Pruebas

- Compilación y Despliegue: Se compila el contrato y se despliega en una blockchain de prueba usando Web3 y eth_tester.
- Transacciones de Prueba: Se ejecutan transacciones para actualizar y leer mensajes del contrato para asegurar la funcionalidad básica
- Creación y Fondos de Cuentas Aleatorias: Se crean cuentas aleatorias y se transfieren fondos a estas para poder realizar transacciones
- Pruebas de Pseudo-Aleatoriedad: Se ejecuta la función lottery múltiples veces para actualizar estadísticas y verificar la media y la desviación estándar de los premios otorgados.
- Validación de Premios: Se validan los premios para cada cuenta y se imprimen las estadísticas de premios.

# Ejemplo de uso

```
python3 deploy_test.py
```

Ejemplo de salida:
```
Message: W
Random number: 113
Mean: 1, Variance: 0, Standard Deviation: 0
Message: W
Random number: 56
Mean: 1, Variance: 2, Standard Deviation: 1
Message: W
Random number: 116
Mean: 1, Variance: 2, Standard Deviation: 1
Message: Hello Lottery World
Random number: 151
Mean: 1, Variance: 2, Standard Deviation: 1
Message: Hello Lottery World
Random number: 242
Mean: 1, Variance: 2, Standard Deviation: 1
Message: Hello Lottery World
Random number: 239
Mean: 1, Variance: 2, Standard Deviation: 1
```

El threshold de la distribución está configurado a 128.

# Exploit

Se añaden tres funciones, create_random_accounts, exploit_one, y exploit_multiple, para simular el
comportamiento de un atacante.

En este caso, es solo una cuestión semántica puesto que podemos interpretar las diferentes cuentas como creadas por un mismo atacante.
La capacidad del atacante para realizar con éxito esto depende de su propia capacidad de cómputo (para precomputar parámetros correctos) y de la competencia en el mercado via tasas por priorizar sus transacciones. Si muchos usuarios diferentes realizan la lotería honestamente, con números verdaderamente aleatorios y no sesgados, entonces será más dificil para el atacante tener más éxito que sus homólogos. El valor de los premios de la lotería se podría calcular respecto de la media poblacional, que está presente en el contrato.

Se observa cierta resiliencia en el contrato ya que aunque el atacante único, simulado en las líneas
66 a 76 ejecute la lotería muchas veces no consigue mucho mejores resultados (capado por la distribución).

Por ejemplo, esta es la salida para el 'ataque múltiple', con un atacante único realizando 1000 intentos.
```
Address of attacker : 0x75cD7C288Ac12aC71365DF7AA782BAF76519625C, Awards Count: 53
Mean Award Count: 16
Standard Deviation Award Count: 18
Address: 0x75cD7C288Ac12aC71365DF7AA782BAF76519625C, Awards Count: 53
Address: 0xD99Ec4dDff9376C6E56DcB9E33Bb4d7bd7BF1b0F, Awards Count: 49
Address: 0xDA8ad93177afC3cD2563C73697364EBd02F95B4f, Awards Count: 46
Address: 0x8ef796BB4c04215fE22ddBc1c06c8437A54276d9, Awards Count: 44
Address: 0xDf92876374803E819Add54FdBa66eb09AAF75875, Awards Count: 47
Address: 0x2254836c596802327bb0Ccf8A16D04AE518ec3E2, Awards Count: 45
Address: 0x458E68444Ee0314600bF1a87ca6B2E2F48A26Edd, Awards Count: 51
Address: 0x331A576EFD19563fF09366D6914Ed47aaa366a2d, Awards Count: 47
Address: 0xdf5e78d1B47Ca9C505d7f86882b2E46b7C189fF4, Awards Count: 45
Address: 0x92FecECdc1f76C8419Ba094870608393f568b38f, Awards Count: 44
```

Por otro lado, en el caso real habría que tener en cuenta también los otros dos parámetros
(que no añaden seguridad a los efectos de esta PoC) y el vector de ataque
ya que la función es internal y se llama en función de los resultados
de las votaciones de la DAO.

## Análisis estadístico básico

El problema se puede modelar como una distribución binomial:

$$F(k;n,p) = \Pr(X \le k) = \sum_{i=0}^{\lfloor k \rfloor} {n\choose i}p^i(1-p)^{n-i}$$

donde n es el número de intentos y p la probabilidad de éxito.

El script stats.py devuelve las funciones de distribución acumulada (CDF) para
diferentes valores de n y threshold. La probabilidad p se calcula como
p=threshold/256 ya que el tipo de datos utilizado en la función es int8.
Recordemos que la función de densidad es la derivada de la CDF.

Uso:
stats.py 100 10

![plot](./img/n1000_t10.png)

Para n=1000 y t=10 obtendremos entre 16 y 64 éxitos (posibles NFTs).

![plot](./img/n2000_t10.png)

Si aumentamos el número de intentos la curva se desplaza a la derecha.

![plot](./img/n2000_t16.png)

Si aumentamos el threshold la curva se desplaza a la derecha (menos dificil).

## Posible solución, oráculos (Chainlink)

Una posible solución es recurrir a la infraestructura y software de Chainlink.
Entre otros, proporcionan oráculos.

Para instalar las dependencias:<br />
npm install @chainlink/contracts

Para acceder al oráculo Verifiable Random Function (VRF):<br />
import {VRFV2WrapperConsumerBase} from "./node_modules/@chainlink/contracts/src/v0.8/vrf/VRFV2WrapperConsumerBase.sol";<br />
import {LinkTokenInterface} from "./node_modules/@chainlink/contracts/src/v0.8/shared/interfaces/LinkTokenInterface.sol";

Se proporciona un contrato de ejemplo Pseudoaleatoriedad_sol.sol
basado en la documentación de Chainlink, pero simplificado.

Sin embargo, esto solo proporciona solución a la cuestión de la pseudoaleatoriedad
(asumiendo que el oráculo de Chainlink es realmente Random Verifiable).
No proporciona solución al problema de la creación de cuentas.

# TODO

## Comprobar lógica algoritmo en línea de Welford

## Comprobar/implementar aritmética punto flotante