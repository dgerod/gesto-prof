import os
import pandas as pd



class Incomes:

    def __init__(self, df):

        self._df = df


class IncomesLoader:

    def __init__(self, file_path: str):

        column_dates = ["FECHA FACTURA"]
    
        column_types = {
            "NÚMERO CLIENTE" : str,
            "NÚMERO FACTURA" : str,
            "OPERACIÓN" : str,
            "CONCEPTO" : str,
            "IMPORTE BASE" : float,
            "% IVA" : float,
            "IMPORTE IVA" : float,
            "% RETENCIÓN" : float,
            "IMPORTE RETENCIÓN" : float,
            "IMPORTE TOTAL" : float,
            "OBSERVACIONES" : str}
        
        column_names = column_dates + list(column_types.keys())

        self._incomes = pd.read_csv(file_path, sep=';', decimal='.', usecols=column_names,
                                    parse_dates=column_dates, dtype=column_types)

    def incomes(self) -> Incomes:

        return Incomes(self._incomes.copy(deep=True))


class Expenses:

    def __init__(self, df):

        self._df = df


class ExpensesLoader:

    def __init__(self, file_path: str):

        column_dates = ["FECHA CONTABILIZADO",
                        "FECHA OPERACIÓN"]
        
        column_types = {
            "NÚMERO PROVEEDOR" : str,
            "NÚMERO FACTURA" : str,
            "OPERACIÓN" : str,
            "CONCEPTO" : str,
            "IMPORTE BASE" : float,
            "% IVA" : float,
            "IMPORTE IVA" : float,
            "% RETENCIÓN" : float,
            "IMPORTE RETENCIÓN" : float,
            "IMPORTE TOTAL" : float,
            "IMPORTE PENDIENTE" : float,
            "ESTADO" : str,
            "OBSERVACIONES" : str}
        
        column_names = column_dates + list(column_types.keys())
        self._expenses = pd.read_csv(file_path, sep=';', decimal='.', usecols=column_names,
                                     parse_dates=column_dates, dtype=column_types)

    def expenses(self) -> Expenses:

        return Expenses(self._expenses.copy(deep=True))

