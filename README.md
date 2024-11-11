# MISW4304-devOps
Ciclo 7 de la maestría en ingeniería de software asignatura DevOps

# Entrega 2 - Integración continua con CodeBuild, CodePipeline y Beanstalk

Las consideraciones que se tuvieron en cuenta para la entrega 1 siguen estando vigente, sin embargo, es importante mencionar el proceso que se ha llevado a cabo para la realización de la pruebas unitarias

## Pruebas unitarias
**Nota**: es recomendable la instalación de un ambiente virtual con python, desde la raíz del proyecto se puede utilizar el comando `python -m venv .venv` el cual creará la carpeta .venv en la raíz del proyecto. 

Las pruebas unitarias se pueden ejecutar localmente desde la raíz del proyecto, con el comando `pytest --cov=. -v -s --cov-fail-under=75`, con este comando se ejecutan todas las pruebas unitarias que validan que los flujos de la aplicación brinden la respuesta esperada, además, se especifica que el coverage debe ser superior al 75%, en caso contrario fallará.

### Estructura de capeta y archivos
Desde la raíz del proyecto se puede apreciar la carpeta **tests**, en esta carpeta se incluye el archivo conftest.py que permite la configuración inicial de las pruebas, como la definición de un cliente http y lo que debe ocurrir al finalizar todas las ejecuciones de las pruebas. Por otra parte, como existen dos endpoints, se crean dos archivos de pruebas, uno para agregar un email a la lista negra y otro para obtener el email. Todas las pruebas se ejecutan correctamente y tienen un coverage superior al 90%. En la raíz del proyecto también se incluye el archivo **.coveragerc** que permite omitir los archivos de tests que no deben ser tenidos en cuenta para el coverage. Por último, en el archivo de compilación **buildspec.yml** se incluye el comando antes mencionado para la ejecución de los tests unitarios cuando se realice la compilación en CodeBuild de AWS.

**Coverage** <br>
<img width="975" alt="image" src="https://github.com/user-attachments/assets/5f78c8ac-4669-438f-b2c5-68a486d8c078">


# Entrega 1

La aplicación ha sido desarrollado en python y Flask, para su ejecución, recomendamos configurar y activar un ambiente virtual de python, luego instalar las dependencias con el comando `pip install --no-cache-dir -r requirements.txt`. Vale la pena mencionar que existe un archivo Dockerfile en la raíz del proyecto, este carga la configuración y hace uso de variables de entorno para la conexión a la base de datos postgresql que está localmente, si no se desea ejecutar la aplicación con Docker, desde la raíz del proyecto bastaría ejecutar `python application.py`, de esta menera se tomaría por defecto SQLite y la aplicación funcionaría sin problemas. Cabe aclarar que en AWS Beanstalk no se ejecutó la aplicación contenerizada, en su lugar, se cargó un archivo comprimido para ejecutar la aplicación, el archivo comprimido se encuentra en la raíz del proyecto con el nombre **Archivador.zip**

## Descripción de Endpoints

## Uso
A continuación se especifica cada endpoint con lo necesario para realizar las peticiones http que permitan agregar un correo a la lista negra y consultar si un correo está en la lista negra y la razón por la cual el correo se agregó a la lista negra: <br>

### Agregar correo a la lista negra
Permite agregar un email a la lista negra global de la organización.

<table>
<tr>
<td> Método </td> <td> POST </td>
</tr>
<tr>
<td> Ruta </td> <td> /blacklists </td>
</tr>
<tr>
<td> Parámetros </td> <td> Sin parámetros en la URL </td>
</tr>
<tr>
<td> Encabezados </td> <td> `Authorization: Bearer token` </td>
</tr>
<tr>
<td> Cuerpo </td> <td> 

```json
{
    "email": Correo electrónico a agregar en la blacklist,
    "app_uuid": Identificador de la aplicación en formato UUID,
    "blocked_reason": Razón por la cual se desea bloquear el correo
}
``` 
</td>
</tr>
</table>

<br>

**Respuestas**

<table>
<tr>
<th> Código </th> <th> Descripción </th> <th> Cuerpo </th>
</tr>
<tr>
<td> 401 </td> <td> El token no es válido. </td> <td> {"message": "The token is invalid"} </td>
</tr>
<tr>
<td> 403 </td> <td> El token no está en el encabezado de la solicitud </td> <td> {"message": "The token is required"} </td>
</tr>
<tr>
<td> 400 </td> <td> Cuando no se envía un campo requerido </td> <td> Mensaje campos faltantes: {"message": 'All fields are needed'}</td>
</tr>
<tr>
<td> 500 </td> <td> Error interno que no está contemplado que suceda </td> <td> {"message": 'Internal server error, the account could not be created'}</td>
</tr>
<tr>
<td> 412 </td> <td> Cuando está duplicado el email o el identificador de la app  </td> <td> {"message": mensaje de acuerdo al campo duplicado} </td>
</tr>
<tr>
<td> 201 </td> <td> Se agrega exitosamente el email a la lista negra </td> <td> 

