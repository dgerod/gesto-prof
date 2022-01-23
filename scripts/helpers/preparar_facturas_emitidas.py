from paths import add_packages_to_path
add_packages_to_path()


import os
from scripts.helpers.classgap import LessonsIncomeLoader
from scripts.common.configuration import Configuration


configuration = Configuration()

file_path = os.path.join(configuration.get_inputs_directory(), 'clases_finalizadas_totales.csv')
lessons_loader = LessonsIncomeLoader(file_path)

original_data = lessons_loader.loaded()
data = lessons_loader.data()
print(data)

file_path = os.path.join(configuration.get_outputs_directory(), 'facturas_emitidas_totales.csv')
data.to_csv(file_path, index=False, sep=';', decimal='.')
