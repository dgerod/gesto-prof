import os
from scripts.common.configuration import Configuration


def show_information():

    configuration = Configuration()
    print("Base de datos: %s" % configuration.get_db_directory())
    print("Entradas: %s" % configuration.get_inputs_directory())
    print("Salidas: %s" % configuration.get_outputs_directory())
