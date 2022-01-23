import os
from typing import Tuple
import pandas as pd
from scripts.common.invoices import Incomes, Expenses


class DataBase:

    _COMPANY_TABLE_FILE = "info_empresa.csv"
    _INCOMES_TABLE_FILE = "ingresos.csv"
    _EXPENSES_TABLE_FILE = "gastos.csv"
    _PROVIDERS_TABLE_FILE = "proveedores.csv"
    _CLIENTS_TABLE_FILE = "clientes.csv"
    _OPERATIONS_TABLE_FILE = "tipo_cuentas.csv"

    def __init__(self, directory_path: str):
        self._directory_path = directory_path

    def retrieve_providers(self) -> pd.DataFrame:
        return self._retrieve_providers()

    def retrieve_clients(self) -> pd.DataFrame:

        column_types = {
            "NÚMERO CLIENTE" : str,
            "NOMBRE": str,
            "PRIMER APELLIDO" : str,
            "SEGUNDO APELLIDO" : str,
            "PERSONA FÍSICA / jURÍDICA": str,
            "TIF" : str,
            "NIF" : str,
            "PAÍS": str,
            "PROVINCIA": str,
            "POBLACIÓN" : str}

        column_names = list(column_types.keys())
        
        file_path = os.path.join(self._directory_path, self._CLIENTS_TABLE_FILE)
        return pd.read_csv(file_path, sep=";", decimal=".", usecols=column_names, 
                           dtype=column_types)

    def retrieve_operations(self) -> pd.DataFrame:
        return self._retrieve_operations()

    def retrieve_incomes(self) -> pd.DataFrame:

        column_dates = ["FECHA FACTURA",
                        "FECHA GUARDADO"]

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

        file_path = os.path.join(self._directory_path, self._INCOMES_TABLE_FILE)
        return pd.read_csv(file_path, sep=";", decimal=".", usecols=column_names,
                           parse_dates=column_dates, dtype=column_types)

    def retrieve_expenses(self) -> pd.DataFrame:

        column_dates = ["FECHA CONTABILIZADO",
                        "FECHA OPERACIÓN",
                        "FECHA GUARDADO"]
        
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
            "ESTADO" : str,
            "OBSERVACIONES" : str}

        column_names = column_dates + list(column_types.keys())

        file_path = os.path.join(self._directory_path, self._EXPENSES_TABLE_FILE)
        return pd.read_csv(file_path, sep=";", decimal=".", usecols=column_names, 
                           parse_dates=column_dates, dtype=column_types)
                           
    def add_incomes(self, incomes: Incomes) -> None:

        df = incomes._df.copy(deep=True)
        db_incomes = self.retrieve_incomes()

        from datetime import date
        d1 = date.today().strftime("%Y-%m-%d")
        
        df.insert(0, "FECHA GUARDADO", [d1]*len(df), True)
        df["FECHA GUARDADO"] = pd.to_datetime(df["FECHA GUARDADO"])
        df = db_incomes.append(df, ignore_index=True)

        file_path = os.path.join(self._directory_path, self._INCOMES_TABLE_FILE)
        df.to_csv(file_path, index=False, sep=";", decimal=".")

    def add_expenses(self, expenses: Expenses) -> None:

        df = expenses._df.copy(deep=True)
        db_expenses = self.retrieve_expenses()

        from datetime import date
        d1 = date.today().strftime("%Y-%m-%d")
        
        df.insert(0, "FECHA GUARDADO", [d1]*len(df), True)
        df["FECHA GUARDADO"] = pd.to_datetime(df["FECHA GUARDADO"])
        df = db_expenses.append(df, ignore_index=True)

        file_path = os.path.join(self._directory_path, self._EXPENSES_TABLE_FILE)
        df.to_csv(file_path, index=False, sep=";", decimal=".")
    
    def get_company_information(self) -> Tuple[str, str]:

        column_types = {
            "NOMBRE": str,
            "NIF" : str}

        column_names = list(column_types.keys())

        file_path = os.path.join(self._directory_path, self._COMPANY_TABLE_FILE)
        df = pd.read_csv(file_path, sep=";", decimal=".", usecols=column_names, 
                         dtype=column_types)
        first_row = df.iloc[0]

        return first_row["NOMBRE"], first_row["NIF"]
    
    def get_provider_information(self, id_: str) -> str:
        
        providers = self._retrieve_providers()

        for _, row in providers.iterrows():
            if row['NÚMERO PROVEEDOR'] == id_:
                return row['NOMBRE'], row['NIF']
        else:
            raise ValueError("Unknown operation type")

    def get_income_concept_id(self, name: str) -> str:
    
        operations = self._retrieve_operations()

        for _, row in operations.iterrows():
            if row['CONCEPTO'] == name:
                return row['CUENTA']
        else:
            raise ValueError("Unknown operation type")
    
    def get_expense_concept_id(self, name: str) -> str:
    
        operations = self._retrieve_operations()

        for _, row in operations.iterrows():
            if row['CONCEPTO'] == name:
                return row['CUENTA']
        else:
            raise ValueError("Unknown operation type")
   
    def _retrieve_providers(self):

        column_types = {
            "NÚMERO PROVEEDOR" : str,
            "NOMBRE": str,
            "PERSONA FÍSICA / JURÍDICA": str,
            "TIF" : str,
            "NIF" : str,
            "PAÍS": str,
            "PROVINCIA": str,
            "POBLACIÓN" : str}

        column_names = list(column_types.keys())
        
        file_path = os.path.join(self._directory_path, self._PROVIDERS_TABLE_FILE)
        return pd.read_csv(file_path, sep=";", decimal=".", usecols=column_names, 
                           dtype=column_types)

    def _retrieve_operations(self):

        column_types = {
            "CONCEPTO" : str,
            "TIPO" : str,
            "CUENTA" : str}

        column_names = list(column_types.keys())

        file_path = os.path.join(self._directory_path, self._OPERATIONS_TABLE_FILE)
        return pd.read_csv(file_path, sep=";", decimal=".", usecols=column_names,
                           dtype=column_types)
                        