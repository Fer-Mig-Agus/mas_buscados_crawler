# Mas Buscados de Argentina
---

Se necesita la informacion de los mas buscados de Argentina, para ello se hara uso de la siguiente **[pagina](https://www.dnrec.jus.gov.ar/MasBuscados/  'pagina principal')**


Datos necesarios:

* Genero (gender)
* Apellido (last_name)
* Segundo apellido (second_name)
* Nombre (first_name)
* Segundo nombre (middle_name)
* DNI (id_numer)
* Fecha de Nacimiento (date_of_birth)
* Nacionalidad (nationality)
* Edad (age)


Extraer la mayor informacion posible de cada individuo, en el caso de no contener un dato, directamente colocar N/A.
El proyecto debera de contar con los siguientes archivos

* .env
* .env.example
* .gitignore
* config.py
* crawler.py
* requirements.txt

## Recordar
Usar un entorno virtual, hacer uso de .env si es que  es necesario.

## Informacion Obtenida

La informacion que se obtenga, se debera de guardar en un archivo csv y excel, para ello se puede hacer uso de la libreria pandas.

## Fecha de entrega
El proyecto se debera de entregar hasta el 7/3/25 a las 23:59