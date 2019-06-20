# Estructura de archivos y Script listos para despliegue de Odoo 11 con Docker + módulos extras


### Requisitos

* maquina linux (probado sobre ubuntu 18.04)
* acceso superusuario
* openssh 
* git

### Instalación

Acceder como super usuario preferiblemente

```
sudo su
```

clonar el repositorio dentro de un directorio de su preferencia, por ejempo /home/ubuntu/odoo/

```
git clone https://gitlab.com/rash07/facturaloperu_odoo_base.git
```

acceder a la carpeta del repositorio clonado

```
cd facturaloperu_odoo_base
```

dar permisos de ejecución al archivo install.sh

```
chomd +x install.sh
```

si ejecutará odoo en un puerto específico deberá editar el archivo docker-compose.yml

```
nano docker-compose.yml
```

cerca de la linea 8-9 cambiar el primer número por el que necesite, por ejemplo (8081:8089), por defecto es 8069:8069

```
ports:
      - "8081:8069"
```

guarde los cambios del archivo y confirme el nombre.

Para ejecutar el script debe conocer el paquete que ha adquirido

* Odoo Basic
* Odoo PRO

para el caso de Odoo Basic ejecute

```
./install.sh
```

en el proceso de ejecución se solicitarán las credenciales para los repositorios:

* https://gitlab.com/rash07/facturaloperu_odoo_facturacion
* https://gitlab.com/rash07/facturaloperu_odoo_pos

verifique que se le hayan compartido dichos repositorios, deberá ingresar el correo y contraseña de acceso a gitlab, una vez finalizado el script tendrá Odoo funcionando correctamente en la IP o Dominio bajo el puerto configurado previamente.

Para el paquete PRO el caso es muy similar solamente debe enviar un parametro en la ejecución del script:

```
./install.sh 2
```

con esto se descargarán los modulos de facturación, pos, guías, kardex y demás, de igual manera serán solicitadas las credenciales de cada uno, asi que debe verificar previamente que tiene acceso a cada uno.

### Tareas del script

* Actualizar el sistema operativo
* Instalar las herramientas necesarias (Docker, Curl,entre otras)
* Clonar los repositorios al cual se tenga acceso como miembro
* Configurar los archivos de los contenedores para que los modulos extras sean reconocidos por Odoo
* Iniciar los servicios de base de datos y web para Odoo 11

### Tareas comunes posteriores a la ejecución del script

1. Verificar el acceso

Acceder al dominio o IP, Odoo deberá estar listo con una base de datos precargada, de tener algun error (error 500, 404 o similar) debe reiniciar el servicio con el comando

```
docker restart fp_odoo
```

Si continua con algun error puede ubicar el log de Odoo con el siguiente comando

```
docker logs --tail 60 fp_odoo
```

Puede hacernos llegar el log o enviar el acceso a su instancia para verificar si el problema no es solventado reiniciando el servicio

2. Crear su primera BD 

Eliminar la base de datos actual, esta contiene ya datos precargados sin pero esta en otro idioma y con otras localidades, se recomienda eliminarla y crear una nueva con el idioma y pais adecuado

3. Módulos extras

Si desea agregar módulos extras deberá añadirlos a la carpeta addons, una vez cargados reinicie el servicio y actualice las aplicaciones en Odoo, recuerde estar en modo desarrollador

4. Comandos Docker

El despliegue se realiza con Docker, por lo que necesitará conocer algunos comandos básicos para su mantenimiento.
Puede ver la documentacion aqui https://docs.docker.com


Autor
-----

http://facturaloperu.com

