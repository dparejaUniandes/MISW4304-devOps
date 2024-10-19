# MISW4304-devOps
Ciclo 7 de la maestría en ingeniería de software asignatura DevOps

# Entrega 1

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

### Ejecución de los tests de postman
Para la ejecución de los tests en postman, se deben realizar los siguientes pasos:
1. En la carpeta Tests, oprimir en los tres puntos y seleccionar la opción "Run folder"
2. Una vez seleccionada esta opción, se listarán todas las peticiones encargadas de ejecutar los tests, debemos fijarnos que todos los checkbox estén seleccionados
3. Oprimir la opción "Run Ciclo 7 DevOps", Ciclo 7 DevOps es el nombre de la colección, si la colección ha cambiado de nombre, posiblemente la opción aparezca "Run nombre_colección"
<img width="1065" alt="image" src="https://github.com/user-attachments/assets/28ff445e-3b14-41d5-9cd2-fd20d1769f80">
4. Al ejecutar todos los tests, se debe validar que se ejecutaron 26 tests, fallaron cero y se omitieron cero como se puede ver a continuación.
<img width="1323" alt="image" src="https://github.com/user-attachments/assets/dc9c8f79-9f45-43e1-9b5c-d90895babddb">
