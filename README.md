# FRIMA

El lenguaje FRIMA es un lenguaje en español que permite declarar variables simples de tipo entero y decimal, así como variables de una y dos dimensiones de los mismos tipos. El lenguaje permite realizar operaciones aritméticas, lógicas y relacionales. Por otro lado, se pueden declarar funciones de tipo entero, decimal y sinregresar (void). Entre sus estatutos permitidos está la asignación de valores a una variable, lectura de una variable, así como la escritura de variables, de constantes y de letreros (strings). Tomando como referencia al lenguaje C++, FRIMA permite ciclos `mientras` (while), `desde hasta` (for), así como condicionales de tipo `si` (if) e `si no` (if else). Por último, permite la manipulación de variables simples así como variable de una y dos dimensiones.

## Equipo FRIMA

Nombre | Matrícula
------------ | -------------
Frida Gutiérrez Mireles | A01039975
María Renée Benavides Puente | A01139495

## Requerimientos para la utilización del lenguaje 
* Tener instalado Python 3
* Tener instalado Flask
* React-Native
* Tener instalado el manejador de paquetes `npm`.

## Instrucciones para correr el compilador (back-end)
1. Dentro del archivo `app.py` correr el comando `flask run`.

## Instrucciones para utilizar la aplicación móvil (front-end)
1. Clonar el código referente al front-end que se encuentra [aquí](https://github.com/fridagtt/FRIMAPP).
1. Dentro del proyecto correr el comando `npm install` para instalar todas las dependencias y librerías necesarias.
2. Correr el comando `expo-cli start --tunnel`.

## Especificaciones de uso del lenguaje FRIMA

### Declaración de variables

Tanto para variables simplres como dimensionales, se permiten los siguientes tipos de datos:
 * entero
 * decimal
 
 ```
renglon decimal -> arr[3];
tabla decimal -> mat[2][3];
variable decimal -> i,j;
variable entero -> m,n;
 ```
 
### Acceder a variables dimensionales
```
arr[0] = 1;
arr[1] = 2;
arr[2] = arr[1] + 1;
mat[0][0] = 3;
mat[0][1] = arr[0];
mat[0][2] = arr[arr[1]];
```
* Se permite sub-indexar arreglos y matrices.

### Declaración de funciones

Los tipos de funcionales permitidas son:
 * entero
 * decimal
 * sinregresar

 ```
 nombreFuncion tipo (tipo param1, tipo param2){
   <Declaración de variables>
   <Estatutos>
 };
 ```
 
### Estatutos
* Asignar
* Llamada a funciones
* Leer
* Imprimir
* Ciclos
* Condicionales

### Asignar
```
variableIzquierda = variableDerecha;

x = 2;
i = 1;
j = i +x;
```

### Llamada a funciones
```
nombreFuncion(param);
```
* La función a llamar tiene que estar declarada en el código.
* Las llamadas pueden llamarse dentro de sí misma, desde otra función o desde el inicio.

### Leer
````
leer(variable);
````
* La variable a leer tiene que estar previamente declarada.
* La lectura de variables occure dentro de la aplicación móvil.

### Imprimir
````
imprimir(variable);
````
* Se pueden imprimir variables, arreglos, matrices, constantes, letreros y resultados de expresiones aritméticas.
* Todo aquello a imprimir será desplegado dentro de la aplicación móvil.

### Ciclos
```
desde (variable = limiteInferior) hasta (limiteSuperior) {
  <Estatutos>
};
```
* La variable a la que se le asigna el limiteInferior debe estar previamente declarada. 
* Repite los estatutos hasta llegar al límite superior.
* Cada vuelta de ciclo la variable condicional brinca de uno en uno.

```
mientras(expresion){
  <Estatutos>
};
```
* Repite los estatutos mientras la expresión sea verdadera.

### Condicionales
```
si(expresion){
  <Estatutos>
};

si(expresión){
  <Estatutos>
}
sino{
  <Estatutos>
};
```
* El resultado de la expresión evaluada en los estatuto de decisión debe ser de tipo booleano.

### Operadores

Los operadores permitidos en el lenguaje FRIMA son:

##### Aritméticos
* Suma (+)
* Resta (-)
* Multiplicación (*)
* División (/)

##### Lógicos
* y
* o

##### Relacionales
* '>'
* '<'
* '=='
* '!='
* '<='
* '>='