```json
{
    "message": "The account could be created successfully"
}
````
</td>
</tr>
</table>

### Consultar si un email está en la lista negra
Permite saber si un email está en la lista negra global de la organización o no, y el motivo por el que fue agregado a la lista negra.

<table>
<tr>
<td> Método </td> <td> GET </td>
</tr>
<tr>
<td> Ruta </td> <td> /blacklists/<string:email> </td>
</tr>
<tr>
<td> Parámetros </td> <td> email: correo electrónico que se desea consultar </td>
</tr>
<tr>
<td> Encabezados </td> <td> `Authorization: Bearer token` </td>
</tr>
<tr>
<td> Cuerpo </td> <td> N/A </td>
</tr>
</table>

<br>

**Respuestas**

<table>
<tr>
<th> Código </th> <th> Descripción </th> <th> Cuerpo </th>
</tr>
<tr>
<td> 401 </td> <td> El token no es válido. </td> <td> {"message": "The token is invalid"} </td>
</tr>
<tr>
<td> 403 </td> <td> El token no está en el encabezado de la solicitud </td> <td> {"message": "The token is required"} </td>
</tr>
<tr>
<td> 404 </td> <td> El email no ha sido encontrado </td> <td> {"is_email_present": valor booleano que indica que el email no está en la lista negra de la organización} </td>
</tr>
<tr>
<td> 200 </td> <td> El email está presente en la lista negra global de la organización </td> <td> 

```json
{
    "is_email_present": true,
    "reason": Descripción que expresa la justificación por la cual se ha tomado la decisión de bloquear el email
}
````
</td>
</tr>
</table>

## Documentación Postman

En la raíz del proyecto existe el archivo `Ciclo_7_DevOps.postman_collection.json` el cual es una colección de postman, en ella se encuentra la carpeta **Entrega 1**, esta carpeta contiene una carpeta de **Tests** la cual se puede ejecutar para probar todas las respuestas que la aplicación puede brindar, además, posee dos peticiones, una de tipo Post para agregar un email a la lista negra de la organización y otra de tipo Get para consultar si un email está presente en la lista negra. A continuación, se muestra como se ve la estructura mencionada anteriormente desde el postman:

<br>
<img width="328" alt="image" src="https://github.com/user-attachments/assets/7cfb1af0-5f5e-4e83-b96a-e385e0649bcc">
<br>

### Variables de la colección en postman
Para la correcta ejecución de los escenarios de prueba en postman, se han definido las variables EMAIL, APP_UUID, BLOCKED_REASON, TOKEN, GET_EMAIL, la variable HOST es la URL base para realizar las peticiones, en local se puede reemplazar por `http://localhost:5000`, en este momento se encuentra configurado con el dominio de AWS Beanstalk en donde se ejecutó la aplicación: `proyecto-entrega-1-env-1.eba-pzar3z2n.us-east-1.elasticbeanstalk.com/`

<img width="1044" alt="image" src="https://github.com/user-attachments/assets/a84c4772-2a26-4656-886d-08f367bb8d0a">

### Ejecución de los tests de postman
Para la ejecución de los tests en postman, se deben realizar los siguientes pasos:
1. En la carpeta Tests, oprimir en los tres puntos y seleccionar la opción "Run folder"
2. Una vez seleccionada esta opción, se listarán todas las peticiones encargadas de ejecutar los tests, debemos fijarnos que todos los checkbox estén seleccionados
3. Oprimir la opción "Run Ciclo 7 DevOps", Ciclo 7 DevOps es el nombre de la colección, si la colección ha cambiado de nombre, posiblemente la opción aparezca "Run nombre_colección"
<img width="1065" alt="image" src="https://github.com/user-attachments/assets/28ff445e-3b14-41d5-9cd2-fd20d1769f80">
4. Al ejecutar todos los tests, se debe validar que se ejecutaron 26 tests, fallaron cero y se omitieron cero como se puede ver a continuación.
<img width="1323" alt="image" src="https://github.com/user-attachments/assets/dc9c8f79-9f45-43e1-9b5c-d90895babddb">
