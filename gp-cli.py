import os
import sys

_CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.normpath(_CURRENT_DIRECTORY))

import click 
from scripts.operations import show_information
from scripts.operations import export_books
from scripts.operations import generate_simplified_invoices, export_simplified_invoices
from scripts.operations import generate_report_periods
from scripts.operations import generate_m130
from scripts.operations import add_expenses, add_incomes


@click.group()
def main():
    pass


@main.command(name='información')
def show():
    
    show_information()
    

@main.command(name='crear_facturas')
@click.option('-f', '--fichero', 'file_path', type=str, default='', help='Ruta al fichero CSV de facturas emitidas')
def make_invoices_from_file(file_path):
    """
    Crear las facturas emitidas a partir del fichero que se indica. En caso 
    que no se pase un fichero, lo va a buscar al directory e entradas con el nombre 
    'factura_recibidas.csv'.
    """

    if file_path == '':
        generate_simplified_invoices('facturas_emitidas.csv')
    else:
        raise NotImplementedError


@main.command(name='incorporar_gastos')
@click.option('-f', '--fichero', 'file_path', type=str, default='', help='Ruta al fichero CSV de facturas recibidas')
def add_expenses_to_db(file_path):
    """
    Añadir facturas recibidas a la base de datos. En caso que no se pase un 
    fichero, lo va a buscar al directory de entradas con el nombre 'factura_recibidas.csv'.
    """

    if file_path == '':
        add_expenses('facturas_recibidas.csv')
    else:
        raise NotImplementedError


@main.command(name='incorporar_ingresos')
@click.option('-f', '--fichero', 'file_path', type=str, default='', help='Ruta al fichero CSV de facturas emitidas')
def add_incomes_to_db(file_path):
    """
    Añadir facturas emitidas a la base de datos. En caso que no se pase un 
    fichero, lo va a buscar al directory de entradas con el nombre 'factura_emitidas.csv'.
    """

    if file_path == '':
        add_incomes('facturas_emitidas.csv')
    else:
        raise NotImplementedError


@main.command(name='crear_informe')
@click.argument('periodo', type=str, default='total')
@click.option('-a', '--acumulado', 'accumulated', type=bool, default=False, help='Incluir periodos anteriores o no')
def make_report_from_db(periodo, accumulated):
    """
    Crear un informe de un PERIODO determinado a partir de la información en
    la base de datos. En caso que no se pase un directorio lo escribe en el directorio de salidas
    con el nombre 'informe_periodos.txt'.
    """

    if periodo in ['total']:
        generate_report_periods()
    else:
        raise NotImplementedError


@main.command(name='preparar_m130')
@click.option('-f', '--fichero', 'file_path', type=str, default='', help='Ruta al fichero yaml con los datos')
@click.option('-d', '--directorio', 'directory_path', type=str, default='', help='Ruta al directory de salida')
def calculate_m130(file_path, directory_path):
    """
    Calcular información para rellenar el modelo 130 de AEA. En caso que no se pase un 
    fichero, lo va a leer del directorio de entradas con el nombre 'modelo_130_datos.yaml'.
    Y si no se pasa el directory lo escribe en el directorio de salidas con el nombre 
    'calculo_modelo_130.txt'.
    """

    if file_path == '':
        generate_m130('modelo_130_datos.yaml')
    else:
        raise NotImplementedError


@main.command(name='exportar_libros')
@click.option('-d', '--directorio', 'directory_path', type=str, default='', help='Ruta al directory de salida')
def export_books_from_db(directory_path):
    """
    Exportar los libros de ingreso y gastos a partir de la información en la 
    base de datos. En caso que no se pase un directorio lo escribe en el directorio de salidas
    con el nombre 'informe_periodos.txt'.
    """

    if directory_path == '':
        export_books()
    else:
        raise NotImplementedError


@main.command(name='exportar_facturas')
@click.option('-d', '--directorio', 'directory_path', type=str, default='', help='Ruta al directory de salida')
def export_invoices_from_db(directory_path):
    """
    Exportar las facturas emitidas a partir de la información en la base 
    de datos.
    """

    if directory_path == '':
        export_simplified_invoices()
    else:
        raise NotImplementedError


if __name__ == "__main__":
    main() 
