import os
import sys

_CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(os.path.normpath(_CURRENT_DIRECTORY))))

from scripts.helpers.classgap import LessonsIncomeLoader
from scripts.common.configuration import Configuration


configuration = Configuration()

file_path = os.path.join(configuration.get_inputs_directory(), 'classgap_clases_originales.csv')
lessons_loader = LessonsIncomeLoader(file_path)

original_data = lessons_loader.loaded()
data = lessons_loader.data()
print(data)

file_path = os.path.join(configuration.get_outputs_directory(), 'classgap_clases_corregidas.csv')
data.to_csv(file_path, index=False, sep=';', decimal='.')
