import os
import sys

_CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(os.path.normpath(_CURRENT_DIRECTORY))))

import pandas as pd
from scripts.common.configuration import Configuration


configuration = Configuration()
file_path = os.path.join(configuration.get_inputs_directory(), "classgap_servicio_facturas.csv")

column_dates = ["Fecha"]

column_types = {
    "Factura" : str,
    "Serie" : str,
    "Base" : float,
    "IVA" : float,
    "Total" : float}

classgap_data = pd.read_csv(file_path, sep=";", decimal=".",
                   parse_dates=column_dates, dtype=column_types)

# Nuevo fichero

num_rows = len(classgap_data["Fecha"])

data = {}
data["FECHA CONTABILIZADO"] = pd.to_datetime(classgap_data["Fecha"]).dt.date
data["FECHA OPERACIÓN"] = pd.to_datetime(classgap_data["Fecha"]).dt.date
data["NÚMERO PROVEEDOR"] = [""] * num_rows
data["NÚMERO FACTURA"] = classgap_data["Serie"] + "-" + classgap_data["Factura"]
data["OPERACIÓN"] = ["Factura Recibida"] * num_rows
data["CONCEPTO"] = ["Otros Servicios"] * num_rows
data["IMPORTE BASE"] = classgap_data["Base"]
data["% IVA"] = classgap_data["IVA"]
data["IMPORTE IVA"] = classgap_data["Total"] - classgap_data["Base"]
data["% RETENCIÓN"] = [0.0] * num_rows
data["IMPORTE RETENCIÓN"] = [0.0] * num_rows
data["IMPORTE TOTAL"] = classgap_data["Total"]
data["IMPORTE PENDIENTE"] = [0.0] * num_rows
data["ESTADO"] =  ["Pagado"] * num_rows
data["OBSERVACIONES"] = [""] * num_rows

df = pd.DataFrame(data)
#print(data)

file_path = os.path.join(configuration.get_outputs_directory(), "facturas_recibidas_solo_classgap.csv")
df.to_csv(file_path, index=False, sep=";", decimal=".")
