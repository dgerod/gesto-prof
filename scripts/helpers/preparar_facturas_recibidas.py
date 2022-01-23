from paths import add_packages_to_path
add_packages_to_path()


import os
import pandas as pd
from scripts.common.configuration import Configuration


configuration = Configuration()
file_path = os.path.join(configuration.get_inputs_directory(), "facturas_recibidas_1.csv")

column_dates = ["FECHA CONTABILIZADO",
                "FECHA OPERACIÓN"]

column_types = {
    "NÚMERO PROVEEDOR" : str,
    "NÚMERO FACTURA" : str,
    "OPERACIÓN" : str,
    "CONCEPTO" : str,
    "IMPORTE BASE" : float,
    "IMPORTE IVA" : float,
    "IMPORTE RETENCIÓN" : float,
    "IMPORTE RECARGO" : float,
    "IMPORTE TOTAL" : float,
    "IMPORTE PENDIENTE" : float,
    "ESTADO" : str,
    "OBSERVACIONES" : str}

data = pd.read_csv(file_path, sep=";", decimal=".",
                   parse_dates=column_dates, dtype=column_types)

data["FECHA CONTABILIZADO"] = pd.to_datetime(data["FECHA CONTABILIZADO"]).dt.date
data["FECHA OPERACIÓN"] = pd.to_datetime(data["FECHA OPERACIÓN"]).dt.date
print(data)

file_path = os.path.join(configuration.get_outputs_directory(), "facturas_recibidas_2.csv")
data.to_csv(file_path, index=False, sep="";", decimal=".")
