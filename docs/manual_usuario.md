Manual de uso
=============

## Introducción

## Procedimientos

### Crear un nuevo proyecto y configurarlo

* Crea un directorio donde se guadarán la contabilidad (por ejemplo "mis_datos_hacienda") y copia en él el directorio ".gesto-prof" que está en "plantillas".  
* Abre el fichero "settings.yaml" que está dentro de ".gesto-prof" en tu directory para indicar al sw donde vas a guardar tu BD. La ruta de directorio que se escribe es relativa a donde está ".gesto-prof." 
* Copia el directorio "bd" de "plantillas" donde quieres dentro del directorio donde has pegado ".gesto-prof", pueden estar al mismo nivel (por ejemplo dentro de "mis_datos_hacienda/contabilidad") o en un subdirectorio (por ejemplo "mis_datos_hacienda/2021/contabilidad").
* En la tabla "info_empresa.csv" que está dentro de "bd" es donde se guardan tus datos de autónomo, por lo que tienes que modificarla y añadir al menos tu nombre y el NIF.
* Limpia todas las otras tablas de la BD para añadir más adelante la información.
* Una vez hecho lo anterior ya puedes usar el software, tienes que llamar al script "gp-cli.py" estando dentro del directorio del proyecto. Es decir: 
    ```console  
    .../mis_datos_hacienda$ python gp-cli.py make_report
    ```

### Añadir un nuevo cliente

* Edita el fichero "clientes.csv" de la BD y añade la información. El campo "Número de cliente" es obligatoria.

### Añadir un nuevo proveedor

* Edita el fichero "proveedores.csv" de la BD y añade la información. El campo "Número de proveedor" es obligatoria.

### Crear facturas emitidas (ingresos) en un trimestre a partir de la información recibida de Classgap

* Copiar los fichero de clases finalizadas proporcionados por ClassGap en el directorio 'ingresos' de un periodo (T1, T2, T3 o T4). 
* Crear un único fichero ODT a partir de todos los ficheros de classes finalizadas proporcionados por ClassGap. Revisa las fechas de ambos ficheros ya que pueden usar diferentes formatos lo que poduce errores durante el post-proceso.
* Añadir una columna con los números de cliente (CxxZ).
* Remplazar la cabeza del fichero ODT con la que está definida en el fichero patrón "nuevos_ingresos_classgap.template.csv" .
* Guardar el fichero como "clases_finalizadas_totales.csv", en formato CSV. El separador usado tiene que ser ";" y el símbolo decimal ".". Cambia los formatos a "YYYY-MM-DD" para las fechas y "XX.XX" para porcentajes y euros.
* Calcular el precio a poner en la factura emitida a cada estudiante usando el script "preparar_facturas_emitidas.py". Este script escribe un fichero CSV en "/resultados" llamado "facturas_emitidas_totales.csv".
* El fichero final tiene que seguir el formato de "nuevas_facturas_emitidas.template.csv".

### Crear facturas recibidas (gastos) en un trimestre

* 

### Generar las facturas simplificadas emitidas

* Ejecutar el script "gp-scli.py make_invoices". Las facturas emitidas se generan a partir del fichero de facturas emitidas que sigue el formato "facturas_recibidas.template.csv".

### Actualizar la base de datos con los ficheros de facturas de un trimestre

* Para añadir las facturas emitidas a la base de datos hay qeu ejecutar el script "gp-scli.py add_incomes" que espera como entrada un fichero con el formato "facturas_emitidas.template.csv".
* Para añadir las facturas recibidas hay que ejecutar el script "gp-scli.py add_expenses" que espera como entrada un fichero con el formato "facturas_recibidas.template.csv".

### Generar resumen de los trismestres para rellenar el modelo 130

* Ejecutar el script "gp-scli.py make_report". El resumen se genera a partir de la información guardada en la base de datos.
* Ejecutar el script "gp-scli.py make_m130". A partir de los datos introducidos se generar el Modelo 130 .

### Exportar las facturas simplificadas emitidas

* Ejecutar el script "gp-scli.py export_invoices". Las facturas emitidas se generan a partir de la información guardada en la base de datos.

### Exportar los libros de contabilidad 

* Ejecutar el script "gp-scli.py export_books". El libro de gastos y él de ingresos se genera a partir de la información guardada en la base de datos.
