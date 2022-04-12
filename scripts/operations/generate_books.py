import os
import pandas as pd
from scripts.common.configuration import Configuration
from scripts.common.db import DataBase
from scripts.common import periods as taxes_periods


def _generate_incomes_book():

    configuration = Configuration()
    db = DataBase(configuration.get_db_directory())
    incomes = db.retrieve_incomes()
    periods = taxes_periods.generate_periods(configuration.get_year())

    book_entries = []
    for index, row in incomes.iterrows():

        year, period = taxes_periods.get_period_info(row["FECHA FACTURA"].date(), periods)
        operation_type = db.get_income_concept_id(row["CONCEPTO"])

        entry = {
        "ORDEN" : index + 1,
        "EJERCICIO" : year,
        "PERIODO" : "T%s" % period,
        "FECHA EXPEDICIÓN" : row["FECHA FACTURA"].date().strftime("%d/%m/%Y"),
        "FECHA OPERACIÓN" : row["FECHA FACTURA"].date().strftime("%d/%m/%Y"),
        "TIPO OPERACIÓN" : row["OPERACIÓN"],
        "NÚMERO FACTURA" : row["NÚMERO FACTURA"],
        "NÚMERO CLIENTE" : row["NÚMERO CLIENTE"],
        "NIF DESTINATARIO" : "n.a.",
        "NOMBRE DESTINATARIO" : "n.a.",
        "CLAVE CUENTA" : operation_type,
        "DESCRIPCIÓN CUENTA" : row["CONCEPTO"],
        "TOTAL FACTURA" : row["IMPORTE TOTAL"],
        "BASE IMPONIBLE" : row["IMPORTE BASE"],
        "TIPO DE IVA (%)" : row["% IVA"],
        "CUOTA IVA REPERCUTIDA" : row["IMPORTE IVA"],
        "TIPO DE RECARGO DE EQUIVALENCIA (%)" : "0.0",
        "CUOTA RECARGO EQUIVALENCIA" : "0.0",
        "TIPO RETENCIÓN DEL IRPF (%)" : row["% RETENCIÓN"],
        "IMPORTE RETENIDO DEL IRPF" : row["IMPORTE RETENCIÓN"]}

        book_entries.append(entry)

    print("Num entries in incomes book: %s" % len(book_entries))

    df = pd.DataFrame(book_entries)
    file_path = os.path.join(configuration.get_outputs_directory(), "libro_ventas_e_ingresos.csv")
    df.to_csv(file_path, index=False, sep=";", decimal=".")

def _generate_expenses_book():

    configuration = Configuration()
    db = DataBase(configuration.get_db_directory())
    expenses = db.retrieve_expenses()
    periods = taxes_periods.generate_periods(configuration.get_year())

    book_entries = []
    for index, row in expenses.iterrows():

        year, period = taxes_periods.get_period_info(row["FECHA OPERACIÓN"].date(), periods)
        operation_type = db.get_expense_concept_id(row["CONCEPTO"])
        provider_name, provider_nif = db.get_provider_information(row["NÚMERO PROVEEDOR"])

        entry = {
            "ORDEN" : index + 1,
            "EJERCICIO" : year,
            "PERIODO" : "T%s" % period,
            "FECHA EXPEDICIÓN" : row["FECHA OPERACIÓN"].date().strftime("%d/%m/%Y"),
            "FECHA OPERACIÓN" : row["FECHA OPERACIÓN"].date().strftime("%d/%m/%Y"),
            "TIPO OPERACIÓN" : row["OPERACIÓN"],
            "NÚMERO FACTURA" : row["NÚMERO FACTURA"],
            "NÚMERO PROVEEDOR" : row["NÚMERO PROVEEDOR"],
            "NIF EXPENDIDOR" : provider_nif,
            "NOMBRE EXPENDIDOR" : provider_name,
            "CLAVE CUENTA" : operation_type,
            "DESCRIPCIÓN CUENTA" : row["CONCEPTO"],
            "TOTAL FACTURA" : row["IMPORTE TOTAL"],
            "BASE IMPONIBLE" : row["IMPORTE BASE"],
            "TIPO DE IVA (%)" : row["% IVA"],
            "CUOTA IVA SOPORTADO" : row["IMPORTE IVA"],
            "TIPO DE RECARGO EQUIVALENTE (%)" : "0.0",
            "CUOTA RECARGO EQUIVALENCIA" : "0.0",
            "TIPO RETENCIÓN DEL IRPF (%)" : row["% RETENCIÓN"],
            "IMPORTE RETENIDO DEL IRPF" : row["IMPORTE RETENCIÓN"]}

        book_entries.append(entry)
    
    print("Num entries in expenses book: %s" % len(book_entries))

    df = pd.DataFrame(book_entries)
    file_path = os.path.join(configuration.get_outputs_directory(), "libro_compras_y_gastos.csv")
    df.to_csv(file_path, index=False, sep=";", decimal=".")


def export_books():
    _generate_incomes_book()
    _generate_expenses_book()
