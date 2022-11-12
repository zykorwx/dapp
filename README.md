# DAPP Prueba técnica

Para ejecutarlo solo se debe teclear

`uvicorn app.main:app --reload`

Se desarrollo y probo usando python3.8

En el archivo requirements.txt están las librerías necesarias para ejecutar el proyecto, para instalarlas ejecuta el siguiente comando:

`pip install -r requirements.txt`

Para ejecutar las pruebas solo se ejecuta:

`pytest`

Se realizo la migración desde: https://github.com/alfaro28/comerciosempleados



Para visualizar la documentación, una vez corriendo el proyecto solo se tiene que entrar al siguiente link,:

http://localhost:8000/docs

o

http://localhost:8000/redoc



Algunos comentarios:

 * Se respeto la estructura de la base de datos, de hecho la base de datos que incluye el proyecto funciona con los datos originales que me se incluían en el repositorio anterior, solo removí las tablas que no se usaban.

* Aunque la documentación de swagger diga lo contrario, todos los errores se retornan de en el formato:

  ```json
  {
  	"rc": -654, // Esto cambia segun el raise o status_code en caso de ser http error
  	"msg": "Mensaje",
  }
  ```
